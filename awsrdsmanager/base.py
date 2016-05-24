import logging
import os


class Base(object):
    """
    Handles common functionality across all cli command classes.
    """

    @staticmethod
    def _add_logging_options(argument_parser):
        """
        Add logging cli options.

        :param argparse.ArgumentParser argument_parser:
        :return:
        """

        logging_args = argument_parser.add_argument_group('Logging')
        logging_args.add_argument('--log-level', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'],
                                  default='ERROR')

    def __init__(self, logging_level, enable_logging=True, dry_run=False):
        """
        Specify the logging_level, and wether or not to perform actions

        :param string logging_level:
        :param bool dry_run:
        :return:
        """
        self.logging_level = logging_level
        self.enable_logging = enable_logging
        self.dry_run = dry_run
        self._init_logger()

    def _init_logger(self):
        """
        Initialises a logger
        
        :return:
        """
        self.logger = logging.getLogger(__name__)

        self.debug = (os.environ.get('DEBUG', '0') == '1')

        if self.debug:
            formatter = logging.Formatter(
                'AWS-RDSMan[%(threadName)10s:%(relativeCreated)5d:%(filename)17s:%(lineno)3s] %(levelname)s:%(message)s')
            stdout_handler = logging.StreamHandler()
            stdout_handler.setFormatter(formatter)
            self.logger.addHandler(stdout_handler)
            self.logger.setLevel(logging.DEBUG)
            self.logger.propagate = False
        else:
            formatter = logging.Formatter(
                'AWS-RDSMan: %(levelname)s:%(message)s'
            )
            stdout_handler = logging.StreamHandler()
            stdout_handler.setFormatter(formatter)
            self.logger.addHandler(stdout_handler)
            self.logger.setLevel(self.logging_level)
            self.logger.propagate = False

        if not self.enable_logging:
            self.logger.disabled = True
