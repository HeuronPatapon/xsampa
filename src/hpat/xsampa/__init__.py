__author__ = "Heuron Patapon"
__email__ = "heuron-patapon@laposte.net"
__version__ = "1.1.3"


import doctest
import unittest


from .converters import XSAMPA


def load_tests(loader, tests, ignore):
    from . import test
    suite = unittest.defaultTestLoader.loadTestsFromModule(test, ignore)
    tests.addTests(suite)

    from . import converters
    converters.load_tests(loader, tests, ignore)
    return tests
