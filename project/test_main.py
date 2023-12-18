import unittest

if __name__ == '__main__':

    test_pattern = 'test_*.py'


    test_directory = 'tests'
    import os
    print(os.getcwd())


    test_loader = unittest.TestLoader()

    test_suite = test_loader.discover(start_dir=test_directory, pattern=test_pattern)
    test_runner = unittest.TextTestRunner()
    test_runner.run(test_suite)
