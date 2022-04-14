import pandas as pd
import csv
import json
import sys

path = sys.argv[1]
print("starting....")

'''---------------------------------------------------------------------------x-------------------------------x--------------------------------------------------------------'''

# Function to convert a CSV to JSON
# Takes the file paths as arguments
def csv_to_json(csvFilePath, jsonFilePath):
     
    # create a dictionary
    data = []
     
    # Open a csv reader called DictReader
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
         
        '''Convert each row into a dictionary and add it to data'''
        i = 1
        for row in csvReader:
             data.append(row)
    ''' Open a json writer, and use the json.dumps() function to dump data '''
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))
    
    return jsonFilePath

# read an excel file and convert 
# into a dataframe object
def excel_to_csv(filepath):
    df = pd.DataFrame(pd.read_excel(filepath))
    i = filepath.rindex('.')
    csv_filepath = filepath[:i] + '_con.csv'
    json_filepath = filepath[:i] + '_conj.json'
    df.to_csv(csv_filepath, index=None, header=True)
    return csv_filepath, json_filepath

'''---------------------------------------------------------------------x-----------------------------------------------------------------x--------------------------------------'''

def excel_to_json(path):
    tup = excel_to_csv(path)
    csv_path = tup[0]
    json_path = tup[1]
    return csv_to_json(csv_path, json_path)

if __name__ == "__main__":
    print(excel_to_json(path))