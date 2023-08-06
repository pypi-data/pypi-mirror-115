import subprocess

from tchotchke.exceptions import ShellError


class Shell:
    def __init__(self, logger):
        self.__logger = logger

    def execute_for_stdout(self, command, insured=True):
        process_result = self.execute(command, insured)
        return process_result.stdout.strip()

    def execute(self, command, insured=True, capture_output=True):
        process_result = subprocess.run(command, capture_output=capture_output, shell=True, encoding="UTF-8")
        if insured:
            self.__ensure_successful_return_code(process_result)
        return process_result

    @staticmethod
    def __ensure_successful_return_code(process_result):
        if process_result.returncode != 0:
            raise ShellError("subprocess command failed", {"process_result": repr(process_result)})
