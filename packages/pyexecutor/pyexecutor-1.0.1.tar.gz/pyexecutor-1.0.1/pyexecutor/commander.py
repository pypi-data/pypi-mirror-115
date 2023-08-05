import json
import subprocess

from pyexecutor.exceptions import CommanderException
from pyexecutor import Logger


class Commander():
    _output = ''
    _error = ''
    _returncode = 0
    _logger = None

    def __init__(self, logger=None):
        self._set_logger(logger)

    """
    Run command with sub process
    """
    def run(self, cmd, supress_error=False):
        self._logger.info('Running command {}.'.format(cmd))

        if supress_error:
            self._logger.warning('Supress error is True, will not throw any exceptions even if any error occured when running command!')

        try:
            result = subprocess.run(cmd.strip().split(' '), capture_output=True)
            self._output = result.stdout
            self._error = result.stderr

            if result.returncode != 0:
                raise CommanderException(result.stderr)

            self._returncode = 0

            self._logger.info('Run command sucessfully!'.format(cmd))
            return self
        except Exception as e:
            self._logger.error('Error occured! {}'.format(e))

            self._returncode = 1

            if not supress_error:
                raise e

            self._logger.warning('The command error is supressed due to supress_error is True!')

            return self

    """
    Get output message
    """
    def output(self):
        return self._output.decode("utf8").strip()

    """
    Get output message in JSON format
    """
    def json(self):
        try:
            return json.loads(self.output())
        except Exception as e:
            self._logger.error('Cannot convert command output to JSON object, {}'.format(e))
            raise CommanderException('Invalid JSON string "{}"'.format(self._output))

    """
    Get error message
    """
    def error(self):
        return self._error.decode("utf8").strip()

    """
    Return code is 0
    """
    def ok(self):
        return self._returncode == 0

    """
    Return code is not 0
    """
    def fail(self):
        return self._returncode != 0

    """
    Set the command logger
    """
    def _set_logger(self, logger):
        self._logger = Logger(logger)
