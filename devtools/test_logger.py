from unittest import TestCase

from devtools import logger


class Test(TestCase):
    def test_log(self):
        logger.set_log_level('debug',show_core=True, show_thread=True)
        logger.log('test', 'info', 'yellow',flush=True)
