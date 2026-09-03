
import csv
import os
import json
import subprocess
import sys

# Define paths
HERMES_HOME = os.environ.get('HERMES_HOME', os.path.expanduser('~/.hermes'))
ARCHIE_PROFILE_DIR = HERMES_HOME
TSV_FILE_PATH = os.path.join(ARCHIE_PROFILE_DIR, 'cache', 'documents', 'searates_catalog_reset_status.tsv')
QUEUE_MANAGER_SCRIPT = os.path.join(ARCHIE_PROFILE_DIR, 'content_pipeline', 'queue_manager.py')

print(f"Starting script to add links to queue from: {TSV_FILE_PATH}")
print(f"Using queue manager: {QUEUE_MANAGER_SCRIPT}")

def run_command(command_args, timeout=None):
    try:
        result = subprocess.run(command_args, capture_output=True, text=True, check=True, timeout=timeout)
        return {"exit_code": 0, "output": result.stdout.strip(), "error": ""}
    except subprocess.CalledProcessError as e:
        return {"exit_code": e.returncode, "output": e.stdout.strip(), "error": e.stderr.strip()}
    except FileNotFoundError:
        return {"exit_code": 1, "output": "", "error": f"Command not found: {command_args[0]}"}

# Read the entire file content
try:
    with open(TSV_FILE_PATH, 'r', encoding='utf-8') as f:
        raw_content = f.read()
except FileNotFoundError:
    print(f"Error: TSV file not found at {TSV_FILE_PATH}")
    sys.exit(1)

# Replace escaped tabs with actual tabs
processed_content = raw_content.replace('\\t', '\t')

lines = processed_content.strip().split('\n')

# Handle empty file or only header
if not lines or len(lines) < 2:
    print("File is empty or contains only a header. No links to process.")
    print("Total links attempted to add to queue: 0")
    print("Successfully added to queue: 0")
    sys.exit(0)

header = lines[0].split('\t')

# Find the index of the "Ссылка" column
try:
    link_col_index = header.index("Ссылка")
except ValueError:
    print("Error: 'Ссылка' column not found in the header.")
    print("Total links attempted to add to queue: 0")
    print("Successfully added to queue: 0")
    sys.exit(1)

links_to_add = []
problematic_lines = []

for i, line in enumerate(lines[1:]):
    if not line.strip(): # Skip empty lines
        continue
    
    row = line.split('\t')
    if len(row) > link_col_index:
        links_to_add.append(row[link_col_index])
    else:
        problematic_lines.append(f"Line {i+2}: {line}") # +2 because of header (1) and 0-indexing

added_count = 0
failed_adds = []

if not links_to_add:
    print("No valid links found to add to the queue.")
else:
    # Get current queue items to avoid adding duplicates
    current_queue_links = set()

    def parse_queue_output(output):
        links = set()
        for line in output.split('\n'):
            parts = line.split()
            if len(parts) >= 4 and parts[0].startswith('[') and parts[0].endswith(']'):
                # Assuming the last part is always the URL
                links.add(parts[-1])
        return links

    list_result = run_command([sys.executable, QUEUE_MANAGER_SCRIPT, 'list'], timeout=300)
    if list_result['exit_code'] == 0:
        try:
            current_queue_links = parse_queue_output(list_result['output'])
        except Exception as e:
            print(f"Warning: Could not parse queue list output: {list_result['output']} - Error: {e}")
    else:
        print(f"Warning: Failed to list current queue: {list_result['error']}")

    for link in links_to_add:
        if link in current_queue_links:
            added_count += 1 # Count as 'added' since it's effectively in the queue
            continue

        add_command_args = [sys.executable, QUEUE_MANAGER_SCRIPT, 'add', link, '--type=rewrite']
        result = run_command(add_command_args)
        if result['exit_code'] == 0:
            added_count += 1
        else:
            failed_adds.append({"link": link, "output": result['output'], "error": result['error']})

print(f"Total links attempted to add to queue: {len(links_to_add)}")
print(f"Successfully added to queue (including existing ones): {added_count}")

if failed_adds:
    print(f"Failed to add the following links to queue: {len(failed_adds)} links")
    for i, failure in enumerate(failed_adds):
        if i >= 10: # Limit output to first 10 failures
            break
        print(f"  - Link: {failure["link"]}\n    Output: {failure["output"]}\n    Error: {failure["error"]}")
    if len(failed_adds) > 10:
        print(f"  ... and {len(failed_adds) - 10} more failures.")

if problematic_lines:
    print(f"Found {len(problematic_lines)} problematic lines in the input file (skipped):")
    # Print only first 5 problematic lines to avoid flooding output
    for p_line in problematic_lines[:5]:
        print(f"  {p_line}")
    if len(problematic_lines) > 5:
        print(f"  ... and {len(problematic_lines) - 5} more.\n")
