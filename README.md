# Ballot Push 

## Purpose

The purpose of this project is to create a quick automated system of sending out ballots stored as PDFs in folders named after the competitors. 

In the "output" folder, folders are created to the format of "Round_X" for each round - where X could be 1, 2, 3, etc or could be "Finals" or "Semis" or "Quarters" etc. Inside each folder, ballots are named to the format "FirstL_FirstL_Round_X.pdf" where the first "FirstL" is the first debater and the second "FirstL" is the second debater.


## Usage 

### Setting Up Email 

Follow the redmail instructions here: https://red-mail.readthedocs.io/en/stable/tutorials/config.html#config-gmail 

In short, you'll need to (1) Enable 2FA and (2) Create an app password. Then, rename the example.env file to just .env and fill in the appropriate information (make sure the password field is your app password). 

### Notes

#### Separate PDFs

The PDFs must be separate files. If they are not, you can use the following command to separate them (and use choco or apt to install "pdftk"):

```
pdftk Round_X.pdf burst output round_X_page_%04d.pdf
```

If you need to rotate pages then use: 
    
```
pdftk Round_X.pdf cat 1-endeast output Round_X_Rotated.pdf
pdftk Round_X_Rotated.pdf burst output Round_X/round_X_page_%01d.pdf  
```