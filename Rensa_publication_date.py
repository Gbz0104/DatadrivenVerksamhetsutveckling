import pandas as pd

# Load the original CSV file
file_path = '/Users/svenhammarberg/Desktop/2023 enkel/rensad_occupasion_field&occupasion_v2.csv'
data = pd.read_csv(file_path)

# Convert the 'publication_date' to date format without time
data['publication_date'] = pd.to_datetime(data['publication_date']).dt.date

# Save the updated dataframe to a new CSV file
updated_file_path = '/Users/svenhammarberg/Desktop/2023 enkel/Rensad_alla.csv'
data.to_csv(updated_file_path, index=False)
