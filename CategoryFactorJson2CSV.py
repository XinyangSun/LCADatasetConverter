import json
import os

import pandas as pd


# Function to convert a single JSON file to a CSV file
def convert_json_to_csv(json_file_path, csv_file_path):
    # Open the JSON file and load its content
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Check if 'impactFactors' key exists in the JSON data
    if 'impactFactors' not in data:
        # If not, return without processing
        return

    # Extract relevant details from the JSON data
    impact_category_id = data['@id']
    impact_category_name = data['name']
    category = data['category']
    version = data['version']
    last_change = data['lastChange']
    ref_unit = data['refUnit']
    impact_factors = data['impactFactors']

    # Prepare a list to hold rows of data
    rows = []
    for factor in impact_factors:
        # Extract flow details and other relevant data
        flow = factor['flow']
        unit = factor.get('unit', {}).get('name', '')
        flow_property = factor.get('flowProperty', {}).get('name', '')

        # Create a row with the extracted data
        row = [impact_category_id, impact_category_name, category, version, last_change, ref_unit, flow['name'],
            flow['@id'], flow['category'], flow['flowType'], flow['refUnit'], factor['value'], unit, flow_property]
        # Add the row to the list of rows
        rows.append(row)

    # Create a DataFrame from the rows list
    df = pd.DataFrame(rows, columns=['Impact Category ID', 'Impact Category Name', 'Category', 'Version', 'Last Change',
        'Reference Unit', 'Flow Name', 'Flow ID', 'Flow Category', 'Flow Type', 'Flow Reference Unit', 'Impact Factor',
        'Unit', 'Flow Property'])

    # Save the DataFrame to a CSV file
    df.to_csv(csv_file_path, index=False)


# Path to the folder containing JSON files
json_folder_path = 'Downloads/openLCA LCIA Methods 2.4.3 2024-07-22/lcia_categories'
# Path to the folder where CSV files will be saved
csv_folder_path = 'Downloads/openLCA LCIA Methods 2.4.3 2024-07-22/lcia_category_csv'

# Create the CSV folder if it doesn't exist
os.makedirs(csv_folder_path, exist_ok=True)

# Loop through each file in the JSON folder
for filename in os.listdir(json_folder_path):
    # Check if the file is a JSON file
    if filename.endswith('.json'):
        # Define the full path to the JSON file
        json_file_path = os.path.join(json_folder_path, filename)

        # Define the full path for the corresponding CSV file
        csv_file_name = os.path.splitext(filename)[0] + '.csv'
        csv_file_path = os.path.join(csv_folder_path, csv_file_name)

        # Convert the JSON file to CSV
        convert_json_to_csv(json_file_path, csv_file_path)
