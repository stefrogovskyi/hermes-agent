
import pandas as pd
import json

try:
    df = pd.read_excel('SeaRates_Blogposts.xlsx')
    
    # Find the first row where 'Статус' (Column D) is 'В очереди'
    # Assuming the first row is header, so actual data starts from row 1 (0-indexed)
    # Column A is index 0, B is 1, C is 2, D is 3, E is 4, F is 5
    
    found_row = None
    row_number = -1 # 1-indexed for the sheet
    
    for index, row in df.iterrows():
        if row[df.columns[3]] == 'В очереди': # Column D (index 3)
            found_row = row
            row_number = index + 2 # +1 for 0-indexed to 1-indexed, +1 for header row
            break
            
    if found_row is not None:
        result = {
            "row_number": row_number,
            "article_title": found_row[df.columns[0]], # Column A
            "article_url": found_row[df.columns[1]],   # Column B
            "article_language": found_row[df.columns[2]] # Column C
        }
        print(json.dumps(result))
    else:
        print(json.dumps({"status": "no_rows_found"}))

except Exception as e:
    print(json.dumps({"error": str(e)}))
