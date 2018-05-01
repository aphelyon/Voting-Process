## How to navigate through models, and create a valid election allowing users to vote
# Create an election
  You first must be logged in as superuser (see readme.md for how to create one)
  
  Navigate to Create Election (/create_election)
  
  You need to input the election date in the format (YYYY-MM)
  
  The dropdown menu for selecting an election type only has three types: General, Primary, and Referendum
  
  Since our election date is a unique identifier, you can't have more than one type of election for a specific month. 
  
# Create a candidate
  You first must create an election for which the candidate is running in
  
  Navigate to (/create_candidate) or find 'Create Candidate' under 'Candidate Actions' in the top navigation bar.
  
  Enter the first name of the candidate
  
  Enter the last name of the candidate
  
  Enter the date of birth of the candidate in the format (YYYY-MM-DD)
        
# Create a ballot entry for that candidate
  You first must create an election, and then candidate(s) running within that election.
  
  Navigate to (/create_ballot_entry) or find 'Create Ballot Entry' under 'Ballot Actions' in the top navigation bar.
  
  Select a candidate from the list of all the possible candidates. Candidates are listed by their first and last name, along with their birth year.
  
  Select an election from the list of all the possible elections
  
  Enter the position the candidate is running for
  
  Enter the political party the candidate is running under
  
  Enter the precinct ID for the election

# Select current election
  You first must create an election, candidate(s) running within that election, and valid ballots.
  
  Navigate to (/election_selection), or under the 'Election Actions' dropdown, choose 'Select Election'
  
  Select whichever election you want to be active, given that there are candidate and ballot entries
  
  Enter in the precinct ID 
  
  If an election has not been selected, there will be red text indicating so at the top of this page. Once the election has been selected, there will be green text displaying which election is currently active. 
  
  Once you have an election active, the system is now ready to begin the registration check and the voting process.
