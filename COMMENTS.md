# second-lowest-silver

## Installation instructions

This code can be run in a Python 3.6 environment with the packages in requirements.txt installed. The steps below will set up a fresh virtual environment with the appropriate packages. 

- Run `virtualenv "venv" --python=python3` in repository base folder to create a virtual environment to run the code in.
  - To install virtualenv on your machine follow these [virtualenv installation instructions.](https://virtualenv.pypa.io/en/latest/installation/) 
- Run `source venv/bin/activate` to activate the virtual environment (All other commands assume the user is in this virtual environment)
- Install packages by running `pip3 install -r requirements.txt`

## Testing instructions

Tests are written in `test_suite.py` and some refer to `data/test_plans.csv` which is included in the repository.

Tests can be run by calling `pytest test_suite.py` in the base folder of the repository.

## Running instructions

To run the main file call `python3 file_processor.py` from the command line.

### Logic assumptions

- If two silver plans had the same costs as each other and the lowest cost in their rate area, I assumed that cost was considered the second lowest cost silver plan.
