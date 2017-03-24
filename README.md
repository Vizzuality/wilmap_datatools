## WIL MAP data prep

[![license](https://img.shields.io/github/license/mashape/apistatus.svg)]()

Simple data preparation script for WILMAP csv data. Designed to read in multiple csv files, all containing a column named country, and combine the data together. It should have only one row per country. Therefore files with
multiple rows for the same country should have their data collapsed to a single column before combination. Currently this is done by creating a string separated by `+` symbols.

## Requirements

* Python 2.7 or 3


## Instructions

Download this repo, and `cd` to folder. Install the required Python libraries via the below command:

```bash
pip install -r requirements.txt
```

Assuming the target csv data are stored in the subfolder `input_data`, the script could then be run as follows:

```bash
python generate_clean_file.py input_data/*.csv
```

This should result in the creation of `output.csv` in the local directory.
