"""
import pandas as pd 

# Load the data
file_path = 'C:/Users/steff/Contacts/Downloads/filtered_byggbranschen_data.csv'
data = pd.read_csv(file_path, usecols=['occupation_field', 'workplace_address.municipality'])

# Group the data by occupation field and municipality, and count the number of jobs
jobs_by_location = data.groupby(['occupation_field', 'workplace_address.municipality']).size().reset_index(name='job_count')

# Sort the results for better readability
jobs_by_location_sorted = jobs_by_location.sort_values(['workplace_address.municipality', 'job_count'], ascending=[True, False])

# Display the sorted, grouped data
print(jobs_by_location_sorted)

# Optionally, save this data to a CSV file for further analysis or use
output_path = 'C:/Users/steff/Contacts/Downloads/jobs_by_location.csv'
jobs_by_location_sorted.to_csv(output_path, index=False)
print(f'The grouped data has been saved to {output_path}')  
"""

"""
import pandas as pd 

# Load the data
file_path = 'C:/Users/steff/Contacts/Downloads/Svens fixade fil.csv'
data = pd.read_csv(file_path, usecols=['occupation_field', 'workplace_address.municipality'])

# Group the data by occupation field and municipality, and count the number of jobs
jobs_by_location = data.groupby(['occupation_field', 'workplace_address.municipality']).size().reset_index(name='job_count')

# Sort the results for better readability
jobs_by_location_sorted = jobs_by_location.sort_values(['workplace_address.municipality', 'job_count'], ascending=[True, False])

# Display the sorted, grouped data
print(jobs_by_location_sorted)

# Save this data to a CSV file for further analysis or use
output_path = 'C:\\Users\\steff\\Contacts\\Downloads\\Svens fixade fil.csv'
jobs_by_location_sorted.to_csv(output_path, index=False)
print(f'The grouped data has been saved to {output_path}')
"""
"""
import csv

# Load the data
file_path = "C:/Users/steff/Contacts/Downloads/Svens fixade fil.csv"

# Dictionary för att hålla reda på antalet jobb per plats
jobs_per_location = {}

# Read the data from CSV file
with open(file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        location = row['workplace_address.municipality']
        if location in jobs_per_location:
            jobs_per_location[location] += 1
        else:
            jobs_per_location[location] = 1

# Sortera platserna efter antalet jobb
sorted_locations = sorted(jobs_per_location.items(), key=lambda x: x[1], reverse=True)

# Skriv ut platserna och antalet jobb
for location, job_count in sorted_locations:
    print(f"{location}: {job_count} jobb")

# Spara resultatet till en CSV-fil
output_path = "C:/Users/steff/Contacts/Downloads/jobs_per_location.csv"
with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['workplace_address.municipality', 'job_count'])
    for location, job_count in sorted_locations:
        writer.writerow([location, job_count])

print(f'The job counts per location have been saved to {output_path}')
"""


import pandas as pd 

# Load the data
file_path = 'C:/Users/steff/Contacts/Downloads/filtered_byggbranschen_data.csv'
data = pd.read_csv(file_path, usecols=['workplace_address.municipality'])

# Group the data by municipality and count the number of jobs
jobs_by_location = data.groupby('workplace_address.municipality').size().reset_index(name='job_count')

# Sort the results for better readability
jobs_by_location_sorted = jobs_by_location.sort_values('job_count', ascending=False)

# Display the sorted data
print(jobs_by_location_sorted)

# Optionally, save this data to a CSV file for further analysis or use
output_path = 'C:/Users/steff/Contacts/Downloads/jobs_per_location.csv'
jobs_by_location_sorted.to_csv(output_path, index=False)
print(f'The job counts per location have been saved to {output_path}')




