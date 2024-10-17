import pandas as pd

def parse_slaughter_data_xlsx(df: pd.DataFrame):
    # remove nan columns
    df = df.dropna(axis=1, how='all')
    # remove all rows that are completely empty
    df = df.dropna(axis=0, how='all')
    
    # name the columns based on the first row and remove it
    df.columns = df.iloc[0]
    df = df[1:]
    
    # Diernr HB 1 Hb 2
    column_mapping = {
        "Diernr": "ear_tag_number",
        "HB 1": "HB_1",
        "HB 2": "HB_2",
        "Hb 1": "HB_1", # the excel files have inconsistent column names
        "Hb 2": "HB_2",
    }
    
    df = df.rename(columns=column_mapping)
    
    df["id"] = df["ear_tag_number"].str.replace(" ", "")
    
    
    return df

def parse_slaughter_data_xls(df: pd.DataFrame):
    # remove nan columns
    df = df.dropna(axis=1, how='all')
    
    # name the columns based on the first row and remove it
    df.columns = df.iloc[0]
    df = df[1:]
    
    # remove newline characters from column names
    df.columns = df.columns.str.replace("\n", "")
    
    
    # 	ID nummer	WerkNr	#	Gewicht	Soort	Kleur	Vet	Geboortedatum	Leeftijdscode	Sekse	...	Nieren	Lever	Kalf	Overziener	Antibiotica	Bacteriologie	Prostaat	Spuitnek	Spuitborst	Slacht Datum
    column_mapping = {
        "ID nummer": "ear_tag_number",
        "WerkNr": "work_number", # not sure what this is
        "Gewicht": "weight",
        "Soort": "type",
        "Kleur": "color",
        "Vet": "fat",
        "Geboortedatum": "birth_date",
        "Leeftijdscode": "age_code",
        "Sexe": "sex",
        "Nieren": "kidneys",
        "Lever": "liver",
        "Kalf": "calf", # not sure what this is
        "Overziener": "overseer", # not sure what this is
        "Antibiotica": "antibiotics",
        "Bacteriologie": "bacteriology",
        "Prostaat": "prostate", # Whaaaaat?
        "Spuitnek": "injection_neck", # not sure what this is
        "Spuitborst": "injection_chest", # not sure what this is
        "Slacht Datum": "slaughter_date"
    }
    
    df = df.rename(columns=column_mapping)
    
    
    # calculate the age of the animal based on the slaughter date and the birth date
    df["birth_date"] = pd.to_datetime(df["birth_date"], format="%d-%m-%Y")
    df["slaughter_date"] = pd.to_datetime(df["slaughter_date"], format="%d-%m-%Y")
    
    df["lifetime_in_days"] = (df["slaughter_date"] - df["birth_date"]).dt.days
    
    df["id"] = df["ear_tag_number"].str.replace(" ", "")
    
    return df
    


# makes the data more readable by renaming the columns
def parse_slaughter_data_csv(df: pd.DataFrame):
#	Volgnr.	Koppel	Land en IDcode	Type	Vetbedekking	Kleur	Sexe	Gewicht	Correctie	UBN	Geboorte datum	Slacht datum	Huisvesting	Categorie	Afwijkingen
    column_mapping = {
        "Volgnr.": "sequence_number",
        "Koppel": "couple", # not sure what this is
        "Land en IDcode": "ear_tag_number_full",
        "type": "blood_type", # I think it's blood type but not sure
        "Vetbedekking": "fat_cover",
        "Kleur": "color",
        "Sexe": "sex",
        "Gewicht": "weight",
        "Correctie": "correction", # not sure what this is
        "UBN": "UBN", # not sure what this is probably some company number
        "Geboorte datum": "birth_date",
        "Slacht datum": "slaughter_date",
        "Huisvesting": "housing", # not sure what this is
        "Categorie": "category", # not sure what this is
        "Afwijkingen": "deviations" # not sure what this is 
    }
    df = df.rename(columns=column_mapping)
    
    # calculate the age of the animal
    df["birth_date"] = pd.to_datetime(df["birth_date"], format="%d-%m-%Y")
    df["slaughter_date"] = pd.to_datetime(df["slaughter_date"], format="%d-%m-%Y")
    
    # add the cow_id column (ear tag number without spaces)
    df["id"] = df["ear_tag_number_full"].str.replace(" ", "")
    
    df["lifetime_in_days"] = (df["slaughter_date"] - df["birth_date"]).dt.days
    
    return df

class SlaughterData:
    df: pd.DataFrame

    def __init__(self, file_path):
        try: 
            if file_path.endswith('.csv'):
                self.df = parse_slaughter_data_csv(pd.read_csv(file_path, sep=";", encoding="latin1"))
            elif file_path.endswith('.xls'):
                self.df = parse_slaughter_data_xls(pd.read_excel(file_path))
            elif file_path.endswith('.xlsx'):
                self.df = parse_slaughter_data_xlsx(pd.read_excel(file_path))
            else:
                raise ValueError("File type not supported")
            
            self.df = self.df[self.df["id"].notna()]
            
        except Exception as e:
            # print("Error loading file", file_path)
            self.error = {
                "file_path": file_path,
                "error": e
            }
            # raise e
            self.df = None

if __name__ == "__main__":
    slaughter_data = SlaughterData("/home/teunm/git/school/ai-farming-python-app/sample_files/HB uitslag bult 4.xlsx")
    print(slaughter_data.df.head())
