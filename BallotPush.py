# Made by Justin Marwad, 2022 (updated 2024)

import os, glob, pandas as pd, re
from redmail import gmail
from dotenv import load_dotenv

class BallotPush:
    def __init__(self, competitors_file, base_directory, email, password, subject, message):
        self.competitors_file = competitors_file
        self.base_directory = base_directory
        self.competitors = pd.read_csv(competitors_file)
        self.email = email
        self.password = password
        self.subject = subject
        self.message = message
        gmail.username = self.email
        gmail.password = self.password
    
    def find_ballot(self, first_name, last_name, pdf_files):
        first_initial = first_name[0].upper()
        last_initial = last_name[0].upper()
        last_name_upper = last_name.upper()
        first_name_upper = first_name.upper()
        
        # Pattern to match last_name first, then first_name or vice versa
        pattern1 = re.compile(rf"{last_name_upper}{first_initial}.*\.pdf", re.IGNORECASE)
        pattern2 = re.compile(rf"{first_name_upper}{last_initial}.*\.pdf", re.IGNORECASE)
        
        matching_pdfs = [pdf for pdf in pdf_files if pattern1.search(os.path.basename(pdf)) or pattern2.search(os.path.basename(pdf))]
        return matching_pdfs

    def find_ballots(self):
        pdf_files = []
        for subdir, _, _ in os.walk(self.base_directory):
            pdf_files.extend(glob.glob(os.path.join(subdir, "*.pdf")))

        results = {}
        for index, row in self.competitors.iterrows():
            first_name = row['First Name']
            last_name = row['Last Name']
            email_address = row.get('Email', None)  # Optional email column in competitors.csv
            full_name = f"{first_name} {last_name}"

            matching_pdfs = self.find_ballot(first_name, last_name, pdf_files)
            
            if matching_pdfs:
                print(f"Competitor: {first_name} {last_name}")
                for pdf in matching_pdfs:
                    print(f"\t - Matched PDF: {pdf}")
                if email_address:
                    if email_address not in results:
                        results[email_address] = {'full_name': full_name, 'pdfs': []}
                    results[email_address]['pdfs'].extend(matching_pdfs)
            else:
                print(f"No match found for {first_name} {last_name}")
        return results

    def send_email(self, to_email, full_name, pdf_paths):
        message = f"{full_name}, <br><br> {self.message}"
        
        # Check file paths before sending
        for pdf in pdf_paths:
            if not os.path.isfile(pdf):
                print(f"[-] ERROR: {pdf} does not exist or cannot be read.")
                return

        # Read and attach files
        attachments = {}
        for pdf in pdf_paths:
            try:
                with open(pdf, "rb") as file:
                    attachments[os.path.basename(pdf)] = file.read()
            except Exception as e:
                print(f"Error reading {pdf}: {e}")
                return
        
        gmail.send(
            subject=self.subject,
            sender=self.email,
            receivers=[to_email],
            cc=["justinmarwad@gmail.com"],
            html=message,
            attachments=attachments
        )
        print(f"Email sent to {to_email} with attachments {', '.join(attachments.keys())}")

    def send_emails(self, email_pdf_dict):
        for to_email, data in email_pdf_dict.items():
            self.send_email(to_email, data['full_name'], data['pdfs'])

if __name__ == "__main__":
    load_dotenv()  # Load environment variables from .env file
    
    email = os.getenv('EMAIL')
    password = os.getenv('PASSWORD')
    subject = os.getenv('SUBJECT', "Default Subject")
    message = os.getenv('MESSAGE', "Default Message")
    
    matcher = BallotPush(
        competitors_file="competitors.csv",
        base_directory="Ballot_Files", 
        email=email,
        password=password,
        subject=subject,
        message=message
    )
    email_pdf_dict = matcher.find_ballots()
    matcher.send_emails(email_pdf_dict)
