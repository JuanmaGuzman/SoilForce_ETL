import pandas as pd
import numpy as np

def read_table_and_extract_values(filename):
    # Read the text file and extract the lines
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Define the required patterns and headers
    load_combinations_header = "*****     LOAD COMBINATIONS RESULTS      *****"
    load_combinations_pattern = "LOAD COMB. :"
    load_combinations_coordinate_system = "THE PILE COORDINATE SYSTEM (LOCAL AXES)"
    pile_reactions_header = "* PILE TOP REACTIONS *"
    stress_table_header = "PILE GROUP   STRESS, KN/ M**2"

    # Initialize variables to track the reading process
    count_header_found = False
    read_combination = False
    read_pattern = False
    read_table = False
    table_data = []
    all_tables = []

    # Loop through each line in the file
    for line in lines:
        # Check if the header for load combinations results is found
        if load_combinations_header in line:
            count_header_found = True

        # Check if a specific load combination is found
        if count_header_found and load_combinations_pattern in line:
            read_combination = True

        # Check if the pile coordinate system is found
        elif read_combination and load_combinations_coordinate_system in line:
            read_pattern = True

        # Check if the header for pile top reactions is found
        elif read_pattern and pile_reactions_header in line:
            read_table = True

        # Check if the header for stress table is found to stop reading
        elif read_table and stress_table_header in line:
            read_table = False
            read_pattern = False
            read_combination = False

            # If inside the table and the line is not empty, add the data to the table_data list
        if read_table and line.strip():
            data = line.split()
            if len(data) == 7:  # Make sure it's a row of the table
                table_data.append(data)

        # If a combination is complete, create a DataFrame with it and append it to all_tables
        if not read_combination and table_data:
            columns = ["PILE GROUP", "AXIAL, KN", "LAT. y, KN", "LAT. z, KN", "MOM x, KN-M", "MOM y, KN-M", "MOM z, KN-M"]
            df = pd.DataFrame(table_data, columns=columns)
            all_tables.append(df)
            table_data = []

    return all_tables

if __name__ == "__main__":
    columns_array = [['PILE GROUP', 'AXIAL, KN'], ['PILE GROUP',  "MOM y, KN-M", "MOM z, KN-M"], ['PILE GROUP', "LAT. y, KN", "LAT. z, KN"]]

    a_df = pd.DataFrame()
    q_df = pd.DataFrame()
    m_df = pd.DataFrame()

    filename = input("Ingrese el nombre del archivo de entrada (con extensión): ")
    all_tables = read_table_and_extract_values(filename)

    if all_tables:
        combinations = [f"Comb #{i+1}" for i in range(len(all_tables))]
        for table in all_tables:
            # Create a DataFrame from the dictionary
            df = pd.DataFrame(table)

            # Filter out rows where 'PILE GROUP' is a number
            df = df[df['PILE GROUP'].str.isnumeric()]

            selected_columns = ['PILE GROUP', 'AXIAL, KN', "MOM y, KN-M", "MOM z, KN-M", "LAT. y, KN", "LAT. z, KN"]
            selected_df = df[selected_columns]

            # Convert all values to numeric
            selected_df = selected_df.apply(pd.to_numeric, errors='coerce')

            # Calculate Q and M values for each row
            Q_values = np.sqrt(selected_df["LAT. y, KN"].astype(float) ** 2 + selected_df["LAT. z, KN"].astype(float) ** 2)
            M_values = np.sqrt(selected_df["MOM y, KN-M"].astype(float) ** 2 + selected_df["MOM z, KN-M"].astype(float) ** 2)

            # Add the calculated columns to the DataFrame
            selected_df["Q"] = Q_values
            selected_df["M"] = M_values

            selected_df = selected_df[['PILE GROUP', 'AXIAL, KN', "Q", "M"]]


            columns_to_process = ['AXIAL, KN', 'Q', 'M']
            final_dfs = []

            for column in columns_to_process:
                # Pivot the DataFrame
                transposed_df = selected_df.pivot(index=None, columns='PILE GROUP', values=column)
                transposed_df.columns = ['PILE ' + str(col) for col in transposed_df.columns]

                # Inside the loop for column processing
                values = []
                for col in transposed_df.columns:
                    pile_number = col.split()[-1]
                    value = transposed_df[col].dropna().values[0]  # Access value using .values[0]
                    values.append(value)

                column_names = {f"Pile {i+1}": [value] for i, value in enumerate(values)}
                df = pd.DataFrame(column_names)

                if column == 'AXIAL, KN':
                    # Add the "Combination" column to the DataFrame as the first column
                    df.insert(0, "Combination", combinations[len(a_df):len(a_df)+len(df)])
                    # Concatenate the current df to the final_df DataFrame
                    a_df = pd.concat([a_df, df], ignore_index=True)

                elif column == 'Q':
                    # Add the "Combination" column to the DataFrame as the first column
                    df.insert(0, "Combination", combinations[len(q_df):len(q_df)+len(df)])
                    # Concatenate the current df to the final_df DataFrame
                    q_df = pd.concat([q_df, df], ignore_index=True)

                elif column == 'M':
                    # Add the "Combination" column to the DataFrame as the first column
                    df.insert(0, "Combination", combinations[len(m_df):len(m_df)+len(df)])    
                    # Concatenate the current df to the final_df DataFrame
                    m_df = pd.concat([m_df, df], ignore_index=True)


        output_file = "output.xlsx"

        with pd.ExcelWriter(output_file) as writer:
            a_df.to_excel(writer, sheet_name='Resultant A', index=False)
            q_df.to_excel(writer, sheet_name='Resultant Q', index=False)
            m_df.to_excel(writer, sheet_name='Resultant M', index=False)

        print("DataFrames written to Excel file successfully.")

    else:
        print("No data found for any load combination in the table.")


