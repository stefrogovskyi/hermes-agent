
import csv
from openpyxl import Workbook
import os
import sys

input_tsv_path = "/opt/hermes/profiles/archie/cache/documents/searates_blogposts_cleared.tsv"
output_xlsx_path = "/opt/hermes/profiles/archie/cache/documents/searates_blogposts.xlsx"

print(f"Converting TSV from: {input_tsv_path}")
print(f"Writing XLSX to: {output_xlsx_path}")

try:
    # Read TSV content
    with open(input_tsv_path, 'r', newline='', encoding='utf-8') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        data = list(reader)

    if not data:
        print("No data found in the TSV file.")
        sys.exit(1)

    # Create a new Excel workbook
    wb = Workbook()
    # Get the active sheet or create one if it's the default empty one
    if wb.active:
        ws = wb.active
    else:
        ws = wb.create_sheet("Sheet1", 0) # Create a sheet if active is None
    
    ws.title = "Sheet1"

    # Append data to the worksheet
    for row_data in data:
        ws.append(row_data)

    # Save the workbook
    wb.save(output_xlsx_path)

    print(f"Successfully converted TSV to XLSX: {output_xlsx_path}")
    print(f"Total rows converted: {len(data)}")

except FileNotFoundError:
    print(f"Error: Input TSV file not found at {input_tsv_path}")
    sys.exit(1)
except Exception as e:
    print(f"An unexpected error occurred during conversion: {e}")
    sys.exit(1)
