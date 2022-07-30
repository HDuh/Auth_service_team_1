import unittest

loader = unittest.TestLoader()
tests_suite = loader.discover('')
tests_run = unittest.TextTestRunner(verbosity=2)
tests_run.warnings = "ignore"

if __name__ == "__main__":
    print("Count of tests: " + str(tests_suite.countTestCases()) + "\n")

    status = None

    res = tests_run.run(tests_suite)

    if res.wasSuccessful():
        status = "SUCCESS"
    else:
        status = "FAIL"

    print(f'\nErrors: {len(res.errors)}'
          f'\nFailed Tests: {len(res.failures)}')
    print(f'Tests status: {status}')
