import ast
import unittest


class InventoryAppTestCase(unittest.TestCase):

    def test_app_file_exists_and_is_valid_python(self):
        with open("app.py", "r", encoding="utf-8") as file:
            source = file.read()

        ast.parse(source)

        self.assertTrue(len(source) > 0)


if __name__ == "__main__":
    unittest.main()