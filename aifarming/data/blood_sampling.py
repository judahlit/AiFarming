import re
import pandas as pd


def load_blood_sampling_weeks(file_path: str) -> pd.DataFrame:
    _df = pd.read_excel(file_path)

    # get first column
    first_column = _df.columns[0]

    # look for the first row with blood sampling weeks based on the name of the first column
    skipped_rows = 0
    for i in range(50):  # 50 is an arbitrary number
        contents = _df[first_column][i]
        if contents == "Land":
            skipped_rows = i
            break

    if skipped_rows == 0:
        raise ValueError("No blood sampling weeks found in the file")

    df = pd.read_excel(file_path, skiprows=skipped_rows)

    # name the columns based on the first row and remove it
    df.columns = df.iloc[0]
    df = df[1:]

    # remove rows with all NaN values for the "Land" column
    df = df.dropna(subset=["Land"])
    # remove rows that are a repeat of the Land column
    df = df[df["Land"] != "Land"]

    return df


# makes the data more readable by renaming the columns
def parse_blood_sampling_weeks(df: pd.DataFrame):
    column_mapping = {
        "Land": "country",
        "Haarkleur": "coat_color",
    }
    df = df.rename(columns=column_mapping)
    
    df, levensnr_column = find_column_and_convert(df, "levensnr")
    df["id"] = df["country"] + df[levensnr_column]

    df = find_and_rename_hb_columns(df)
    return df


def find_and_rename_hb_columns(df: pd.DataFrame):
    # Column names match the regex if they start with "hb" followed by a number
    pattern = re.compile(r"hb.*?(\d+)", re.IGNORECASE)
    matching_columns = [col for col in df.columns if pattern.search(col)]
    
    # Extract the number and sort by it
    sorted_columns = sorted(matching_columns, key=lambda col: int(pattern.search(col).group(1)))

    # Rename columns and add them to the DataFrame
    for col in sorted_columns:
        number = pattern.search(col).group(1)
        new_col_name = f"hb_{number}"
        df[new_col_name] = df[col]
        df = df.drop(columns=col)
    
    return df


def find_column_and_convert(df: pd.DataFrame, search: str):
    column = next((col for col in df.columns if search in col.lower()), None)

    if not column:
        raise ValueError("No column containing " + search + " found in the data")
    
    df[column] = df[column].apply(lambda x: str(x))

    return (df, column)


def load_metadata(file_path: str):
    df = pd.read_excel(file_path)

    company_name = df.iat[2, 2]
    company_location = df.iat[3, 2]
    phone_number = df.iat[4, 2]
    mobile_phone_number = df.iat[5, 2]
    measurement_datetime = df.iat[6, 2]
    integration_name = df.iat[7, 2]
    link_number = df.iat[2, 9]
    week_number = df.iat[3, 9]
    measurement_number = df.iat[4, 9]
    hematic_week_number = df.iat[5, 9]
    amount = df.iat[6, 9]
    
    return Metadata({
        "company_name": company_name,
        "phone_number": phone_number,
        "mobile_phone_number": mobile_phone_number,
        "link_number": link_number,
        "company_location": company_location,
        "week_number": week_number,
        "measurement_number": measurement_number,
        "hematic_week_number": hematic_week_number,
        "measurement_datetime": measurement_datetime,
        "amount": amount,
        "integration_name": integration_name
    })

class Metadata:
    company_name: str
    phone_number: str
    mobile_phone_number: str
    link_number: int
    company_location: str
    week_number: int
    measurement_number: int
    hematic_week_number: int
    measurement_datetime: str
    amount: int
    integration_name: str
    
    
    def __init__(self, metadata_dict):
        self.company_name = metadata_dict["company_name"]
        self.phone_number = metadata_dict["phone_number"]
        self.mobile_phone_number = metadata_dict["mobile_phone_number"]
        self.link_number = metadata_dict["link_number"]
        self.company_location = metadata_dict["company_location"]
        self.week_number = metadata_dict["week_number"]
        self.measurement_number = metadata_dict["measurement_number"]
        self.hematic_week_number = metadata_dict["hematic_week_number"]
        self.measurement_datetime = metadata_dict["measurement_datetime"]
        self.amount = metadata_dict["amount"]
        self.integration_name = metadata_dict["integration_name"]


class BloodSamplingData:
    df: pd.DataFrame
    meta: Metadata

    def __init__(self, file_path):
        self.df = parse_blood_sampling_weeks(load_blood_sampling_weeks(file_path))
        self.meta = load_metadata(file_path)
        
        # print('Successfully loaded blood sampling data')
        # print('rows:', len(self.df))
        # print('columns:', len(self.df.columns))
        # print('metadata:', self.meta.__dict__)