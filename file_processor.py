import pandas as pd

class FileProcessor:

    def __init__(self, plan_file_path, rate_area_lookup_path):

        self.rate_code_lookup = self.get_rate_code_lookup(rate_area_lookup_path)

    @staticmethod
    def get_rate_code_lookup(rate_code_lookup_path):

        # Convert zip codes and other codes to strings to have them format correctly and not drop leading zeros
        rate_df = pd.read_csv(rate_code_lookup_path, dtype={'zipcode': 'str', 'rate_area': 'str', 'county_code': 'str'})

        # Set single name for a rate area
        rate_df['rate_area_name'] = rate_df['state'] + '-' + rate_df['rate_area']

        # Remove rows where county different but zip and rate area are the same, this arbitrarily keeps the first row
        # but for the purposes of the lookup they are the same

        deduped_df = rate_df.drop_duplicates(subset=['zipcode', 'rate_area_name'], keep='first')

        # Drop all ambiguous zip codes with multiple rows
        deduped_rate_df = deduped_df.drop_duplicates(subset='zipcode', keep=False)

        # Convert dataframe to dictionary with zipcode as a key and rate area name as a value
        zip_to_rate_lookup = deduped_rate_df.set_index('zipcode')['rate_area_name'].to_dict()

        return zip_to_rate_lookup






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


