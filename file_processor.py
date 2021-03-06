import pandas as pd

# Expected column headers that will be used
ZIP_CODE = 'zipcode'
RATE_AREA = 'rate_area'
STATE = 'state'
COUNTY_CODE = 'county_code'
METAL_LEVEL = 'metal_level'
RATE_VALUE = 'rate'

# New columns added to dataframes
RATE_AREA_NAME = 'rate_area_name'

# Metal identifier in csv that indicates silver plans
SILVER_IDENTIFIER = 'Silver'
RANK_COL = 'group_rank'

# File locations
PLAN_FILE = 'data/plans.csv'
ZIP_FILE = 'data/zips.csv'
INPUT_FILE = 'data/slcsp.csv'

def get_rate_area_name(df):
    """
    Standard function to combine state and rate area columns to
    :param df:
    :return:
    """

    return df['state'] + '-' + df['rate_area']


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

class FileProcessor:

    def __init__(self, plan_file_path=PLAN_FILE, rate_area_lookup_path=ZIP_FILE):

        self.rate_code_lookup = self.get_rate_code_lookup(rate_area_lookup_path)
        self.second_lowest_cost_lookup = self.get_second_lowest_cost_lookup(plan_file_path)

    @staticmethod
    def get_rate_code_lookup(rate_code_lookup_path):
        """
        Reads CSV that includes zipcode, rate_area, county_code and state and returns a dictionary mapping zip codes
        to rate areas. Multiple instances of the same zip code in one rate area is permitted due to duplicates from
        zip codes in multiple counties, multiple rate areas for the same zip code are not permitted and that zip code
        will not be added to the returned dictionary
        :param rate_code_lookup_path: path to file with a header row including zipcode, rate_area, county_code and state
        :return: <dict> with entries of key: zipcode, value: rate area with rate area formatted as State abbreviation-
        rate area number, eg. (AK-1).
        """

        # Convert zip codes and other codes to strings to have them format correctly and not drop leading zeros
        rate_area_df = pd.read_csv(rate_code_lookup_path, dtype={ZIP_CODE: 'str', RATE_AREA: 'str', COUNTY_CODE: 'str'})

        # Set single name for a rate area
        rate_area_df[RATE_AREA_NAME] = get_rate_area_name(rate_area_df)

        # Remove rows where county different but zip and rate area are the same, this arbitrarily keeps the first row
        # but for the purposes of the lookup they are the same

        deduped_df = rate_area_df.drop_duplicates(subset=[ZIP_CODE, RATE_AREA_NAME], keep='first')

        # Drop all ambiguous zip codes with multiple rows
        deduped_rate_area_df = deduped_df.drop_duplicates(subset=ZIP_CODE, keep=False)

        # Convert dataframe to dictionary with zipcode as a key and rate area name as a value
        zip_to_rate_lookup = deduped_rate_area_df.set_index(ZIP_CODE)[RATE_AREA_NAME].to_dict()

        return zip_to_rate_lookup

    @staticmethod
    def get_second_lowest_cost_lookup(plan_file_path):
        """
        Reads in CSV from plan_file_path containing plan information and returns a dictionary that looks up the second
        lowest cost silver plan in every rate area.
        :param plan_file_path: <string> file path to CSV that has a header that includes metal_level, state, rate_area and rate
        :return: <dict> with keys of rate areas formatted as State abbreviation-rate area number, eg. (AK-1) and values
        as the second lowest silver rates as floats.
        """
        plan_df = pd.read_csv(plan_file_path, dtype={RATE_AREA: 'str'})

        # Add column for rate area name
        plan_df[RATE_AREA_NAME] = get_rate_area_name(plan_df)

        # Drop all non-silver plans
        silver_df = plan_df.loc[plan_df[METAL_LEVEL] == SILVER_IDENTIFIER].copy()

        # Group all the silver plans by their rate area and create a new column that ranks them from lowest to highest
        # Plans with the same rate will be assigned ranks based on their order in the dataframe (method='first'
        # specifies this logic).
        silver_df[RANK_COL] = silver_df.groupby(by=RATE_AREA_NAME)[RATE_VALUE].rank(method='dense')

        # Only keep plans that have the second lowest cost in the group. (in some cases this may return the lowest cost
        # plan if there are two plans with the same cost that is also the lowest.
        second_lowest_df = silver_df[silver_df[RANK_COL] == 2].copy()

        # Convert dataframe to dictionary that is keyed with the rate area name and has the value as the second lowest
        # rate as those are the only rates that remain in the dataframe.
        area_to_rate_lookup = second_lowest_df.set_index(RATE_AREA_NAME)[RATE_VALUE].to_dict()

        return area_to_rate_lookup

    def process_zip_code(self, zip_code):
        """
        Looks up rate area and associated second lowest silver plan cost for the provided zip code and prints the
        results to stdout with the proper formatting.
        :param zip_code: <string> Assumed 5 digit zip code that is potentially in the rate area lookup
        :return: None, prints row to screen
        """

        # Get rate area from rate area lookup if it exists
        rate_area = self.rate_code_lookup.get(zip_code)

        # Get second lowest silver plan cost from lookup, or None if it does not exist
        rate = self.second_lowest_cost_lookup.get(rate_area) if rate_area else None

        formatted_string = formatted_print(zip_code, rate)
        # Process zip code will be called in a loop so each instance will print on a new line
        print(formatted_string)


if __name__ == '__main__':

    # Initialize file processor with files to create rate
    file_processor = FileProcessor(rate_area_lookup_path=ZIP_FILE, plan_file_path=PLAN_FILE)

    # Print headers

    with open(INPUT_FILE,'r') as f:
        lines = f.readlines()
        print(f"{ZIP_CODE},{RATE_VALUE}")
        # Skip header
        for line in lines[1:]:
            # Zip code should be the first item in the comma separated list
            zip_code = line.split(',')[0]
            file_processor.process_zip_code(zip_code)

