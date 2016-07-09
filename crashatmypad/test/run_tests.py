import os
import unittest
from coverage import coverage


if __name__ == "__main__":
    cov = coverage(branch=True, omit=['/usr/local/lib/*', '*/test/*'])
    cov.start()
    suite = unittest.TestSuite()
    test_suite = unittest.TestLoader().discover('crashatmypad', '*_test.py')
    unittest.TextTestRunner(verbosity=2).run(test_suite)
    cov.stop()
    cov.save()
    print("\n\nCoverage Report:\n")
    cov.report()
    print("HTML version: tmp/coverage/index.html")
    cov.html_report(directory=os.path.join(os.curdir, 'tmp/coverage'))
    cov.erase()
