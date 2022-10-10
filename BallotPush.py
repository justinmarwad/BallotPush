# Made by Justin Marwad, 2022 

from dotenv import load_dotenv
from redmail import gmail
from pathlib import Path
import csv, os, glob

class BallotPush: 
    def __init__(self, csv, subject, message, email=None, password=None): 
        self.subject = subject
        self.message = message
        self.email = email 
        self.password = password

        self.data = open(csv) 

        load_dotenv()
        if self.email is None: 
            self.email = os.getenv("EMAIL")
        if self.password is None: 
            self.password = os.getenv("PASSWORD")
        

    def create_folders(self, dirname=None):
        for row in csv.reader(self.data, delimiter=","):
            first_name = row[0] 
            last_name = row[1] 
            email = row[3]
            
            if dirname is None: 
                dirname = f"{last_name}_{first_name}"

            if not os.path.exists(dirname):
                os.makedirs(dirname)

    def send_ballot(self, first_name, last_name, email, full_message=None, files=None): 
        file_attachments = []
        for f in files:
            file_attachments.append(Path(f))

        if full_message is None: 
            full_message = f"Hello {first_name} {last_name}! <br><br> {self.message}"

        gmail.username = self.username
        gmail.password = self.password 
        gmail.send(subject=self.subject, html=full_message, receivers=[email], attachments=file_attachments)

    def send_ballots(self): 
        for row in csv.reader(self.data, delimiter=","):
            first_name = row[0]; last_name = row[1]; email = row[3]
            files = glob.glob(f"{last_name}_{first_name}/*.pdf")

            self.send_ballot(first_name, last_name, email, files)


if __name__ == "__main__": 
    bp = BallotPush()

    # Create folders
    bp.create_folders()

    # Send ballots
    bp.send_ballots()

