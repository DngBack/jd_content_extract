from collections import defaultdict

def parse_range(cell_range):
    """Parse a range like 'C5:H6' into individual cell coordinates."""
    start, end = cell_range.split(':')
    start_col, start_row = start[:1], int(start[1:])
    end_col, end_row = end[:1], int(end[1:])
    
    cols = [chr(c) for c in range(ord(start_col), ord(end_col) + 1)]
    rows = list(range(start_row, end_row + 1))
    
    return [(col, row) for row in rows for col in cols]

def group_ranges_by_row(merged_ranges):
    """Group the merged cell ranges based on the horizontal rows."""
    row_groups = defaultdict(list)
    
    for cell_range in merged_ranges:
        cells = parse_range(cell_range)
        for col, row in cells:
            row_groups[row].append(cell_range)
    
    return row_groups

def find_comprehensive_groups(row_groups):
    """Identify the most comprehensive range for each row based on coverage."""
    comprehensive_groups = []
    
    for row, ranges in row_groups.items():
        # Sort ranges by the start column
        sorted_ranges = sorted(ranges, key=lambda r: parse_range(r)[0])
        # Choose the largest range (comprehensive coverage) for this row
        comprehensive_groups.append({
            "row": row,
            "ranges": sorted_ranges
        })
    
    return comprehensive_groups

# Sample input
merged_ranges = ['AV1:AZ1', 'A2:BH2', 'AU3:AX3', 'AY3:AZ3', 'BA3:BB3', 'BC3:BD3', 
                 'BE3:BF3', 'BG3:BH3', 'A4:B14', 'C4:H4', 'I4:AE4', 'AF4:AK6', 
                 'AL4:AM4', 'AN4:AP4', 'AR4:AU4', 'C5:H6', 'I5:AE6', 'AL5:BH5',
                 # Add the rest of the ranges here...
                 ]

# Step 1: Group ranges by horizontal row
row_groups = group_ranges_by_row(merged_ranges)

# Step 2: Find the comprehensive groups
comprehensive_groups = find_comprehensive_groups(row_groups)

# Output the result
for group in comprehensive_groups:
    print(f"Row {group['row']}: {group['ranges']}")
