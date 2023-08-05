"""
Class to store results of processes
"""

import enum

import requests


class ResultStatus(enum.IntEnum):
    """
    Enumeration of possible result states
    """

    SUCCESS = 0
    RETRY = 1
    FAIL = 2
    SKIP = 3


class Result:
    """
    Class to store results of processes
    """

    def __init__(self, status: ResultStatus, message: str = ""):
        self.status = status
        self.message = message

    def __str__(self):
        result_msg = f"{self.status.name}"
        if self.message != "":
            result_msg += f", msg: {self.message}"

        return result_msg.rstrip()

    @staticmethod
    def success(message: str = "") -> "Result":
        """
        Convenience method for generating success messages
        """
        return Result(ResultStatus.SUCCESS, message)

    @staticmethod
    def retry(message: str = "") -> "Result":
        """
        Convenience method for generating retry messages
        """
        return Result(ResultStatus.RETRY, message)

    @staticmethod
    def fail(message: str = "") -> "Result":
        """
        Convenience method for generating failure messages
        """
        return Result(ResultStatus.FAIL, message)

    @staticmethod
    def skip(message: str = "") -> "Result":
        """
        Convenience method for generating skip messages
        """
        return Result(ResultStatus.SKIP, message)

    def is_success(self) -> bool:
        """
        Convenience method for testing for success messages
        """
        return self.status == ResultStatus.SUCCESS

    def is_retry(self) -> bool:
        """
        Convenience method for testing for retry messages
        """
        return self.status == ResultStatus.RETRY

    def is_fail(self) -> bool:
        """
        Convenience method for testing for failure messages
        """
        return self.status == ResultStatus.FAIL

    def is_skip(self) -> bool:
        """
        Convenience method for testing for skip messages
        """
        return self.status == ResultStatus.SKIP

    def merge(self, other: "Result"):
        """
        Logically combine two Result objects
        """
        if other.is_skip():
            return

        self.status = max(self.status, other.status)
        if self.message == "":
            self.message = other.message
        else:
            self.message += "\n" + other.message

        return

    @staticmethod
    def from_http_response(response: requests.Response):
        """
        Build a Result object from an HTTP request response
        """

        match response.status_code:
            case response_code if 200 <= response_code <= 299:  # pylint: disable=used-before-assignment
                status = ResultStatus.SUCCESS
            case response_code if 500 <= response_code:
                status = ResultStatus.RETRY
            case _:
                status = ResultStatus.FAIL

        message = f"HTTP Status Code: {response.status_code}"

        if status.name in ["RETRY", "FAIL"]:
            message = f"{message}; {response.reason or response.text}"

        return Result(status, message)
