class Logger():
    _logger = None

    def __init__(self, logger = None):
        self._logger = logger

    def debug(self, message):
        if self._logger is None:
            print("DEBUG: " + message)
            return

        self._logger.debug(message)

    def verbose(self, message):
        if self._logger is None:
            print("VERBOSE: " + message)
            return

        self._logger.verbose(message)

    def info(self, message):
        if self._logger is None:
            print("INFO: " + message)
            return

        self._logger.info(message)

    def warning(self, message):
        if self._logger is None:
            print("WARNING: " + message)
            return

        self._logger.warning(message)

    def error(self, message):
        if self._logger is None:
            print("ERROR: " + message)
            return

        self._logger.error(message)