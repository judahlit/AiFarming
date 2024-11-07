from . import data

import click
import numpy as np
import pandas as pd
import zipfile
import os

from .database import db


# from typing import List

@click.group()
def cli():
    pass

@cli.command()
@click.argument('blood_sampling_directory')
@click.argument('slaughter_directory')
def parse_all(blood_sampling_directory, slaughter_directory):
    
    blood_sampling_data_files: list[data.BloodSamplingData] = []
    
    for item in os.listdir(blood_sampling_directory):
        datafile = data.BloodSamplingData(os.path.join(blood_sampling_directory, item))
        blood_sampling_data_files.append(datafile)
    
    print('Successfully loaded blood sampling data')
    
    
    # slaughter data can come in 3 different formats, xls, csv and xlsx for the hb values
    slaughter_data_files_xls: list[data.SlaughterData] = []
    slaughter_data_files_csv: list[data.SlaughterData] = []
    slaughter_data_files_xlsx: list[data.SlaughterData] = []
    
    # go through subdirectories too 
    for root, dirs, files in os.walk(slaughter_directory):
        for file in files:
            if file.endswith('.xls'):
                slaughter_data_files_xls.append(data.SlaughterData(os.path.join(root, file)))
            elif file.endswith('.csv'):
                slaughter_data_files_csv.append(data.SlaughterData(os.path.join(root, file)))
            elif file.endswith('.xlsx'):
                slaughter_data_files_xlsx.append(data.SlaughterData(os.path.join(root, file)))
            else:
                print('Unknown file format:', file)
                
    # filter out slaughter data files that have no data (slaughter data is very messy)
    slaughter_data_files_xls = [file for file in slaughter_data_files_xls if not file.df is None]
    slaughter_data_files_csv = [file for file in slaughter_data_files_csv if not file.df is None]
    slaughter_data_files_xlsx = [file for file in slaughter_data_files_xlsx if not file.df is None]
    
    print('Successfully loaded slaughter data files xlsx:', len(slaughter_data_files_xlsx), 'csv:', len(slaughter_data_files_csv), 'xls:', len(slaughter_data_files_xls))
    
    # db
    db.build_tables()
    
    # insert blood sampling data
    for datafile in blood_sampling_data_files:
        for index, row in datafile.df.iterrows():
            db.insert_blood_sampling_data(
                row['id'],
                row['country'],
                row['coat_color'],
                row['hb_1'],
                row['hb_2'],
                row['hb_3'],
                row['hb_4']
            )
            
    # insert slaughter data
    # TODO
    
    for datafile in slaughter_data_files_xls:
        for index, row in datafile.df.iterrows():
            db.insert_slaughter_data(
                row['id'],
                row['birth_date'],
                row['slaughter_date'],
                row['lifetime_in_days'],
                row['weight']
            )
    
    for datafile in slaughter_data_files_csv:
        for index, row in datafile.df.iterrows():
            db.insert_slaughter_data(
                row['id'],
                row['birth_date'],
                row['slaughter_date'],
                row['lifetime_in_days'],
                row['weight']
            )
    
    
    db.commit()
    
    
    
    
    
    
            
        
    
    
    
    
    
@cli.command()
@click.argument('source_directory')
@click.argument('destination_directory')
def unzip_slaughter(source_directory, destination_directory):
    """
    Unzips all the data files in the given directory.
    """

    for item in os.listdir(source_directory):
        if item.endswith('.zip'):
            try:
                with zipfile.ZipFile(os.path.join(source_directory, item), 'r') as zip_ref:
                    zip_ref.extractall(destination_directory)
                    print('Extracted:', item)
            except zipfile.BadZipFile:
                print('Bad zip file:', item)
                continue
    
    
    

if __name__ == '__main__':
    cli()