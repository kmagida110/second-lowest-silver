import pandas as pd


class FileProcessor:

    def __init__(self, plan_file_path, rate_area_lookup_path):

        self.rate_code_lookup = self.get_rate_code_lookup(rate_area_lookup_path)

    @staticmethod
    def get_rate_code_lookup(rate_code_lookup_path):

        # Convert zip codes and other codes to strings to have them format correctly and not drop leading zeros
        rate_df = pd.read_csv(rate_code_lookup_path, dtype={'zipcode': 'str', 'rate_area': 'str', 'county_code': 'str'})


def formatted_print(zip_code, rate):
    """
    Returns formatted string for printing to stdout to conform with the requirements with two decimal places on the rate
    and the full zip code separated by a comma. Null rates should not print anything following the comma.
    :param zip_code: <string> zip code
    :param rate: <float> rate with unrounded
    :return:
    """
    rate_string = f"{rate:.2f}" if rate else ''
    return f"{zip_code},{rate_string}"


