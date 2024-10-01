import openpyxl

# Function to read the excel file and convert to a markdown-like format, skipping empty cells
def excel_to_markdown(file_path):
    # Load the workbook and select the first sheet
    wb = openpyxl.load_workbook(file_path, data_only=True)
    sheet = wb.active

    markdown_output = ""

    # Iterate through all the cells in the sheet
    for row in sheet.iter_rows():
        for cell in row:
            # Check if the cell value is None (empty), skip the cell if True
            if cell.value is None:
                continue

            # Get the cell address, value, and formatting (if any)
            cell_address = cell.coordinate
            cell_value = cell.value
            
            # For simplicity, we'll extract only basic formatting details here
            font = cell.font
            bold = "Bold" if font.bold else "Normal"
            italic = "Italic" if font.italic else "Regular"
            underline = "Underline" if font.underline else "No Underline"

            # Create the markdown-like representation
            markdown_output += f"[{cell_address}, {cell_value}, {bold}/{italic}/{underline}]\n"

    return markdown_output

# Example Usage:
excel_file_path = '318_1_求人票（総務部）2022.11新規ver2 (2).xlsx'  # Replace with the actual file path
markdown_result = excel_to_markdown(excel_file_path)

# Save or print the markdown result
with open('output.md', 'w', encoding='utf-8') as f:
    f.write(markdown_result)

print("Markdown conversion done, empty cells skipped.")
