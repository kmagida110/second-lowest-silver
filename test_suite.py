import unittest
import pandas as pd
from file_processor import formatted_print

TEST_PLAN_FILE = 'data/test_plans.csv'


class TestSuite(unittest.TestCase):

    @unittest.skip("Skip until function is set")
    def test_find_second_lowest(self):
        """
        Test whether the find second lowest function works on a small set of test data
        """

        sample_df = pd.read_csv(TEST_PLAN_FILE)

        expected_result = {}

        # Check that the two region that should have second best rates are included and correct
        self.assertEqual(expected_result['GA-7'], 300.62)
        self.assertEqual(expected_result['MI-4'], 150.6767)

        # Check that only one silver isn't added to the final dictionary
        self.assertNotIn('FL-60', expected_result)

        # Check that no silver plan is not added to the final dictionary
        self.assertNotIn('IL-5', expected_result)

    def test_proper_output(self):
        """
        Test whether the format to print function returns the correct string to print
        :return:
        """

        # Check the standard input prints appropriately
        full_print = formatted_print('01234', 100.19)
        self.assertEqual("01234,100.19", full_print)

        # Check the floats are truncated properly
        trunc_print = formatted_print('12345', 123.45678)
        self.assertEqual('12345,123.46',trunc_print)

        # Check that no rate passed prints none
        null_print = formatted_print('54321', None)
        self.assertEqual('54321,', null_print)


if __name__ == "__main__":
    unittest.main()
