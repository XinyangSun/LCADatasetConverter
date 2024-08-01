import os

import pandas as pd


# Function to load a CSV file into a DataFrame
def load_csv(file_path):
    return pd.read_csv(file_path)


# Function to generate output by matching process data with category data
def generate_output(process_folder, folder_path, output_path):
    # Load the process CSV file into a DataFrame
    df1 = pd.read_csv(process_folder)
    # If the DataFrame is empty, return without processing
    if len(df1) < 1:
        return

    results = []  # List to store the result rows

    # Loop through each file in the folder containing category CSV files
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            # Define the full path to the category CSV file
            file_path = os.path.join(folder_path, filename)
            # Load the category CSV file into a DataFrame
            df2 = load_csv(file_path)

            # Extract category ID and name from the first row of the category DataFrame
            category_id = df2.iloc[0, 0]
            category_name = df2.iloc[0, 1]

            matched_amount = 0  # Initialize matched amount for the current category

            # Loop through each row in the process DataFrame
            for _, row in df1.iterrows():
                process_uuid = row['process_uuid']
                process_name = row['process_name']
                product_name = row['product_name']
                product_value = row['product_value']

                flow_id = row['flow_uuid']
                amount1 = row['flow_amount']

                # Find matching rows in the category DataFrame based on Flow ID
                match = df2[df2['Flow ID'] == flow_id]
                if not match.empty:
                    # Extract the impact factor for the matching row
                    amount2 = match.iloc[0]['Impact Factor']
                    # Calculate the matched amount by multiplying flow amount with impact factor
                    matched_amount += amount1 * amount2

            # Append the result for the current process and category to the results list
            results.append({'Process ID': process_uuid, 'Process Name': process_name, 'Product Name': product_name,
                'Product Value': product_value, 'Category ID': category_id, 'Category Name': category_name,
                'Amount': matched_amount})

    # Create a DataFrame from the results list
    output_df = pd.DataFrame(results)
    # Save the results DataFrame to a CSV file
    output_df.to_csv(output_path, index=False)


# Loop through each file in the process CSV folder
for filename in os.listdir('Downloads/processcsv/unfinished'):
    if filename.endswith('.csv'):
        # Define the full path to the process CSV file
        json_file_path = os.path.join('Downloads/processcsv/unfinished', filename)

        # Define the full path for the corresponding output CSV file
        csv_file_name = os.path.splitext(filename)[0] + '.csv'
        csv_file_path = os.path.join('Downloads/res', csv_file_name)

        # Generate the output by matching process data with category data
        generate_output(json_file_path, 'Downloads/selected_category', csv_file_path)
