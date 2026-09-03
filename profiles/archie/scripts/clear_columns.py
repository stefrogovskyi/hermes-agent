
import csv
import os
import sys

input_log_path = "/opt/hermes/profiles/archie/cache/terminal-output/out-1786797994-605311-7a40.log"
output_tsv_path = "/opt/hermes/profiles/archie/cache/documents/searates_blogposts_cleared.tsv"

print(f"Reading content from: {input_log_path}")
print(f"Writing cleared TSV to: {output_tsv_path}")

try:
    with open(input_log_path, 'r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile, delimiter='\t')
        
        output_rows = []
        
        # Initialize column indices with a value that indicates they are not found
        col_e_index = -1
        col_f_index = -1
        col_g_index = -1 # Assuming 7th column (index 6) for G

        # Read header to find column indices
        try:
            header = next(reader)
            output_rows.append(header)
            
            if "Название статьи на Наво" in header:
                col_e_index = header.index("Название статьи на Наво")
            if "Ссылка на Наво / Файл Наво" in header:
                col_f_index = header.index("Ссылка на Наво / Файл Наво")
            
            # For column G, we'll assume it's at index 6 if the header is long enough
            if len(header) > 6: # Check if header has at least 7 columns for G
                col_g_index = 6

        except StopIteration:
            print("Input file is empty or contains no header.")
            sys.exit(0)
        except ValueError as e:
            print(f"Warning: Some expected header columns not found, proceeding with available: {e}")

        # Process data rows
        for i, row in enumerate(reader):
            # Make sure the row is long enough to cover the required columns
            # We need to extend the row to include at least 7 columns (index 6 for G)
            while len(row) <= col_g_index:
                row.append('')
            
            if col_e_index != -1 and len(row) > col_e_index:
                row[col_e_index] = '' # Clear column E
            
            if col_f_index != -1 and len(row) > col_f_index:
                row[col_f_index] = '' # Clear column F
            
            if col_g_index != -1 and len(row) > col_g_index: # Ensure G index is valid for current row
                row[col_g_index] = '' # Clear column G
            
            output_rows.append(row)

    with open(output_tsv_path, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile, delimiter='\t')
        writer.writerows(output_rows)
    
    print(f"Successfully cleared columns E, F, G and wrote to: {output_tsv_path}")
    print(f"Total data rows processed (excluding header): {len(output_rows) - 1}")

except FileNotFoundError:
    print(f"Error: Input log file not found at {input_log_path}")
    sys.exit(1)
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    sys.exit(1)
