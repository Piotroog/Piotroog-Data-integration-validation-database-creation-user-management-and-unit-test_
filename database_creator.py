import pandas as pd
import sqlite3
import json

class UserDataManager:
    def __init__(self, json_path, db_path):
        self.json_path = json_path
        self.db_path = db_path

    def load_data(self):
        with open(self.json_path, 'r') as file:
            data = [json.loads(line) for line in file]
        self.df = pd.DataFrame(data)

    def process_children(self, children):
        if not children:
            return None
        if isinstance(children, list):
            return "; ".join([" ".join(child) for child in children])
        return children

    def process_data(self):
        self.df['children'] = self.df['children'].apply(self.process_children)

    def save_to_database(self):
        conn = sqlite3.connect(self.db_path)
        self.df.to_sql('users', conn, if_exists='replace', index=False)
        conn.close()

    def execute(self):
        self.load_data()
        self.process_data()
        self.save_to_database()
        print("Database has been created and data has been imported.")


manager = UserDataManager('cleaned_data.json', 'users_database.db')
manager.execute()
