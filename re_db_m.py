import csv

def read():
    data = []
    with open("healthcare-dataset-stroke-data.csv", mode='r') as stroke_data:
        # Using DictReader to read each row as a dictionary
        reader = csv.DictReader(stroke_data)
        
        # Append each row (as a dictionary) to the data list
        for row in reader:
            data.append(row)
    
    return data
