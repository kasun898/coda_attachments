import os
import requests
from codaio import Coda, Document
import pandas as pd

# Initialize Coda and Document
coda = Coda('API Key')
doc = Document('doc_id', coda=coda)

# Get the table and convert to DataFrame
table = doc.get_table('Applications')
df = pd.DataFrame(table.to_dict())

# Function to download attachments
def download_file(file_url, filename):
    """Downloads a file from the given URL and saves it to the specified filename."""
    try:
        response = requests.get(file_url)
        response.raise_for_status()  # Raise an error for bad responses
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f'Downloaded: {filename}')
    except requests.exceptions.RequestException as e:
        print(f'Failed to download {file_url}: {e}')

# Create download directory
download_dir = 'downloads'
os.makedirs(download_dir, exist_ok=True)

# Iterate through DataFrame and download files
for index, row in df.iterrows():
    file_url = row.get('file_url')  # Extract the file URL
    name = row.get('HR Lead No', f'document_{index + 1}')  # Get the name or use a default
    if file_url:
        # Create a valid filename by sanitizing the name
        sanitized_name = ''.join(c for c in name if c.isalnum() or c in (' ', '_')).rstrip()
        filename = os.path.join(download_dir, f'{sanitized_name}.pdf')  # Assuming the files are PDFs
        download_file(file_url, filename)
    else:
        print(f'No file URL found for item {index + 1}')


