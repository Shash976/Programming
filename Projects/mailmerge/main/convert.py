import pandas as pd
import csv
import json
import sys

path = sys.argv[1]

'''---------------------------------------------------------------------------x------------------------------------------------x-------------------------------------------'''
def excel_to_json(path):
    csv_path= excel_to_csv(path)
    return csv_to_json(csv_path)

'''---------------------------------------------------------------------------x-------------------------------x--------------------------------------------------------------'''
# read an excel file and convert 
# into a dataframe object
def excel_to_csv(filepath):
    df = pd.DataFrame(pd.read_excel(filepath))
    i = filepath.rindex('.')
    csv_filepath = filepath[:i] + '_con.csv'
    json_filepath = filepath[:i] + '_conj.json'
    df.to_csv(csv_filepath, index=None, header=True)
    return csv_filepath

'''---------------------------------------------------------------------x-----------------------------------------------------------------x--------------------------------------'''

# Function to convert a CSV to JSON
# Takes the file paths as arguments
def csv_to_json(csvFilePath):
    jsonFilePath = csvFilePath[:csvFilePath.rindex('n')] + 'j.json'
    data = []
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf) # Open a csv reader called DictReader
        '''Convert each row into a dictionary and add it to data'''
        for row in csvReader:
             data.append(row)

    ''' Open a json writer, and use the json.dumps() function to dump data '''
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))
    
    return jsonFilePath
'''---------------------------------------------------------------------x-----------------------------------------------------------------x--------------------------------------'''

if __name__ == "__main__":
    excel_to_json(path)