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
    df = pd.read_csv(file_path)
    print(df.shape)

if __name__ == "__main__":
    main()