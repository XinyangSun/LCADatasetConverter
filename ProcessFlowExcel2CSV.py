import os

import pandas as pd


# Function to convert an Excel file to a CSV file
def convert_excel_to_csv(json_file_path, csv_file_path):
    # Load the Excel file
    excel_file = json_file_path

    # Read specific sheets from the Excel file
    sheet1 = pd.read_excel(excel_file, sheet_name='General information')
    outputs_table = pd.read_excel(excel_file, sheet_name='Outputs')
    inputs_table = pd.read_excel(excel_file, sheet_name='Inputs')
    flows_table = pd.read_excel(excel_file, sheet_name='Flows')

    # Extract process UUID and name from 'General information' sheet
    process_uuid = sheet1.iloc[0, 1]
    process_name = sheet1.iloc[1, 1]

    # Extract relevant columns from 'Outputs' and 'Inputs' sheets
    flow_names_outputs = outputs_table.iloc[1:, 1].tolist()
    categories_outputs = outputs_table.iloc[1:, 2].tolist()
    amount_outputs = outputs_table.iloc[1:, 3].tolist()
    flow_names_inputs = inputs_table.iloc[1:, 1].tolist()
    categories_inputs = inputs_table.iloc[1:, 2].tolist()
    amount_inputs = inputs_table.iloc[1:, 3].tolist()

    # Create a mapping of flow names and categories to UUIDs from 'Flows' sheet
    flows_mapping = flows_table.set_index(['Name', 'Category'])['UUID'].to_dict()

    # Map flow names and categories to their UUIDs for outputs and inputs
    flow_ids_outputs = [flows_mapping.get((name, category), 'Unknown') for name, category in
                        zip(flow_names_outputs, categories_outputs)]
    flow_ids_inputs = [flows_mapping.get((name, category), 'Unknown') for name, category in
                       zip(flow_names_inputs, categories_inputs)]

    # Filter rows in 'Outputs' table where the first column is 'x'
    filtered_outputs = outputs_table[outputs_table.iloc[:, 0] == 'x']

    # Extract specific values from the filtered outputs
    if not filtered_outputs.empty:
        column_3_value = filtered_outputs.iloc[0, 1]
        column_4_value = filtered_outputs.iloc[0, 5]
        column_5_value = filtered_outputs.iloc[0, 6]
    else:
        column_3_value = 'N/A'
        column_4_value = 'N/A'
        column_5_value = 'N/A'

    # Prepare data for CSV from Outputs table
    data_outputs = {'process_uuid': [process_uuid] * (len(outputs_table) - 1),
        'process_name': [process_name] * (len(outputs_table) - 1), 'flow_name': flow_names_outputs,
        'flow_category': categories_outputs, 'flow_uuid': flow_ids_outputs, 'flow_amount': amount_outputs,
        'product_name': [column_3_value] * (len(outputs_table) - 1),
        'product_value': [column_4_value] * (len(outputs_table) - 1),
        'product_currency': [column_5_value] * (len(outputs_table) - 1),
        'source': ['Output'] * (len(outputs_table) - 1)}

    # Prepare data for CSV from Inputs table
    data_inputs = {'process_uuid': [process_uuid] * (len(inputs_table) - 1),
        'process_name': [process_name] * (len(inputs_table) - 1), 'flow_name': flow_names_inputs,
        'flow_category': categories_inputs, 'flow_uuid': flow_ids_inputs, 'flow_amount': amount_inputs,
        'product_name': [column_3_value] * (len(inputs_table) - 1),
        'product_value': [column_4_value] * (len(inputs_table) - 1),
        'product_currency': [column_5_value] * (len(inputs_table) - 1), 'source': ['Input'] * (len(inputs_table) - 1)}

    # Create DataFrames for Outputs and Inputs
    csv_data_outputs = pd.DataFrame(data_outputs)
    csv_data_inputs = pd.DataFrame(data_inputs)

    # Combine the two DataFrames
    combined_csv_data = pd.concat([csv_data_outputs, csv_data_inputs], ignore_index=True)

    # Save the combined DataFrame to a CSV file
    combined_csv_data.to_csv(csv_file_path, index=False)


# Path to the folder containing Excel files
json_folder_path = 'Downloads/New Folder With Items'
# Path to the folder where CSV files will be saved
csv_folder_path = 'Downloads/processcsv'

# Create the CSV folder if it doesn't exist
os.makedirs(csv_folder_path, exist_ok=True)

# Loop through each file in the JSON folder
for filename in os.listdir(json_folder_path):
    # Check if the file is an Excel file
    if filename.endswith('.xlsx'):
        # Define the full path to the Excel file
        json_file_path = os.path.join(json_folder_path, filename)

        # Define the full path for the corresponding CSV file
        csv_file_name = os.path.splitext(filename)[0] + '.csv'
        csv_file_path = os.path.join(csv_folder_path, csv_file_name)

        # Convert the Excel file to CSV
        convert_excel_to_csv(json_file_path, csv_file_path)
