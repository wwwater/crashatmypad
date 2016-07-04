import unittest
from coverage import coverage
from crashatmypad import create_app


if __name__ == "__main__":
    cov = coverage(branch=True, omit=['/usr/local/lib/*', '*_test.py'])
    cov.start()
    app = create_app('TESTING')
    suite = unittest.TestSuite()
    test_suite = unittest.TestLoader().discover('crashatmypad', '*_test.py')
    unittest.TextTestRunner(verbosity=1).run(test_suite)
    cov.stop()
    cov.save()
    print("\n\nCoverage Report:\n")
    cov.report()
    print("HTML version: tmp/coverage/index.html")
    cov.html_report(directory='tmp/coverage')
    cov.erase()
