import pandas as pd

# Ladda in den befintliga CSV-filen
data = pd.read_csv('/Users/svenhammarberg/Desktop/2023 enkel/all_data.csv')

# Skriv ut kolumnnamnen för att säkerställa att 'occupation_field' finns och är korrekt stavat
print(data.columns)

# Nyckelord för att identifiera byggbranschen
construction_keywords = [
    'bygg', 'konstruktion', 'arkitektur', 'renovering', 'anläggning',
    'infrastruktur', 'byggprojektledning', 'fastighetsutveckling', 'vvs',
    'elinstallation', 'markarbete', 'betongarbete', 'takläggning', 'målning',
    'dekorering', 'landskapsdesign', 'demolering', 'stomkomplettering', 'murverk',
    'golvbeläggning', 'fasad'
]

# Förutsätter att 'occupation_field' finns, fyll annars NaN med tomma strängar för att undvika fel
data['occupation_field'] = data['occupation_field'].fillna('')

# Filtrera data för att behålla endast de poster som innehåller något av nyckelorden
filtered_data = data[data['occupation_field'].str.contains('|'.join(construction_keywords), case=False)]

# Spara den filtrerade datan till en CSV-fil med kommatecken som separator
filtered_data.to_csv('/Users/svenhammarberg/Desktop/2023 enkel/filtered_byggbranschen_data.csv', index=False)

print(f"Filtered data contains {len(filtered_data)} records related to the construction industry.")

