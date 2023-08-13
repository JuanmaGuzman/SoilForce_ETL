# SoilForce_etl

## Project README

### Load Combination Results Processor

This Python script is designed to process load combination results from a text file and transform them into structured Excel sheets for further analysis. The script extracts relevant information from the input file, calculates specific values, and organizes the data into separate DataFrames based on different combinations.

#### Features

1. Reads and extracts load combination results from a specified text file.
2. Processes extracted data to calculate axial forces, resultant forces (Q), and resultant moments (M) for each pile group.
3. Organizes the processed data into separate DataFrames for axial forces, resultant forces (Q), and resultant moments (M) for different combinations.
4. Outputs the processed DataFrames to an Excel file for easy analysis and sharing.

#### How to Use

1. Make sure you have Python installed on your system.
2. Ensure you have the `pandas` and `numpy` libraries installed. You can install them using the following command:
   ```
   pip install pandas numpy
   ```
3. Save the script in a `.py` file, for example, `load_combination_processor.py`.
4. Prepare your input text file containing load combination results. The file should have a structure similar to the provided sample input file.
5. Run the script by executing the following command in your terminal or command prompt:
   ```
   python load_combination_processor.py
   ```
6. Enter the name of the input text file when prompted.
7. The script will process the data and create three Excel sheets named 'Resultant A', 'Resultant Q', and 'Resultant M', each containing the processed information for different combinations.

#### Sample Input

An example of the expected format of the input text file can be found in the provided code. Ensure your input file follows a similar structure for accurate processing.

#### Output

The processed DataFrames will be saved in an Excel file named `output.xlsx` in the same directory as the script. You can open this Excel file to analyze the calculated values for each pile group and combination.

#### Notes

- This script assumes that the input text file contains the specified headers and patterns as indicated in the provided code.
- Make sure to input the correct file name when prompted, including the file extension.
- If no data is found in the input file for any load combination, the script will display a message indicating this.

For any questions or issues, feel free to contact the project maintainer.

**Disclaimer:** This script is provided as-is and without warranty. Please review and modify the script to suit your specific needs and ensure the accuracy of results.