from dotenv import load_dotenv
from redmail import gmail
from pathlib import Path
import csv, os, glob

## SETTINGS ##
SUBJECT = "SUBJECT"
MESSAGE = "MESSAGE"

## CREDS ##
load_dotenv()

gmail.username = os.getenv("EMAIL")
gmail.password = os.getenv("PASS")

## CODE ##
def sender(first_name, last_name, email, files): 
    file_attachments = []
    for f in files:
        file_attachments.append(Path(f))

    full_message = f"Hello {first_name} {last_name}! <br><br> {MESSAGE}"

    gmail.send(subject=SUBJECT, html=full_message, receivers=[email], attachments=file_attachments)

if __name__ == "__main__":
    with open("debaters.csv") as csv_file:
        for row in csv.reader(csv_file, delimiter=","):
            first_name = row[0]; last_name = row[1]; email = row[3]
            files = glob.glob(f"{last_name}_{first_name}/*.pdf")

            sender(first_name, last_name, email, files)