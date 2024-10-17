import pandas as pd


def load_blood_sampling_weeks(file_path: str) -> pd.DataFrame:
    _df = pd.read_excel(file_path)

    # get first column
    first_column = _df.columns[0]

    # look for the first row with blood sampling weeks based on the name of the first column
    skipped_rows = 0
    for i in range(50):  # 50 is an arbitrary number
        contents = _df[first_column][i]
        if contents == "Volgnr_V":
            skipped_rows = i
            break

    if skipped_rows == 0:
        raise ValueError("No blood sampling weeks found in the file")

    df = pd.read_excel(file_path, skiprows=skipped_rows)

    # name the columns based on the first row and remove it
    df.columns = df.iloc[0]
    df = df[1:]

    # remove rows with all NaN values for the "Volgnr_V" column
    df = df.dropna(subset=["Volgnr_V"])
    # remove rows that are a repeat of the volgnr_v column
    df = df[df["Volgnr_V"] != "Volgnr_V"]

    return df


 


# makes the data more readable by renaming the columns
def parse_blood_sampling_weeks(df: pd.DataFrame):
    column_mapping = {
        "Volgnr_V": "sequence_number",
        "EersteDier_V": "first_animal_V",  # not sure what this is
        "OnbekendDier_V": "unknown_animal_V",  # not sure what this is
        "Brokkalf_V": "Brokkalf_V",  # not sure what this is
        "ScanWerknr_V": "scan_work_number",  # don't know what this is
        "Bijspuiten_V": "injection",
        "ScanLand_ISO2Dier_V": "ear_tag_country",
        "ScanLevensnr_V": "ear_tag_number",
        "HbWaarde1_V": "hb_1",
        "HbWaarde2_V": "hb_2",
        "HbWaarde3_V": "hb_3",
        "HbWaarde4_V": "hb_4",
        "HbWaarde5_V": "hb_5",
        "SerumWaarde2_V": "serum_2",
        "SerumWaarde3_V": "serum_3",
        "SerumWaarde4_V": "serum_4",
        "SerumWaarde5_V": "serum_5",
        "Afdelingnr_V": "department_number",
        "DetailSoort_Omschr_V": "coat_color",
        "DetailSexe_BedrRegCode_V": "sex",
    }
    
    
    # add id column (ear tag number with country code)
    df["id"] = df["ScanLand_ISO2Dier_V"] + df["ScanLevensnr_V"]

    return df.rename(columns=column_mapping)


### Metadata Example:
# BedrijfRelatie_Naam_V                               Van Meel Mts.
# Koppelnr_V                                                2247366
# BedrijfRelatie_BezPostcodePlaats_V              4751SM Oud-Gastel
# Leeftijd_V                                                     22
# BedrijfRelatie_Telefoon1_V                                    NaN
# Metingnr_V                                                      4
# BedrijfRelatie_Mobiel_V                                       NaN
# HemaWeeknr_V                                                   22
# Datum_V                                       2023-12-05 00:00:00
# Tijd_V                                                   10:07:33
# Aant_V                                                         91
# IntegratieRelatie_Naam_V              Kalvermesterij Hooijer B.V.
def load_metadata(file_path: str):
    df = pd.read_excel(file_path)
    # name the columns based on the first row and remove it
    df.columns = df.iloc[0]
    df = df[1:]
    
    # remove everything except the first row
    df = df.iloc[0]
    
    barn_name = df["BedrijfRelatie_Naam_V"]
    link_number = df["Koppelnr_V"]
    company_location = df["BedrijfRelatie_BezPostcodePlaats_V"]
    week_number = df["Leeftijd_V"]
    measurement_number = df["Metingnr_V"]
    hematic_week_number = df["HemaWeeknr_V"]
    measurement_date = df["Datum_V"] # TODO: maybe combine date and time into one column
    measurement_time = df["Tijd_V"]
    # amount = df["Aant_V"] # not sure what this is
    company_name = df["IntegratieRelatie_Naam_V"]
    
    return Metadata({
        "barn_name": barn_name,
        "link_number": link_number,
        "company_location": company_location,
        "week_number": week_number,
        "measurement_number": measurement_number,
        "hematic_week_number": hematic_week_number,
        "measurement_date": measurement_date,
        "measurement_time": measurement_time,
        # "amount": amount,
        "company_name": company_name
    })

class Metadata:
    barn_name: str
    link_number: int
    company_location: str
    week_number: int
    measurement_number: int
    hematic_week_number: int
    measurement_date: str
    measurement_time: str
    # amount: int
    company_name: str
    
    
    def __init__(self, metadata_dict):
        self.barn_name = metadata_dict["barn_name"]
        self.link_number = metadata_dict["link_number"]
        self.company_location = metadata_dict["company_location"]
        self.week_number = metadata_dict["week_number"]
        self.measurement_number = metadata_dict["measurement_number"]
        self.hematic_week_number = metadata_dict["hematic_week_number"]
        self.measurement_date = metadata_dict["measurement_date"]
        self.measurement_time = metadata_dict["measurement_time"]
        # self.amount = metadata_dict["amount"]
        self.company_name = metadata_dict["company_name"]


class BloodSamplingData:
    df: pd.DataFrame
    meta: Metadata

    def __init__(self, file_path):
        self.df = parse_blood_sampling_weeks(load_blood_sampling_weeks(file_path))
        self.meta = load_metadata(file_path)
        
        # print('Successfully loaded blood sampling data')
        # print('rows:', len(self.df))
        # print('columns:', len(self.df.columns))


