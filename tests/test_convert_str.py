import unittest

from gsheet_ml_scheduler.scheduler import GSheetMLScheduler

class TestConvertStr(unittest.TestCase):

    def test_convert_str_to_bool_int_float_str(self):
        self.assertEqual(GSheetMLScheduler.convert_str_to_bool_int_float_str(""), "")

        self.assertEqual(GSheetMLScheduler.convert_str_to_bool_int_float_str("TRUE"), True)
        self.assertEqual(GSheetMLScheduler.convert_str_to_bool_int_float_str("True"), True)
        self.assertEqual(GSheetMLScheduler.convert_str_to_bool_int_float_str("true"), True)

        self.assertEqual(GSheetMLScheduler.convert_str_to_bool_int_float_str("FALSE"), False)
        self.assertEqual(GSheetMLScheduler.convert_str_to_bool_int_float_str("False"), False)
        self.assertEqual(GSheetMLScheduler.convert_str_to_bool_int_float_str("false"), False)

        self.assertEqual(GSheetMLScheduler.convert_str_to_bool_int_float_str("42"), 42)
        self.assertEqual(GSheetMLScheduler.convert_str_to_bool_int_float_str("0"), 0)
        self.assertEqual(GSheetMLScheduler.convert_str_to_bool_int_float_str("-42"), -42)

        self.assertEqual(GSheetMLScheduler.convert_str_to_bool_int_float_str("0.01"), 0.01)
        self.assertEqual(GSheetMLScheduler.convert_str_to_bool_int_float_str(".01"), 0.01)
        self.assertEqual(GSheetMLScheduler.convert_str_to_bool_int_float_str("0.0"), 0.0)
        self.assertEqual(GSheetMLScheduler.convert_str_to_bool_int_float_str("-0.01"), -0.01)
        self.assertEqual(GSheetMLScheduler.convert_str_to_bool_int_float_str("-2e-4"), -2e-4)
        self.assertEqual(GSheetMLScheduler.convert_str_to_bool_int_float_str("-2E-4"), -2e-4)

        self.assertEqual(GSheetMLScheduler.convert_str_to_bool_int_float_str("Whatever"), "Whatever")

if __name__ == '__main__':
    unittest.main()
