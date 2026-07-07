import unittest

from main import format_inference_error


class FormatInferenceErrorTests(unittest.TestCase):
    def test_rate_limit_error_message(self):
        message = format_inference_error(Exception("rate limit"))
        self.assertIn("currently unavailable", message)
        self.assertIn("quota", message.lower())

    def test_generic_error_message(self):
        message = format_inference_error(Exception("boom"))
        self.assertIn("sorry", message.lower())


if __name__ == "__main__":
    unittest.main()
