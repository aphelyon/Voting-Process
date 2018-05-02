# This document details the process to run an election through our voting system.

## How to create a valid election allowing users to vote
  
  These steps detail how an election and candidates are created, how candidates are added to an election, and how elections become active.
  
  These steps are all done by the superuser before an election takes place.
  
  You first must be logged in as superuser 
  
  To create a superuser:
    
      go to your terminal

      docker-compose up (if it isn't currently running)

      open a new terminal window

      docker exec -it vote_web_1 bash

      python web/manage.py createsuperuser

### Create an election
  
  Navigate to Create Election at /create_election
  
  You need to input the election date in the format (YYYY-MM)
  
  The dropdown menu for selecting an election type only has two types: General or Primary
  
  Since our election date is a unique identifier, you can't have more than one election for a specific month. 
  
### Create a candidate
  You first must create an election for which the candidate is running in (see above step)
  
  Navigate to /create_candidate or find 'Create Candidate' under 'Candidate Actions' in the top navigation bar.
  
  Enter the first name of the candidate
  
  Enter the last name of the candidate
  
  Enter the date of birth of the candidate in the format (YYYY-MM-DD)
        
### Create a ballot entry for that candidate
  You first must create an election, and then also create candidate(s) running within that election (see above steps)
  
  Navigate to /create_ballot_entry or find 'Create Ballot Entry' under 'Ballot Actions' in the top navigation bar.
  
  Select a candidate from the list of all the possible candidates. Candidates are listed by their first and last name, along with their birth year.
  
  Select an election from the list of all the possible elections
  
  Enter the position the candidate is running for
  
  Enter the political party the candidate is running under
  
  Enter the precinct ID for the election. If you would like to add a ballot entry to all precincts, simply enter the word "all" for the  precinct ID.

### Select current election
  You first must create an election, candidate(s) running within that election, and valid ballots (see above steps)
  
  Navigate to /election_selection, or under the 'Election Actions' dropdown, choose 'Select Election'
  
  Select whichever election you want to be active, given that there are candidate and ballot entries assigned to each election
  
  Enter in the precinct ID 
  
  If an election has not been selected, there will be red text indicating so at the top of this page. Once the election has been selected, there will be green text at the top displaying which election is currently active. 
  
  Once you have an election active, the system is now ready to begin the registration check and the voting process.
  
  The current election must be manually selected on all machines by the super user prior to beginning the voting process.
  
### Create a poll worker  
The superuser can create poll workers. To do this, go to /admin and sign in as the super user and create the poll workers. The poll workers are allowed to access the registration page.

## Election day process

These following steps detail which pages are used and how during the day of the election. This includes both the voter registration check as well as the voting and exit booth process. Note that if super user logs out, the current election selection is reset, so superuser must repeat steps from "Select current election" above. Election will still exist, but must be re-selected

### Voter registration check

A pollworker is logged into the system and accesses the registration check page at /registration_check.

Given voter's information, they must enter in the voter's first name, last name, and street address into the appropriate fields. 

After they hit submit, they will be directed to a page that indicates whether or not the voter is registered to vote at that polling location. If the voter is eligible to vote, a QR code will be displayed on the screen. The poll worker should use ctrl + p to print the QR code to a thermal receipt printer. After printing, the poll worker can refresh the page to return to the registration check page. If the voter is ineligible to vote, an error message will be displayed.

### Voter logs in and votes

Voter login page can be accessed at /voter_login. Once directed to this page, the voter scans in their QR code which will input in their code number in the corersponding field. They must also input in their first name, last name, and street address exactly as it appears on their identification card (or in this case, exactly as it appears in the API). 

After logging in, the voter will be directed to the instruction pages, at /instructions1 and /instructions2. These pages describe to the voter how to navigate the system and vote. You can only access these pages after logging in as a voter.

If the election is a primary election, the voter will be prompted to select the type of ballot they want: "Republican" or "Democrat".

The user will then be directed to the /vote/# pages. There is a separate vote page for each position or referendum that the voter can vote on. You can only access these pages after logging in as a voter. Here, on each page, the voter can select a candidate they want to vote for, or choose to abstain from voting. If voting on a referendum, they can choose to be 'In favor' or 'Not in favor' of the referendum, or to abstain from voting. 

On the top navigation bar, the voter can navigate or jump back and forth between the different vote pages. 

After hitting 'Submit' on the last vote page, the voter is presented with a confirmation page that shows who they voted for on each position. They can confirm their votes by hitting 'Confirm', or go back to change their votes. 

Finally, they will be directed to the /voter_finished page, which will thank them for voting and tell them to go to the voter exit booths. 

### Voter exit booth

The voter exit booth can be found at /voter_exit_booth. 

Here, the voter can scan in their QR code and input their first and last names, and their street address. A page with their electronic vote record will be displayed to give them confidence that their vote was recorded correctly.

### Physical ballot booth

There will be a receipt which prints at the time of submission. Each receipt contains the voter's unique hash as well as all of the ballot entries and the voter's choices for each entry. A poll worker should be at this station to rip the receipts from the thermal printer. 
