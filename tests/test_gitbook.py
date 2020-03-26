"""
- run:
    name: ⚗️ Functional testing
    command: |
    python -m pytest .
"""

import subprocess
import unittest


def execute(args: str):
    return "ygitbookintegration {}".format(str)


class TestCommand(unittest.TestCase):

    def setUp(self):
        subprocess.run("pip install .")

    def test_base_integration(self):
        subprocess.run(execute("."))

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
