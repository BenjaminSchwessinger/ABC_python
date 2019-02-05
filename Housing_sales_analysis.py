# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import argparse
import pandas as pd
import seaborn as sns
import datetime as dt
import os
import warnings


def gen_argparser():
    """Defines the arguments of the program.
    """
    program_description = """This is a program that reads a housing dataset.
    Does some summary statisctics and plots. These are printed for the 
    statistics and saved in both cases."""
    parser = argparse.ArgumentParser(description=program_description)
    parser.add_argument('CSV_FN',
    help='File name for housing date file to be be analyzed. Should be in CSV')
    parser.add_argument('--plotting_style',
    help='Plottings style for plotting https://matplotlib.org/gallery/style_sheets/style_sheets_reference.html')
    args = parser.parse_args()
    return args


def read_csv_proper(filename):
    """Reads the csv file in and returns a dataframe."""
    df = pd.read_csv(filename, 
                    usecols=['id','date','price','zipcode','lat','long', 'bedrooms',
                             'waterfront','view','grade','sqft_living','sqft_lot'],
                    parse_dates=['date'], 
                    dtype={'zipcode': 'category',
                           'waterfront': 'bool'})
    return df

def generate_out_folder(filename):
    """Generate a timestamped outfolder to save things in and return its name."""
    outf_suffix = dt.datetime.utcnow().strftime("%d_%b_%Y_%Ih_%Mmin_%Ssec")
    out_folder = os.path.join(os.path.dirname(filename), outf_suffix)
    if not os.path.exists(out_folder):
        os.mkdir(out_folder)
    return out_folder

def generate_and_save_lmplot(df, outf):
    """Generate a limplot and save it out."""
    sns_fig = sns.lmplot(data=df, x='sqft_living', y='price', hue='waterfront')
    sns_fig.savefig(outf, dpi=600)
    
def main():
    """Does all the heavy lifting."""
    warnings.filterwarnings("ignore")
    args = gen_argparser()
    filename = os.path.abspath(args.CSV_FN)
    out_folder = generate_out_folder(filename)
    summary_outfile_name = os.path.join(out_folder,\
                os.path.basename(filename).replace('.csv', '_summary.csv'))
    df = read_csv_proper(filename)
    df.describe().loc[:, 'price'].to_csv(summary_outfile_name)
    plot_outflie_name = os.path.join(out_folder,\
                os.path.basename(filename).\
                replace('.csv', '.lmplot.png'))
    generate_and_save_lmplot(df, plot_outflie_name)
    print("All Done!")


if __name__ == '__main__':
    main()
    
    
    