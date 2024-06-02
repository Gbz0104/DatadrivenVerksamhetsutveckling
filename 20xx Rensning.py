import pandas as pd
import json
import re
import os
import nltk

# Ladda ner stoppord från NLTK
nltk.download('stopwords')
nltk.download('punkt')

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Ladda svenska stoppord från NLTK
swedish_stopwords = set(stopwords.words('swedish'))

def clean_text(text):
    if not isinstance(text, str):
        return text
    text = text.lower()
    words = word_tokenize(text)
    filtered_words = [word for word in words if word not in swedish_stopwords and word.isalpha()]
    return ' '.join(filtered_words)

def clean_date(date_str):
    if isinstance(date_str, str):
        return re.sub(r'[Tt].*', '', date_str)
    return date_str

def handle_json_data(json_data):
    if isinstance(json_data, dict):
        return {k: (json_data[k] if k == 'publication_date' else handle_json_data(v)) for k, v in json_data.items()}
    elif isinstance(json_data, list):
        return [handle_json_data(v) for v in json_data]
    else:
        return clean_text(json_data)

def load_columns_to_keep(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file]

def data_stream(file_paths):
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                yield json.loads(line)

def process_data(file_paths, columns_file, output_path, update_frequency=1000):
    columns_to_keep = load_columns_to_keep(columns_file)
    data_list = []
    total_lines = sum(1 for file_path in file_paths for line in open(file_path, 'r', encoding='utf-8'))
    processed_lines = 0
    first_write = True

    for json_data in data_stream(file_paths):
        cleaned_data = handle_json_data(json_data)
        flat_data = pd.json_normalize(cleaned_data)
        data_list.append(flat_data)
        processed_lines += 1

        if len(data_list) >= 100:
            full_data = pd.concat(data_list, ignore_index=True)
            full_data = full_data[columns_to_keep]  # Behåll endast de valda kolumnerna
            full_data.to_csv(output_path, mode='a', index=False, header=first_write)
            data_list = []
            first_write = False

            if processed_lines % update_frequency == 0:
                progress = (processed_lines / total_lines) * 100
                print(f"Processed {processed_lines} of {total_lines} records ({progress:.2f}%)")

    if data_list:
        full_data = pd.concat(data_list, ignore_index=True)
        full_data = full_data[columns_to_keep]
        full_data.to_csv(output_path, mode='a', index=False, header=first_write)
        progress = (processed_lines / total_lines) * 100
        print(f"Final data batch written. Total records processed: {processed_lines} ({progress:.2f}%)")

file_paths = ['/Users/svenhammarberg/Desktop/2023 enkel/2021.jsonl']
columns_file = '/Users/svenhammarberg/Desktop/2023 enkel/columns_to_keep.txt'
output_path = '/Users/svenhammarberg/Desktop/2023 enkel/all_data_2021.csv'

process_data(file_paths, columns_file, output_path, update_frequency=10000)
