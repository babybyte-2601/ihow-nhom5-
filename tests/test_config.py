"""
Unit tests for iHOW configuration module
"""

import os
import unittest
from unittest.mock import patch

import config


class TestConfig(unittest.TestCase):

    def test_default_models_defined(self):
        self.assertTrue(len(config.DEFAULT_MODELS_NORMAL) > 0)
        self.assertTrue(len(config.DEFAULT_MODELS_HIGH) > 0)
        self.assertIn("gemini-3.5-flash-lite", config.DEFAULT_MODELS_NORMAL)
        self.assertIn("gemini-3.8-flash", config.DEFAULT_MODELS_HIGH)

    def test_get_api_key_from_env(self):
        with patch.dict(os.environ, {"GEMINI_API_KEY": "test-env-key-1234567890"}):
            with patch("config.st", None):
                key = config.get_gemini_api_key()
                self.assertEqual(key, "test-env-key-1234567890")

    def test_validate_api_configuration_missing(self):
        with patch.dict(os.environ, {}, clear=True):
            with patch("config.get_gemini_api_key", return_value=""):
                is_valid, msg = config.validate_api_configuration()
                self.assertFalse(is_valid)
                self.assertIn("Chưa cấu hình GEMINI_API_KEY", msg)

    def test_validate_api_configuration_valid(self):
        with patch("config.get_gemini_api_key", return_value="AIzaSyValidDummyApiKey12345678"):
            is_valid, msg = config.validate_api_configuration()
            self.assertTrue(is_valid)
            self.assertIn("hợp lệ", msg)


if __name__ == "__main__":
    unittest.main()
