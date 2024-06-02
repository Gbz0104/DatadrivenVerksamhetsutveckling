import pandas as pd
import re
from ast import literal_eval

def extract_label_from_occupation(occupation):
    try:
        # Omvandla strängen till ett Python-objekt
        occupation_data = literal_eval(occupation)
        # Gå igenom listan av dictionaries (om det är en lista)
        if isinstance(occupation_data, list):
            for item in occupation_data:
                if 'label' in item:
                    return item['label']
    except ValueError as ve:
        print(f"ValueError: {ve} for input: {occupation}")
    except Exception as e:
        print(f"Error: {e} for input: {occupation}")
    return None

# Ladda in data
file_path = '/Users/svenhammarberg/Desktop/2023 enkel/rensad_occupasion_field_v2.csv'
data = pd.read_csv(file_path)

# Applicera funktionen på 'occupation' kolumnen
data['occupation'] = data['occupation'].apply(extract_label_from_occupation)

# Skriv ut de första raderna av resultatet för att verifiera
print("Processed 'occupation' values:", data['occupation'].head())

# Spara den bearbetade DataFrame till en ny CSV-fil
output_path = '/Users/svenhammarberg/Desktop/2023 enkel/rensad_occupasion_field&occupasion_v2.csv'
data.to_csv(output_path, index=False)
