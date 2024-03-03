import os
import pandas as pd
import json
import xml.etree.ElementTree as ET


csv_file_path_a_b = os.path.join('data', 'a', 'b', 'users_1.csv')
xml_file_path_a_b = os.path.join('data', 'a', 'b', 'users_1.xml')
csv_file_path_a_c = os.path.join('data', 'a', 'c', 'users_2.csv')
json_file_path_a = os.path.join('data', 'a', 'users.json')
xml_file_path = os.path.join('data', 'users_2.xml')


def load_csv_data(file_path):
    return pd.read_csv(file_path, sep=';')

def load_json_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def load_xml_data(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    xml_data = []
    for user in root.findall('user'):
        user_data = {child.tag: child.text for child in user}
        xml_data.append(user_data)

    return pd.DataFrame(xml_data)


csv_data_a_b = load_csv_data(csv_file_path_a_b)
xml_data_a_b = load_xml_data(xml_file_path_a_b)
csv_data_a_c = load_csv_data(csv_file_path_a_c)
json_data_a = pd.DataFrame(load_json_data(json_file_path_a))
xml_data = load_xml_data(xml_file_path)


all_data = pd.concat([csv_data_a_b, xml_data_a_b, csv_data_a_c, json_data_a, xml_data], ignore_index=True)


all_data.to_json('combined_data.json', orient='records', lines=True)

print("All data have been combined and saved in JSON format.")
