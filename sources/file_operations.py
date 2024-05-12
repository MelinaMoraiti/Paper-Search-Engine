import csv,json
"""
Save data in either JSON or CSV format based on the file extension.

Parameters:
- data: The data to be saved (dictionary or list of dictionaries).
- file_path: The path where the data will be saved.
"""
def save_data(data,file_path):
 if data:
    file_extension = file_path.split('.')[-1].lower()
    if file_extension == 'json':
       export_to_JSON(data, file_path)
       print(f'Data for papers saved to {file_path}')
    elif file_extension == 'csv':
        export_to_CSV(data, file_path)
        print(f'Data for papers saved to {file_path}')
    else:
        print(f"Unsupported file format: {file_extension}")

def export_to_JSON(data,file_path):
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file,ensure_ascii=False, indent=4)

def export_to_CSV(data,file_path):
    with open(file_path,'w',newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames= data[0].keys())
        # Write the header
        csv_writer.writeheader()
        # Write the data
        csv_writer.writerows(data)
def retrieve_data(file_path):
    file_extension = file_path.split('.')[-1].lower()
    if file_extension == 'json':
       data = load_from_json(file_path)
    elif file_extension == 'csv':
       data = load_from_csv(file_path)
    else:
        raise ValueError("Unsupported file format. Supported formats: 'json', 'csv'")
    return data
def load_from_json(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        papers = json.load(file)
    return papers
def load_from_csv(csv_file):
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        papers = list(reader)
    return papers

