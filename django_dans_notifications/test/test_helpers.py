from django.test import TestCase
from ..helpers import str_to_bool


class TestStrToBool(TestCase):
    def test_true_values(self):
        true_values = ["yes", "true", "t", "1", "on", "YES", "True", "T", "1", "ON"]
        for value in true_values:
            with self.subTest(value=value):
                self.assertTrue(str_to_bool(value))

    def test_false_values(self):
        false_values = [
            "no",
            "false",
            "f",
            "0",
            "off",
            "NO",
            "False",
            "F",
            "0",
            "OFF",
            "",
            None,
            "random",
            123,
        ]
        for value in false_values:
            with self.subTest(value=value):
                self.assertFalse(str_to_bool(value))
