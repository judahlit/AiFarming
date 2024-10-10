import data as d
import click
import numpy as np
import pandas as pd

@click.command()
@click.option(
    '--file_path',
    required=True,
    type=str,
    help='path to the csv file'
    )
def main(file_path):
    bloodData = d.BloodSamplingData(file_path)
    
    print(bloodData.meta.company_name)    
    
if __name__ == "__main__":
    main()