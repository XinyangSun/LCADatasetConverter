import json
import os

import pandas as pd


# Function to convert a single JSON file to a CSV file
def convert_json_to_csv(json_file_path):
    # Open the JSON file and load its content
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Extract the impact method ID and name
    impact_method_id = data['@id']
    impact_method_name = data['name']

    # Extract the impact categories
    impact_categories = data['impactCategories']

    # Prepare a list to hold rows of data
    rows = []
    for category in impact_categories:
        # Extract impact category ID and name
        impact_category_id = category['@id']
        impact_category_name = category['name']

        # Create a row with the extracted data
        row = [impact_method_id, impact_method_name, impact_category_id, impact_category_name]
        # Add the row to the list of rows
        rows.append(row)

    # Create a DataFrame from the rows list
    df = pd.DataFrame(rows, columns=['Impact Method ID', 'Impact Method Name', 'Impact Category ID',
                                     'Impact Category Name', ])

    # Define the CSV file path
    csv_file_path = os.path.join('Downloads/categorymethod', impact_method_name + '.csv')

    # Save the DataFrame to a CSV file
    df.to_csv(csv_file_path, index=False)


# Path to the folder containing JSON files
json_folder_path = 'Downloads/openLCA LCIA Methods 2.4.3 2024-07-22/lcia_methods'
# Path to the folder where CSV files will be saved
csv_folder_path = 'Downloads/categorymethod'

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
        convert_json_to_csv(json_file_path)
