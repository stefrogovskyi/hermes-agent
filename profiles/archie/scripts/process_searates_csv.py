
import csv
import os
import sys

# Corrected paths
# Use absolute paths directly or build them carefully
PROFILE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'profiles', 'archie'))

input_csv_path = os.path.join(PROFILE_ROOT, 'cache', 'documents', 'temp_searates_catalog.csv')
output_tsv_path = os.path.join(PROFILE_ROOT, 'cache', 'documents', 'searates_catalog_reset_status.tsv')
QUEUE_MANAGER_SCRIPT = os.path.join(PROFILE_ROOT, 'content_pipeline', 'queue_manager.py')

print(f"Processing CSV from: {input_csv_path}")
print(f"Writing TSV to: {output_tsv_path}")

try:
    with open(input_csv_path, 'r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile, delimiter=',')
        
        try:
            header = next(reader)
        except StopIteration:
            print("Input CSV is empty or contains only a header.")
            sys.exit(0)

        try:
            status_col_index = header.index("Статус")
        except ValueError:
            print("Error: 'Статус' column not found in the header of the CSV file.")
            sys.exit(1)
        
        with open(output_tsv_path, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile, delimiter='\t')
            writer.writerow(header) # Write header to TSV
            
            processed_rows = 0
            for i, row in enumerate(reader):
                if len(row) > status_col_index:
                    row[status_col_index] = "В очереди"
                    writer.writerow(row)
                    processed_rows += 1
                else:
                    print(f"Warning: Skipping malformed row {i+2} (too few columns): {row}")

    print(f"Successfully processed CSV and wrote TSV. Total data rows processed: {processed_rows}")

except FileNotFoundError:
    print(f"Error: Input CSV file not found at {input_csv_path}")
    sys.exit(1)
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    sys.exit(1)
