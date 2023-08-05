#from logging import info, warning, error
import logging

logger = logging.getLogger()

class Messages:

    def write_message(self, message: str, skip_newline=False):

        if not skip_newline:
            print(message)
        else:
            print(message, end='')

    def write_warning(self, message: str):

        print('WARNING: {}'.format(message))

    def write_exception(self, message: str):

        print('EXCEPTION: {}'.format(message))
