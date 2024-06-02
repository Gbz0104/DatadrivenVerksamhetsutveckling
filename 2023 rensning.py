# Detta Python-script behandlar JSON-data från filer och exporterar renad och strukturerad information till en CSV-fil.
# Scriptet läser in svenska stoppord, renar textdata från oönskade tecken och stoppord, och tar även bort specifika tidstämplar från datumsträngar.
# Slutligen exporteras data i batcher till en angiven CSV-fil, där vissa kolumner tas bort baserat på en definierad lista.


# tänk på att:
# - det behövs swedish_stopwords.txt
# - ändra filvägarna


import pandas as pd
from pandas import json_normalize
import json
import re
import os


# Laddar svenska stoppord från en textfil för att filtrera dessa från bearbetad text
with open('/Users/svenhammarberg/Desktop/2023 enkel/swedish_stopwords.txt', 'r', encoding='utf-8') as f:
   swedish_stopwords = f.read().split()


def clean_text(text):
   # Rensar och normaliserar textdata genom att omvandla till små bokstäver och ta bort punktering och stoppord
   if not isinstance(text, str):
       return text
   text = text.lower()
   text = re.sub(r'[().,;*:"\-?!\'/]', ' ', text)
   text = re.sub(r'\s+', ' ', text)
   text = ' '.join(word for word in text.split() if word not in swedish_stopwords)
   return text.strip()


def clean_date(date_str):
   # Rensar datumsträngar från tidsstämpel som följer efter 'T' eller 't'
   if isinstance(date_str, str):
       return re.sub(r'[Tt].*', '', date_str)  # Ändrat för att inkludera både 'T' och 't'
   return date_str


def handle_json_data(json_data):
   # Applicerar clean_text på varje strängvärde i json_data rekursivt
   if isinstance(json_data, dict):
       for k, v in json_data.items():
           json_data[k] = handle_json_data(v)
   elif isinstance(json_data, list):
       return [handle_json_data(v) for v in json_data]
   else:
       return clean_text(json_data)
   return json_data


def data_stream(file_paths):
   # Generator som läser en JSON-fil rad för rad
   for file_path in file_paths:
       with open(file_path, 'r', encoding='utf-8') as file:
           for line in file:
               yield json.loads(line)


def process_data(file_paths, output_path, update_frequency=1000):
   # Huvudfunktion för dataprocessning och export till CSV
   data_list = []
   total_lines = sum(1 for file_path in file_paths for line in open(file_path, 'r', encoding='utf-8'))
   processed_lines = 0
   first_write = True  # För att kontrollera om header ska skrivas


   # Lista av kolumnnamn som ska tas bort från det slutliga datasetet
   columns_to_remove = [
       'id', 'external_id', 'webpage_url', 'logo_url', 'access',
       'employment_type.concept_id', 'employment_type.legacy_ams_taxonomy_id',
       'salary_type.concept_id', 'duration.concept_id', 'duration.legacy_ams_taxonomy_id',
       'working_hours_type.concept_id', 'working_hours_type.legacy_ams_taxonomy_id',
       'employer.email', 'employer.organization_number',
       'application_details.reference', 'application_details.email', 'application_details.url',
       'occupation.concept_id', 'occupation.legacy_ams_taxonomy_id',
       'occupation_group.concept_id', 'occupation_group.legacy_ams_taxonomy_id',
       'occupation_field.concept_id', 'workplace_address.municipality_code',
       'workplace_address.municipality_concept_id', 'workplace_address.region_code',
       'workplace_address.region_concept_id', 'workplace_address.country_code',
       'workplace_address.country_concept_id', 'workplace_address.postcode',
       'workplace_address.coordinates', 'access_to_own_car', 'driving_license',
       'application_contacts', 'removed', 'source_type', 'timestamp',
       'salary_type.legacy_ams_taxonomy_id', 'employer.url', 'application_details.information',
       'application_details.other', 'occupation_field.legacy_ams_taxonomy_id',
       'workplace_address.street_address', 'workplace_address.city', 'scope_of_work.min', 'scope_of_work.max',
       'employer.phone_number', 'original_id', 'detected_language', 'removed_data', 'description.text_formatted',
       'description.company_information', 'description.needs', 'description.requirements', 'description.conditions'
   ]


   for json_data in data_stream(file_paths):
       cleaned_data = handle_json_data(json_data)
       cleaned_data['application_deadline'] = clean_date(cleaned_data.get('application_deadline'))
       cleaned_data['publication_date'] = clean_date(cleaned_data.get('publication_date'))
       cleaned_data['last_publication_date'] = clean_date(cleaned_data.get('last_publication_date'))
       flat_data = json_normalize(cleaned_data)
       data_list.append(flat_data)
       processed_lines += 1


       if len(data_list) >= 100:  # Processa i batcher om 100 rader
           full_data = pd.concat(data_list, ignore_index=True)
           full_data.drop(columns=columns_to_remove, errors='ignore', inplace=True)
           full_data.to_csv(output_path, mode='a', index=False, header=first_write)
           data_list = []  # Reset the list for the next batch
           first_write = False


           if processed_lines % update_frequency == 0:
               progress = (processed_lines / total_lines) * 100
               print(f"Processed {processed_lines} of {total_lines} records ({progress:.2f}%)")


   if data_list:  # Hanterar kvarstående data i slutet av filbehandling
       full_data = pd.concat(data_list, ignore_index=True)
       full_data.drop(columns=columns_to_remove, errors='ignore', inplace=True)
       full_data.to_csv(output_path, mode='a', index=False, header=first_write)
       progress = (processed_lines / total_lines) * 100
       print(f"Final data batch written. Total records processed: {processed_lines} ({progress:.2f}%)")


file_paths = [
   '/Users/svenhammarberg/Desktop/2023 enkel/2023.jsonl'
]
output_path = '/Users/svenhammarberg/Desktop/2023 enkel/all_data.csv'


process_data(file_paths, output_path, update_frequency=10000)  # Justera update_frequency efter behov


