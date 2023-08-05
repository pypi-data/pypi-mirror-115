"""
Should be raised when exceptions / errors occurred during run commands with Executor
"""
class ExecutorException(Exception):
    def __init__(self, message):
        self._message = message

    def __str__(self):
        return "EXECUTOR EXCEPTION: {}".format(self._message)
