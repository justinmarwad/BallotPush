# Made by Justin Marwad, 2022 (updated 2023)

from dotenv import load_dotenv
from redmail import gmail
from pathlib import Path
import csv, os, glob, json

# FORMAT = "LastF_Round_X"

class BallotPush: 
    def __init__(self, csv, subject, message, email=None, password=None): 
        self.subject    = subject
        self.message    = message
        self.email      = email 
        self.password   = password

        self.data = open(csv) 

        # Load .env file if email and password are not provided
        load_dotenv()
        if self.email is None: 
            self.email = os.getenv("EMAIL")
        if self.password is None: 
            self.password = os.getenv("PASSWORD")
        

    def collect_ballots(self):
        """ Creates Python dictionary where the key is debater's lastname_firstname and each value is a list which contains two lists. One for full paths for pdf files which are ballots. And one for firstname, lastname, and email."""

        print("[*] Collecting ballots...")

        # Create empty dictionary
        self.ballots = {}

        # Loop over each row in the csv file
        for row in csv.reader(self.data, delimiter=","):
            firstname, lastname, email = row[0], row[1], row[2] 

            print(f"[*] Collecting ballots for {firstname} {lastname}...")

            # Parse ballots for the debater
            parsed_ballots = self.parse_ballots(firstname, lastname)
            if parsed_ballots: 

                # Add the debater to the dictionary
                self.ballots[f"{lastname}_{firstname}"] = [
                    [firstname, lastname, email], 
                    parsed_ballots
                ]

        return self.ballots

    def parse_ballots(self, firstname, lastname): 
        """ Finds a ballot given a name 
                - Enters each round folder in the output folder (named Round_X)
                - There are four rounds which are numbered 1-4 and additionally there are doubleoctas, octas, quarters, semis, and finals (though these may not exist)
                - Runs parse_ballot on each ballot in each round folder 
                - parse_ballot returns true or false depending on whether the ballot was found for the given name
        """
        # Create empty list
        found_ballots = []

        # Loop over each round folder in the output folder
        for round_folder in glob.glob("output\\Round_*"):
            # Get the round number from the folder name
            round_num = round_folder.split("_")[-1]

            # Loop over each ballot in the round folder
            for ballot_filename in glob.glob(f"{round_folder}\\*.pdf"):


                # Remove full path (i.e output\Round_X\) from ballot filename
                ballot_filename = ballot_filename.split("\\")[-1]

                # Parse the ballot
                if self.parse_ballot(ballot_filename, firstname, lastname): 
                    # If the ballot matches, add it to the list
                    found_ballots.append(os.path.join(round_folder, ballot_filename))

        return found_ballots

    def parse_ballot(self, filename, firstname, lastname): 
        """ Parses a ballot filename given a firstname and lastname and return True if matches, else return false ."""

        # print(f"[*] Parsing ballot {filename}...")

        # Split the string into three parts based on underscores
        parts = filename.split('_')

        # Extract the last name and first initial of each debater
        debater1_last_name = parts[0][:-1]
        debater1_first_initial = parts[0][-1]

        debater2_last_name = parts[1][:-1]
        debater2_first_initial = parts[1][-1]

        # Print the results
        # print("Debater 1:")
        # print("Last Name:", debater1_last_name)
        # print("First Initial:", debater1_first_initial)

        # print("\nDebater 2:")
        # print("Last Name:", debater2_last_name)
        # print("First Initial:", debater2_first_initial, "\n\n")

        # if debater1 or debater2 is the name we are looking for, return true
        if debater1_last_name == lastname and debater1_first_initial == firstname[0].upper():
            return True
        elif debater2_last_name == lastname and debater2_first_initial == firstname[0].upper():
            return True
        else:
            return False

    def send_ballots(self):
        """ Sends ballots to each debater in the ballots dictionary. """

        print("[*] Sending ballots...")

        # Loop over each debater in the ballots dictionary
        for debater in self.ballots: 

            # Get the debater's name, email, and ballots 
            firstname   = self.ballots[debater][0][0]
            lastname    = self.ballots[debater][0][1]
            email       = self.ballots[debater][0][2]
            files       = self.ballots[debater][1]

            # Send the ballots
            self.send_ballot(firstname, lastname, email, files)

    def send_ballot(self, firstname, lastname, email, files=None, full_message=None): 
        """ Sends a ballot to a debater. """
        print(f"[*] Sending {firstname} {lastname}'s ballots to {email}...")
        
        # Collect all ballots and save them to list as Path objects 
        file_attachments = [Path(f) for f in files]

        if full_message is None: 
            full_message = f"Hello {firstname} {lastname}, <br><br> {self.message}"

        gmail.username = self.email
        gmail.password = self.password
        gmail.send(
            subject=self.subject, 
            html=full_message, 
            receivers=[email], 
            attachments=file_attachments
        )


if __name__ == "__main__": 
    bp = BallotPush(
        "output/competitors.csv",
        "Ballot Delivery - Tournament Name Year",
        "Thank you for your participation in the {tournament} {year}! Your ballots have been attached to this email. <br><br> Regards, <br> {name} <br> {organization} <br>"  
    )

    # create list
    bp.collect_ballots() 

    # Send ballots
    bp.send_ballots()

