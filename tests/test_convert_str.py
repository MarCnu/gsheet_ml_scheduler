import unittest

from gsheets_ml_scheduler.scheduler import GSheetsMLScheduler

class TestConvertStr(unittest.TestCase):

    def test_convert_str_to_bool_int_float_str(self):
        self.assertEqual(GSheetsMLScheduler.convert_str_to_bool_int_float_str(""), "")

        self.assertEqual(GSheetsMLScheduler.convert_str_to_bool_int_float_str("TRUE"), True)
        self.assertEqual(GSheetsMLScheduler.convert_str_to_bool_int_float_str("True"), True)
        self.assertEqual(GSheetsMLScheduler.convert_str_to_bool_int_float_str("true"), True)

        self.assertEqual(GSheetsMLScheduler.convert_str_to_bool_int_float_str("FALSE"), False)
        self.assertEqual(GSheetsMLScheduler.convert_str_to_bool_int_float_str("False"), False)
        self.assertEqual(GSheetsMLScheduler.convert_str_to_bool_int_float_str("false"), False)

        self.assertEqual(GSheetsMLScheduler.convert_str_to_bool_int_float_str("42"), 42)
        self.assertEqual(GSheetsMLScheduler.convert_str_to_bool_int_float_str("0"), 0)
        self.assertEqual(GSheetsMLScheduler.convert_str_to_bool_int_float_str("-42"), -42)

        self.assertEqual(GSheetsMLScheduler.convert_str_to_bool_int_float_str("0.01"), 0.01)
        self.assertEqual(GSheetsMLScheduler.convert_str_to_bool_int_float_str(".01"), 0.01)
        self.assertEqual(GSheetsMLScheduler.convert_str_to_bool_int_float_str("0.0"), 0.0)
        self.assertEqual(GSheetsMLScheduler.convert_str_to_bool_int_float_str("-0.01"), -0.01)
        self.assertEqual(GSheetsMLScheduler.convert_str_to_bool_int_float_str("-2e-4"), -2e-4)
        self.assertEqual(GSheetsMLScheduler.convert_str_to_bool_int_float_str("-2E-4"), -2e-4)

        self.assertEqual(GSheetsMLScheduler.convert_str_to_bool_int_float_str("Whatever"), "Whatever")

    def test_convert_str_to_bool_int_float_str_type(self):
        self.assertIsInstance(GSheetsMLScheduler.convert_str_to_bool_int_float_str(""), str)

        self.assertIsInstance(GSheetsMLScheduler.convert_str_to_bool_int_float_str("TRUE"), bool)
        self.assertIsInstance(GSheetsMLScheduler.convert_str_to_bool_int_float_str("True"), bool)
        self.assertIsInstance(GSheetsMLScheduler.convert_str_to_bool_int_float_str("true"), bool)

        self.assertIsInstance(GSheetsMLScheduler.convert_str_to_bool_int_float_str("FALSE"), bool)
        self.assertIsInstance(GSheetsMLScheduler.convert_str_to_bool_int_float_str("False"), bool)
        self.assertIsInstance(GSheetsMLScheduler.convert_str_to_bool_int_float_str("false"), bool)

        self.assertIsInstance(GSheetsMLScheduler.convert_str_to_bool_int_float_str("42"), int)
        self.assertIsInstance(GSheetsMLScheduler.convert_str_to_bool_int_float_str("0"), int)
        self.assertIsInstance(GSheetsMLScheduler.convert_str_to_bool_int_float_str("-42"), int)

        self.assertIsInstance(GSheetsMLScheduler.convert_str_to_bool_int_float_str("0.01"), float)
        self.assertIsInstance(GSheetsMLScheduler.convert_str_to_bool_int_float_str(".01"), float)
        self.assertIsInstance(GSheetsMLScheduler.convert_str_to_bool_int_float_str("0.0"), float)
        self.assertIsInstance(GSheetsMLScheduler.convert_str_to_bool_int_float_str("-0.01"), float)
        self.assertIsInstance(GSheetsMLScheduler.convert_str_to_bool_int_float_str("-2e-4"), float)
        self.assertIsInstance(GSheetsMLScheduler.convert_str_to_bool_int_float_str("-2E-4"), float)

        self.assertIsInstance(GSheetsMLScheduler.convert_str_to_bool_int_float_str("Whatever"), str)

if __name__ == '__main__':
    unittest.main()
