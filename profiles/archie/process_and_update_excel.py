
import pandas as pd
import json

try:
    df = pd.read_excel('SeaRates_Blogposts.xlsx')
    
    # Find the first row where 'Статус' (Column D) is 'В очереди'
    found_row_index = -1
    
    for index, row in df.iterrows():
        if row[df.columns[3]] == 'В очереди': # Column D (index 3)
            found_row_index = index
            break
            
    if found_row_index != -1:
        # Update status to 'В процессе'
        df.at[found_row_index, df.columns[3]] = 'В процессе'
        df.to_excel('SeaRates_Blogposts.xlsx', index=False)
        
        # Prepare data for next steps
        row_number_1_indexed = found_row_index + 2 # +1 for 0-indexed to 1-indexed, +1 for header row
        article_title = df.at[found_row_index, df.columns[0]] # Column A
        article_url = df.at[found_row_index, df.columns[1]]   # Column B
        article_language = df.at[found_row_index, df.columns[2]] # Column C

        result = {
            "row_number": row_number_1_indexed,
            "article_title": article_title,
            "article_url": article_url,
            "article_language": article_language,
            "status_updated": "В процессе"
        }
        print(json.dumps(result))
    else:
        print(json.dumps({"status": "no_rows_found"}))

except Exception as e:
    print(json.dumps({"error": str(e)}))
