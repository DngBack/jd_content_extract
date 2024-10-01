from openpyxl import load_workbook

def excel_to_markdown_with_merge(file_path):
    wb = load_workbook(file_path, data_only=True)
    markdown_output = ""

    for sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
        markdown_output += f"## {sheet_name}\n\n"  # Tiêu đề cho mỗi sheet

        # Duyệt qua từng hàng
        for row in ws.iter_rows():
            row_data = []
            for cell in row:
                # Kiểm tra nếu ô này có giá trị
                if cell.value is not None:
                    # Tính toán vị trí ô
                    position = f"{cell.column_letter}{cell.row}"
                    # Kiểm tra ô có nằm trong vùng ô hợp nhất không
                    is_merged = any(cell.coordinate in merged_cell for merged_cell in ws.merged_cells.ranges)
                    if is_merged:
                        # Lấy tất cả các địa chỉ ô trong ô hợp nhất
                        for merged_cell in ws.merged_cells.ranges:
                            if cell.coordinate in merged_cell:
                                # Lấy giá trị từ ô đầu tiên trong vùng hợp nhất
                                value = ws[merged_cell.start_cell.coordinate].value
                                # Lấy danh sách các ô trong vùng hợp nhất
                                addresses = [f"{ws.cell(row=r, column=c).coordinate}" 
                                             for r in range(merged_cell.min_row, merged_cell.max_row + 1)
                                             for c in range(merged_cell.min_col, merged_cell.max_col + 1)]
                                address_list = ', '.join(addresses)  # Chuyển danh sách thành chuỗi
                                row_data.append(f"{value} (Addresses: [{address_list}])")
                                break
                    else:
                        row_data.append(f"{cell.value} ({position})")

            # Ghi lại dữ liệu của hàng chỉ nếu có dữ liệu
            if row_data:
                markdown_output += "| " + " | ".join(row_data) + " |\n"

        markdown_output += "\n"  # Ngắt dòng giữa các sheet

    return markdown_output

# Ví dụ sử dụng
file_path = '318_1_求人票（総務部）2022.11新規ver2 (2).xlsx'  # Thay thế bằng đường dẫn tới file Excel của bạn
markdown_string = excel_to_markdown_with_merge(file_path)
print(markdown_string)

# Save or print the markdown result
with open('output_4.md', 'w', encoding='utf-8') as f:
    f.write(markdown_string)
