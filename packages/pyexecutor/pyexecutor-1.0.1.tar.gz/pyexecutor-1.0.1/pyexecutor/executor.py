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
        for executor in ['which {}'.format(executable), 'where {}'.format(executable), 'where {}.exe'.format(executable)]:
            self._logger.debug('Trying executable file with {}'.format(executor))

            result = self._commander.run(executor, True)

            if self._commander.ok():
                self._executor = result.output()
                self._logger.info('Executable file found {}'.format(self._executor))
                break

        if self._executor is None:
            self._logger.error('Executable file not found {}'.format(executable))
            raise ExecutorException('Executable file {} not found!'.format(executable))

    """
    Set command trailer
    """
    def set_trailer(self, trailer):
        self._trailer = trailer

    """
    Run commands with commander
    """
    def _run(self, cmd):
        executable_cmd = '{} {} {}'.format(self._executor, cmd, self._trailer)
        self._logger.debug('Full command "{}"'.format(executable_cmd))
        try:
            self._commander.run(executable_cmd)

            return self._commander
        except Exception as e:
            raise ExecutorException(str(e))

    """
    Run commands with pretty outputs
    """
    def run(self, cmd, json_output=False):
        if json_output:
            self._logger.debug('Execute with JSON output {}'.format(self._executor))
            return self._run(cmd).json()

        self._logger.debug('Execute {}'.format(self._executor))
        return self._run(cmd).output()

    """
    Set the execution logger
    """
    def _set_logger(self, logger):
        self._logger = Logger(logger)
