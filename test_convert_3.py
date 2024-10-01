import pandas as pd

def inverted_index_translation(file_path):
    # Đọc tất cả các sheet từ file Excel
    all_sheets = pd.read_excel(file_path, sheet_name=None)

    # Tạo một từ điển để lưu giá trị và địa chỉ
    inverted_index = {}

    # Lặp qua từng sheet
    for df in all_sheets.values():
        # Lặp qua từng ô trong DataFrame
        for i, row in df.iterrows():
            for j, value in enumerate(row):
                if pd.notna(value):  # Bỏ qua ô trống
                    key = value
                    # Tính toán chỉ số cột theo quy tắc Excel
                    if j < 26:
                        col_cell = chr(65 + j)  # Chỉ số cột từ A đến Z
                    else:
                        col_cell = f"{chr(64 + j // 26)}{chr(65 + j % 26)}"  # Chỉ số cột từ AA trở đi
                    
                    position = f"{col_cell}{i + 1}"  # Vị trí của ô
                    # Nếu giá trị đã tồn tại trong từ điển, thêm địa chỉ
                    if key in inverted_index:
                        inverted_index[key].append(position)  # Chỉ địa chỉ ô
                    else:
                        inverted_index[key] = [position]

    # Tạo bảng Markdown từ từ điển
    markdown_table = "| Value | Addresses |\n|-------|-----------|\n"
    for value, addresses in inverted_index.items():
        addresses_str = ', '.join(addresses)  # Chuyển danh sách địa chỉ thành chuỗi
        markdown_table += f"| {value} | {addresses_str} |\n"

    return markdown_table

# Ví dụ sử dụng
file_path = '318_1_求人票（総務部）2022.11新規ver2 (2).xlsx'  # Đường dẫn đến file Excel
markdown_str = inverted_index_translation(file_path)

# Xuất ra màn hình hoặc ghi vào file
print(markdown_str)

# Save or print the markdown result
with open('output.md', 'w', encoding='utf-8') as f:
    f.write(markdown_str)

