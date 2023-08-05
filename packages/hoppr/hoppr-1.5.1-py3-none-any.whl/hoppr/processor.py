"""
Run Hoppr processing, using multiple processors
"""
from __future__ import annotations

import os
import logging
import platform
import shutil
import socket
import tempfile
import time

from concurrent.futures import Future, ProcessPoolExecutor
from datetime import datetime
from itertools import zip_longest
from multiprocessing import cpu_count
from os import PathLike
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
from urllib.parse import quote_plus

from hoppr_cyclonedx_models.cyclonedx_1_4 import Component  # type: ignore
from packageurl import PackageURL  # type: ignore
from typer import colors, echo, secho

from hoppr.base_plugins.hoppr import HopprPlugin
from hoppr.configs.manifest import Manifest
from hoppr.configs.transfer import Transfer
from hoppr.context import Context
from hoppr.exceptions import HopprPluginError
from hoppr.flatten_sboms import flatten_sboms
from hoppr.hoppr_types.component_coverage import ComponentCoverage
from hoppr.hoppr_types.transfer_file_content import Stage as StageRef
from hoppr.mem_logger import MemoryLogger
from hoppr.net import download_file
from hoppr.result import Result
from hoppr.utils import plugin_instance

if "nux" in platform.system():
    import pwd  # pylint: disable=import-error


def _run_plugin(
    plugin: HopprPlugin, method_name: str, component: Optional[Component]
) -> Result:
    """
    Runs a single method for a single component (if supplied) on a single plugin
    """
    if method_name == HopprPlugin.pre_stage_process.__name__:
        result = plugin.pre_stage_process()
    elif method_name == HopprPlugin.process_component.__name__:
        result = plugin.process_component(component)
    elif method_name == HopprPlugin.post_stage_process.__name__:
        result = plugin.post_stage_process()
    else:
        result = Result.fail(f"Invalid method: {method_name}")

    return result


class StageProcessor:  # pylint: disable=too-few-public-methods
    """
    Class to handle all processing within a single Hoppr stage
    """

    component_based_methods = [HopprPlugin.process_component.__name__]

    def __init__(self, stage_ref: StageRef, context: Context):
        self.stage_id = stage_ref.name
        self.context = context
        self.plugin_ref_list = stage_ref.plugins
        self.component_coverage = None
        if stage_ref.component_coverage is not None:
            self.component_coverage = ComponentCoverage[stage_ref.component_coverage]
        self.plugins: List[HopprPlugin] = []
        self.results: Dict = {}

    def run(self) -> Result:
        """
        Run all processes for this stage
        """

        try:
            self.plugins = self._load_plugins()
        except (ModuleNotFoundError, HopprPluginError) as err:
            return Result.fail(str(err))

        result = Result.success()

        # Run each sub-stage (pre_stage_process, process_component, post_stage_process)
        # for all plugins (and, for process_component, for all components).
        # Each sub-stage must complete before the next can begin

        result.merge(self._run_all(HopprPlugin.pre_stage_process.__name__))
        result.merge(self._run_all(HopprPlugin.process_component.__name__))
        result.merge(self._run_all(HopprPlugin.post_stage_process.__name__))

        return result

    def _run_all(self, method_name: str):
        """
        Run the named method for all plugins.  If appropriate to the method, run it for
        all components for all plug-ins.
        """

        futures = []

        # Map to allow access to the arguments that went into a future call
        future_argument_map: Dict[Future, Tuple[HopprPlugin, Optional[Component]]] = {}

        with ProcessPoolExecutor(max_workers=self.context.max_processes) as executor:
            for plugin in self.plugins:
                if method_name in self.component_based_methods:

                    # Create one concurrent future object to run this method for each component

                    for component in self.context.consolidated_sbom.components or []:
                        future_proc = executor.submit(
                            _run_plugin, plugin, method_name, component
                        )
                        future_argument_map[future_proc] = (plugin, component)
                        futures.append(future_proc)
                else:

                    # Create a concurrent future object to run this method

                    future_proc = executor.submit(
                        _run_plugin, plugin, method_name, None
                    )
                    future_argument_map[future_proc] = (plugin, None)
                    futures.append(future_proc)

            # Save all the results, count failures and retries
            # Note: future.results() blocks until the process is complete

            need_method_label = True
            failures = 0
            retries = 0
            for future_proc in futures:
                future_result = future_proc.result()
                if not future_result.is_skip():
                    if need_method_label:
                        echo(f"   Beginning method {method_name}")
                        need_method_label = False
                    plugin, comp = future_argument_map[future_proc]
                    self._save_result(
                        method_name, plugin.__class__.__name__, future_result, comp
                    )
                    self._report_result(plugin.__class__.__name__, comp, future_result)

                    if future_result.is_fail():
                        failures += 1
                    if future_result.is_retry():
                        retries += 1

        if method_name in self.component_based_methods:
            failures += self._check_component_coverage(method_name)

        return self._get_stage_result(method_name, failures, retries)

    def _get_stage_result(
        self, method_name: str, failures: int, retries: int
    ) -> Result:
        if failures + retries == 0:
            return Result.success()
        if failures == 0 and retries > 0:
            return Result.fail(f"{retries} '{method_name}' processes returned 'retry'")
        if failures > 0 and retries == 0:
            return Result.fail(f"{failures} '{method_name}' processes failed")
        return Result.fail(
            f"{failures} '{method_name}' processes failed, and {retries} returned 'retry'"
        )

    def _get_required_coverage(self) -> ComponentCoverage:
        if self.component_coverage is not None:
            return self.component_coverage

        if len(self.plugins) == 0:
            return ComponentCoverage.OPTIONAL

        coverage = self.plugins[0].default_component_coverage

        for plugin in self.plugins:
            if plugin.default_component_coverage != coverage:
                raise HopprPluginError(
                    f"Plugins for stage {self.stage_id} do not have consistent default "
                    + "component coverage values.  The value may be overridden in transfer file."
                )

        return coverage

    def _check_component_coverage(self, method_name: str) -> int:
        required_coverage = self._get_required_coverage()
        result_count: Dict[Optional[str], int] = {}
        for (_, purl, _) in self.results.get(method_name, []):
            result_count[purl] = result_count.get(purl, 0) + 1

        additional_failures = 0
        for component in self.context.consolidated_sbom.components or []:
            count = result_count.get(component.purl, 0)
            if not required_coverage.accepts_count(count):
                bad_comp_result = Result.fail(
                    f"Component processed {count} times, {required_coverage.name} coverage required"
                )
                self._save_result(
                    method_name, f"Stage {self.stage_id}", bad_comp_result, component
                )
                self._report_result(
                    f"Stage {self.stage_id}", component, bad_comp_result
                )
                additional_failures += 1

        return additional_failures

    @staticmethod
    def _report_result(plugin, comp, result):
        desc = f"      {plugin} {result.status.name}"
        if comp is not None:
            desc = desc + f" for {comp.purl}"
        color = colors.GREEN
        if not result.is_success():
            color = colors.RED
            desc = desc + f": {result.message}"
        secho(desc, fg=color)

    def _save_result(
        self,
        method_name: str,
        plugin: str,
        result: Result,
        comp: Optional[Component],
    ):
        """
        Store the results for later use
        """
        comp_string = None
        if comp is not None and PackageURL.from_string(comp.purl) is not None:
            comp_string = comp.purl

        # If needed, create a new list for this method
        # Might need to expand this definition in the future to separate by plug-in

        if not method_name in self.results:
            self.results[method_name] = []

        self.results[method_name].append((plugin, comp_string, result))

    def _load_plugins(self) -> List[HopprPlugin]:
        """
        Create a list consisting of a single instance of each plug-in class used in this stage
        """
        plugin_list = []
        for plugin_ref in self.plugin_ref_list:
            plugin_inst = plugin_instance(
                plugin_ref.name, self.context, plugin_ref.config
            )
            plugin_list.append(plugin_inst)

        return plugin_list


class HopprProcessor:  # pylint: disable=too-few-public-methods
    """
    Run the Hoppr process
    """

    def __init__(
        self, transfer: Transfer, manifest: Manifest, log_level: int = logging.INFO
    ) -> None:
        self.transfer = transfer
        self.manifest = manifest
        self.context: Context
        self.stages: Dict = {}
        self.metadata_files: List[Path] = []
        self.logger: Optional[MemoryLogger] = None
        self.log_level = log_level

    def get_logger(self):
        """
        Returns the logger for this class
        """
        return self.logger

    def _collect_file(
        self,
        file_name: Union[str, PathLike[str]],
        target_dir: Union[str, PathLike[str]],
    ) -> None:
        self.get_logger().info(f"Collecting metadata file {file_name}")
        abs_path = Path(file_name).absolute()

        target = Path(target_dir, quote_plus(f"{abs_path}"))
        shutil.copyfile(file_name, f"{target}")

    def _collect_url(
        self, url: Union[str, PathLike[str]], target_dir: Union[str, PathLike[str]]
    ) -> None:
        self.get_logger().info(f"Collecting metadata from url {url}")

        target = Path(target_dir, quote_plus(f"{url}"))
        download_file(url, f"{target}", None)

    def _collect_manifest_metadata(
        self, manifest: Manifest, target_dir: Union[str, PathLike[str]]
    ) -> None:
        for (child_ref, child) in zip_longest(
            manifest.manifest_file_content.includes, manifest.children
        ):
            if child_ref.local is not None:
                self._collect_file(child_ref.local, target_dir)
            else:
                self._collect_url(f"{child_ref.url}", Path(target_dir))

            self._collect_manifest_metadata(child, target_dir)

        for bom_ref in manifest.manifest_file_content.sbom_refs:
            if bom_ref.local is not None:
                self._collect_file(bom_ref.local, target_dir)
            else:
                self._collect_url(f"{bom_ref.url}", target_dir)

    def _collect_metadata(self):
        echo("Collecting Hoppr Metadata")
        target_dir = Path(self.context.collect_root_dir, "generic", "_metadata_")
        target_dir.mkdir(exist_ok=True, parents=True)

        if "nux" in platform.system():
            user = pwd.getpwuid(os.getuid())[0]  # pylint: disable=no-member
        else:
            user = os.getlogin()

        with open(target_dir.joinpath("_run_data_"), "w", encoding="utf-8") as rundata:
            rundata.writelines(
                [
                    f"Collection Start: {str(datetime.now())}\n",
                    f"User:             {user}\n",
                    f"Host FQDN:        {socket.getfqdn()}\n",
                ]
            )

        for file_name in self.metadata_files:
            self._collect_file(file_name, target_dir)

        self._collect_manifest_metadata(self.context.manifest, target_dir)

    def _collect_bom(self) -> None:
        target_dir = Path(self.context.collect_root_dir, "generic", "_metadata_")
        target_dir.mkdir(parents=True, exist_ok=True)

        with open(
            target_dir.joinpath("_consolidated_bom.json"), "w", encoding="utf-8"
        ) as bom_data:
            bom_data.write(self.context.consolidated_sbom.json(by_alias=True, indent=2))

    def _summarize_results(self) -> int:
        """
        Summarize the results of a HopprProcess run
        """

        echo("\n========== Results Summary ==========")
        total_success_count = 0
        total_failure_count = 0
        for stage_id, stage in self.stages.items():
            echo(f"\nStage: {stage_id}")
            for method_name, result_list in stage.results.items():
                echo(f"   {method_name}")
                result_count = len(result_list)
                failure_count = 0
                failure_list = "\n      Failure Summary:\n"
                for plugin_name, comp_str, result in result_list:

                    # All retries should be handled internally by the plugins,
                    # So if a RETRY result is returned, that's a failure

                    if result.is_fail() or result.is_retry():
                        failure_count += 1
                        failure_list += f"         {plugin_name}: "
                        if comp_str is not None:
                            failure_list += f"Component: {comp_str}: "
                        failure_list += result.message + "\n"

                total_failure_count += failure_count
                total_success_count += result_count - failure_count
                echo(
                    f"      {result_count - failure_count} jobs succeeded, {failure_count} failed"
                )
                if failure_count > 0:
                    echo(failure_list)

        echo(
            f"\nGRAND TOTAL: {total_success_count} jobs succeeded, {total_failure_count} failed\n"
        )
        return total_failure_count

    def run(self, log_file: Optional[Path] = None) -> Result:
        """
        Run the Hoppr process executing each stage in turn
        """
        result = Result.success()

        with tempfile.TemporaryDirectory() as collection_root:

            self.context = Context(
                manifest=self.manifest,
                collect_root_dir=collection_root,
                consolidated_sbom=flatten_sboms(self.manifest),
                max_processes=cpu_count(),
                log_level=self.log_level,
            )
            if self.transfer.content:
                self.context.max_processes = self.transfer.content.max_processes

            logger_name: str = f"HopprProcessor--{os.getpid()}"

            self.context.logfile_location = (
                f"hoppr_{time.strftime('%Y%m%d-%H%M%S')}.log"
            )
            if log_file is not None:
                self.context.logfile_location = str(log_file)

            self.logger = MemoryLogger(
                self.context.logfile_location,
                lock=self.context.logfile_lock,
                log_name=logger_name,
                log_level=self.context.log_level,
                flush_immed=True,
            )

            self.get_logger().info(
                f"Beginning Hoppr Process execution, max_processes={self.context.max_processes}"
            )
            echo(
                f"Beginning Hoppr Process execution, max_processes={self.context.max_processes}"
            )
            self._collect_metadata()

            if self.transfer.content is not None:
                for stage_ref in self.transfer.content.stages:
                    self.get_logger().info(
                        f"{'=' * 10} Beginning Stage {stage_ref.name} {'=' * 50}"
                    )
                    echo(f"{'=' * 10} Beginning Stage {stage_ref.name} {'=' * 50}")

                    stage = StageProcessor(stage_ref, self.context)
                    self.stages[stage_ref.name] = stage
                    result = stage.run()
                    if result.is_fail() or result.is_retry():
                        self.logger.error(
                            f"Stage {stage_ref.name} failed, processing terminated: {result.message}"
                        )
                        secho(
                            f"   Stage {stage_ref.name} failed, processing terminated: {result.message}",
                            fg=colors.RED,
                        )
                        break

                    self._collect_bom()

        failed_jobs = self._summarize_results()
        if failed_jobs > 0:
            result.merge(Result.fail(f"{failed_jobs} failed during this execution"))

        return result
