import pandas as pd
import json

# Ange sökvägen till din textfil
file_path = 'Documents/Datadriven Verksamhetsutveckling/jsonl.2023.txt'
data = []

with open(file_path, 'r', encoding='utf-8') as file:
    for line_number, line in enumerate(file, start=1):
        try:
            # Kontrollera att raden inte är tom och ser ut att vara JSON
            if line.strip():  # Kontrollerar att raden inte bara innehåller whitespace
                data.append(json.loads(line))
            else:
                print(f"Tom eller ogiltig rad på rad {line_number} ignoreras.")
        except json.JSONDecodeError as e:
            print(f"JSON-dekoderingsfel på rad {line_number}: {e}")

# Konvertera listan av dictionaries till ett pandas DataFrame
df = pd.DataFrame(data)

# Spara DataFrame till en Excel-fil
excel_path = 'Desktop/2023 till excel.xlsx'
df.to_excel(excel_path, index=False, engine='openpyxl')

print("Data har sparats till Excel!")
print(f"Totalt {len(data)} poster har behandlats.")
