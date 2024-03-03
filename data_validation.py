import pandas as pd
import re
import json

def parse_children(children):
    if children is None or children == []:
        return []
    if isinstance(children, list):
        return [f"{child['name']} ({child['age']})" for child in children]
    if isinstance(children, str):
        return re.findall(r'(\w+)\s*\((\d+)\)', children)
    return []


df = pd.read_json('combined_data.json', lines=True)


expected_columns = ['firstname', 'telephone_number', 'email', 'password', 'role', 'created_at', 'children']
if not all(column in df.columns for column in expected_columns):
    raise ValueError(f"DataFrame is missing one of the expected columns: {expected_columns}")


df['telephone_number'] = df['telephone_number'].astype(str).str.replace(r'\D', '', regex=True)
df['telephone_number'] = df['telephone_number'].str.lstrip('0')


pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]{1,4}$"
df = df[df['email'].astype(str).str.contains(pattern, na=False)]


df.sort_values('created_at', ascending=False, inplace=True)
df.drop_duplicates(subset=['telephone_number', 'email'], keep='first', inplace=True)


df['children'] = df['children'].apply(parse_children)


df.to_json('cleaned_data.json', orient='records', lines=True)

print("Cleaned data has been saved in JSON format.")
