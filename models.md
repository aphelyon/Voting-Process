## How to navigate through models 
# Create an election
  You need to input an election id in the format (YYYY-MM)
  
  The dropdown menu for selecting an election type only has three types: General, Primary, and Referendum
  
  Since our election id is a unique identifier, you can't have more than one type of election for a specific month. 
  
# Create a candidate
  Enter the first name of the candidate
  
  Enter the last name of the candidate
  
  Enter the date of birth of the candidate in the format (YYYY-MM-DD)
    
      Why is their date of birth important? 
        A contingency for candidates with the same name... (i.e George Bush Sr. vs George Bush Jr.)
        It's unlikely that they'll be the same age even if they share the same name
        
      What counts as a unique candidate object?
        A candidate counts as a unique object if any of the three fields differs from any of the existing candidate objects
        
# Create a ballot entry for that candidate
  Select a candidate from the list of all the possible candidates
  
  Select an election from the list of all the possible elections
  
  Enter the position the candidate is running for
  
  Enter the political party the candidate is currently in
    
    Why the drop down lists?
      It limits the room for error.
      Although scalability is an issue, this was solved by having the list be sorted in alphabetical order, so even if they do have to sift through all the candidates, it's in an optimal order.
    
## Issues and changes that came from sprint 3 models
  It was just bad OO design... we had multiple candidate objects for a single candidate if they differed in positions or parties...
  We solved this by adding in our Ballot Entry model, which keeps track of the position, party, and vote count. It also associates the candidate with a specific election.
  
