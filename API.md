## How to use our internal API
# Create an media ID
  First, the superuser must enter the add a media id page, and enter in the company that the api key will be given to.
  This page generates the API key for each of the respective companies, so that the only users that will have access to all the election and candidate information are the media outlets.
  
# How to access the list of all the elections
  The media outlet can access the list of all the past and current elections by simply navigating to 
  
    /elections/<API-KEY>
    
# How to access information relevant to a particular election
  The media outlet can access information about a particular election by simply navigating to
    
    /elections/<Election Year>-<Election Month>/<API-KEY>
   
# How to access the list of all the possible candidates
  The media outlet can access the list of all the past and current candidates by simply navigating to
    
    /candidates/<API-KEY>

# How to access information about a particular candidate
  The media outlet  can access information about a particular candidate by simply navigating to
  
    /candidates/<Candidate First Name>-<Candidate Last Name>-<Candidate Year of Birth>/<API-KEY> 
