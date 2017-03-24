from __future__ import print_function
from colorama import Fore
import pandas as pd
import functools
import sys


def parse_agreements(agreements):
    """countriesagreements.csv file has duplicated countries, as the same country
    can have multiple agreements. This function looks for those cases, and, if it
    finds them, it joins the agreements into a single string, seperated with a '+'
    It then returns a new dataframe, ready to be joined to others.
    """
    agreements.index = agreements.country
    trade_agreements = []
    unique_countries = set(agreements.country.values)
    for place in sorted(unique_countries):
        tmp_values = agreements.international_agreements[place]
        if type(tmp_values) is not str:
            # if multiple entries, the value will be a np-type array, not string
            joined_strings = '+'.join(list(tmp_values.values))
            #print(f'{place}: {joined_strings}')
            trade_agreements.append([place, joined_strings])
        else:
            # if a single entry, the value will be a string
            trade_agreements.append([place, tmp_values])
    processed = pd.DataFrame(trade_agreements, columns=['country','international_agreements'])
    return processed


def main(flist, output_filename):
    """Given csv input files, combine the data into a single table, with country appearing
    once only.
    """
    dfs = []
    for file in flist:
        print('Reading {0}'.format(file))
        tmp = pd.read_csv(file)
        tmp = tmp.drop('id', axis=1)
        if 'international_agreements' in tmp.columns:
            print('    found international agreements file: Combining per-country agreements.')
            tmp = parse_agreements(tmp)
        dfs.append(tmp)
    df_final = functools.reduce(lambda left, right: pd.merge(left, right, on='country'), dfs)
    df_final.to_csv(output_filename, index=False)
    return


if __name__ == "__main__":
    assert len(sys.argv) > 1,'Pass a list of csv files, .e.g. python generate_clean_file.py *.csv'
    flist = sys.argv[1:]
    # Check that only csv files were passed
    for item in flist:
        if item.split('.')[-1] != 'csv':
            print('{0} is not a csv file: excluding it.'.format(item))
            flist.remove(item)
    output_filename = 'output.csv'
    # If this has been run before, output might be accidentally included. Remove that too.
    if output_filename in flist:
        flist.remove(output_filename)
    print("Combining data from: {0} --> {1}".format(flist, output_filename)) 
    main(flist, output_filename)
    print(Fore.GREEN + "Sucsessfully created {0}. Normal end of program".format(output_filename))