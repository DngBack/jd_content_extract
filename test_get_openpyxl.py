import pandas as pd

# File path of the Excel file
file_path = '318_1_求人票（総務部）2022.11新規ver2 (2).xlsx'  # Replace with the path to your Excel file

# Read the Excel file
df = pd.read_excel(file_path)

# Print the content of the Excel file
print(df)