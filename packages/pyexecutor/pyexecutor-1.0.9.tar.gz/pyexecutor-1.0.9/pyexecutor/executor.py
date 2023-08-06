import platform

from pyexecutor import Commander
from pyexecutor import Logger


class Executor():

    _logger = None
    _commander = None
    _executor = None
    _trailer = ''

    def __init__(self, executable, logger=None):
        self._commander = Commander(logger=logger)
        self._set_logger(logger=logger)
        self._set_executor(executable)

    """
    Choose available executor
    """
    def _set_executor(self, executor):
        system = platform.system()

        if system == 'Linux' or system == 'Darwin':
            self._search_linux(executor)
        elif system == 'Windows':
            self._search_windows(executor)
        else:
            raise ExecutorException('Unsupported OS type %s!' % (system))

        if self._executor is None:
            raise ExecutorException('Executor %s not found' % (executor))

        self._logger.info('Choose "%s" as executor' % (self._executor))

    """
    Search available executors in Linux system
    """
    def _search_linux(self, executor):
        result = self._commander.run("which", executor, True)

        executors = result.output().replace("\n", "&PYEXECUTOR&").replace("\r", "&PYEXECUTOR&").split("&PYEXECUTOR&")

        self._logger.debug("Available executors found: %s" % executors)

        if len(executors) > 0:
            self._executor = executors[0]

    """
    Search available executors in Windows system
    """
    def _search_windows(self, executor):
        result = self._commander.run("where", executor, True)

        executors = result.output().replace("\n", "&PYEXECUTOR&").replace("\r", "&PYEXECUTOR&").split("&PYEXECUTOR&")

        self._logger.debug("Available executors found: %s" % executors)

        for item in executors:
            if item.endswith(".exe") or item.endswith(".bat"):
                self._executor = item

    """
    Set command trailer
    """
    def set_trailer(self, trailer):
        self._trailer = trailer

    """
    Run commands with commander
    """
    def _run(self, args):
        args = '%s %s' % (args, self._trailer)

        try:
            self._commander.run(self._executor, args)

            return self._commander
        except Exception as e:
            raise ExecutorException(str(e))

    """
    Run commands with pretty outputs
    """
    def run(self, args, json_output=False):
        if json_output:
            return self._run(args).json()

        return self._run(args).output()

    """
    Set the execution logger
    """
    def _set_logger(self, logger):
        self._logger = Logger(logger)

class ExecutorException(Exception): ...