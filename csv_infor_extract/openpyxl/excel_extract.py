import openpyxl

def get_text_and_positions(file_path):
    # Load the workbook
    wb = openpyxl.load_workbook(file_path)
    
    # Dictionary to store text and positions
    text_positions = {}
    
    # Iterate through all sheets
    for sheet_name in wb.sheetnames:
        sheet = wb[sheet_name]
        
        # Iterate through all cells in the sheet
        for row in sheet.iter_rows(values_only=False):
            for cell in row:
                if cell.value is not None:  # Check if the cell is not empty
                    # Store the text and its position
                    position = f'{sheet_name}!{cell.coordinate}'
                    text_positions[position] = cell.value
    
    return text_positions

# Example usage
file_path = '＜ホールセール／卸売営業＞募集要件確認シート20240620.xlsx'
text_positions = get_text_and_positions(file_path)

# Print the results
for position, text in text_positions.items():
    print(f'Cell: {position}, Text: {text}')
