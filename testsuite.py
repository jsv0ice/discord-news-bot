import unittest

# Import your test modules
from src.commands.subscribe.test_subscribe import *
from src.commands.unsubscribe.test_unsubscribe import *

# Create the test suite
def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SubscribeTest))
    suite.addTest(unittest.makeSuite(UnSubscribeTest))
    # Add other test modules here

    return suite

# Run the test suite
if __name__ == '__main__':
    suite = test_suite()
    runner = unittest.TextTestRunner()
    runner.run(suite)