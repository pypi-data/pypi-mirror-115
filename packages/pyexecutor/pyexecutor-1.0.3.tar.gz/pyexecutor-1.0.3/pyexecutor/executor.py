from pyexecutor.exceptions import ExecutorException
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
    Find proper executor
    """
    def _set_executor(self, executable):
        for hunter in ['which', 'where']:
            self._logger.debug('Trying executable file with %s' % (hunter))

            result = self._commander.run(hunter, executable, True)

            if self._commander.ok():
                self._executor = result.output().replace("\n", "&PYEXECUTOR&").replace("\r", "&PYEXECUTOR&").split("&PYEXECUTOR&")[0]
                self._logger.info('Executable file found %s' % (self._executor))
                break

        if self._executor is None:
            self._logger.error('Executable file not found %s' % (executable))
            raise ExecutorException('Executable file %s not found!' % (executable))

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
            self._logger.debug('Execute with JSON output %s' % (self._executor))
            return self._run(args).json()

        self._logger.debug('Execute %s' % (self._executor))
        return self._run(args).output()

    """
    Set the execution logger
    """
    def _set_logger(self, logger):
        self._logger = Logger(logger)
