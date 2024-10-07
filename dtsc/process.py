import pandas as pd
from sklearn.preprocessing import StandardScaler


def reduce_dimensions(data:pd.DataFrame):
    print("###  Dimension reduce process ###")
    print("Trying to remove redundant information like translation after verification")
    print('Differents regions :')
    print(data["Région"].unique())
    print(data["Région.1"].unique())
    print(data["Région.2"].unique())
    print('')

    print('Differents types :')
    print(data["Type de voie"].unique())
    print(data["Type de voie NL"].unique())
    print(data["Type de voie EN"].unique())
    print('')
    
    return data.drop(columns= ["Région","Région.1", "Type de voie", "Type de voie NL"]) 

def rename_columns(data:pd.DataFrame):
    return data.rename(columns={
                        "Année":"Year",
                        "Région.2": "Region", 
                        "Type de voie EN": "TrackCat",
                        "Kilomètres de voie":"Kilometer",
                        "Nombre d'appareils de voie":"Devices"
                        })


def apply_data_type(data:pd.DataFrame):
    data['Kilometer'] = pd.to_numeric(data['Kilometer'])
    data['Devices'] = pd.to_numeric(data['Devices'])
    data['Year'] = pd.to_numeric(data['Year'],downcast="integer")
    return data

def check_data_integrity(data:pd.DataFrame) -> None:
    print("Duplicated rows : ", data.duplicated().sum())
    print("Missing values : ",sum(data.isna().sum()))


def normalize_distinctly(data: pd.DataFrame, year:bool=False):
    columns_to_normalize = ['Kilometer', 'Devices']
    if year:
        columns_to_normalize.append('Year')
        
    normalized_data = pd.DataFrame()

    for (region, trackcat), group in data.groupby(['Region', 'TrackCat']):
        group_copy = group.copy()
        scaler = StandardScaler()
        group_copy[columns_to_normalize] = scaler.fit_transform(group_copy[columns_to_normalize])
        normalized_data = pd.concat([normalized_data, group_copy], ignore_index=True)

    return normalized_data


    