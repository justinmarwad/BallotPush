import csv, os

## READ SPREADSHEET FOR NAMES AND CREATE FOLDERS IF DOES NOT EXIST ## 
with open("debaters.csv") as csv_file:
    for row in csv.reader(csv_file, delimiter=","):
        first_name = row[0] 
        last_name = row[1] 
        email = row[3]
        
        dirname = f"{last_name}_{first_name}"
        if not os.path.exists(dirname):
            os.makedirs(dirname)