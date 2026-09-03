
import pandas as pd
import json
import sys

try:
    # Read the Excel file
    df = pd.read_excel('SeaRates_Blogposts.xlsx')
    
    # Arguments from the command line
    row_number_to_update = int(sys.argv[1])
    new_article_title_navo = sys.argv[2]
    drive_link = sys.argv[3]
    
    # Adjust row number for 0-indexed DataFrame (subtract 2 because it's 1-indexed for sheets and there's a header)
    df_index_to_update = row_number_to_update - 2

    if 0 <= df_index_to_update < len(df):
        # Update columns E (Название статьи на Наво), F (Ссылка на Наво / Файл Наво), and D (Статус)
        df.at[df_index_to_update, df.columns[4]] = new_article_title_navo # Column E
        df.at[df_index_to_update, df.columns[5]] = drive_link             # Column F
        df.at[df_index_to_update, df.columns[3]] = 'Готово'               # Column D

        # Save the updated DataFrame back to the same Excel file
        df.to_excel('SeaRates_Blogposts.xlsx', index=False)
        
        original_article_title = df.at[df_index_to_update, df.columns[0]]
        original_article_url = df.at[df_index_to_update, df.columns[1]]
        original_article_language = df.at[df_index_to_update, df.columns[2]]

        result = {
            "status": "success",
            "row_number": row_number_to_update,
            "original_article_title": original_article_title,
            "original_article_url": original_article_url,
            "original_article_language": original_article_language,
            "new_article_title_navo": new_article_title_navo,
            "drive_link": drive_link
        }
        print(json.dumps(result))
    else:
        print(json.dumps({"error": f"Row number {row_number_to_update} is out of bounds."}))

except Exception as e:
    print(json.dumps({"error": str(e)}))
