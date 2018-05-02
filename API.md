# How to use our External API
## Create a media ID
  First, the superuser must enter the add a media partner page at http://167.99.237.230:8000/add_media_partner, and enter in the company that the api key will be given to.
  This page generates the 50 character hexadecimal API key for each of the respective companies, so that media outlets with their unique secret identifier are the only users with access to all the election and candidate information.
  
## How to access the list of all the elections
  The media outlet can access the list of all the past and current elections by navigating to 
  
    http://167.99.237.230:8000/elections/<API-KEY>
    
   **Parameters:**
   - API-KEY: the 50 character hexadecimal unique media ID generated at /add_media_partner
    
   **Responses:**
   - pk: Primary key, redundant with election_id
   - election_type: Type of election, either General, Primary, or Referendum
   - election_id: election date in format YYYY-MM
    
   _Sample Response:_
    
    {  
      "elections":[  
         {  
           "pk":"2019-11",
           "election_type":"General",
           "election_id":"2019-11"
         },
         {  
           "pk":"1996-04",
           "election_type":"Primary",
           "election_id":"1996-04"
         }
      ]
    }
    
    
## How to access information relevant to a particular election
  The media outlet can access information about a particular election by navigating to
    
    http://167.99.237.230:8000/elections/<Election Year>-<Election Month>/<API-KEY>
    
   **Parameters:**
   * Election Year: year of the election. Format: YYYY
   * Election Month: month of the election. Format: MM
   * API-KEY: the 50 character hexadecimal unique media ID generated at /add_media_partner
    
   **Responses:**
   * positions: array of all positions for which candidates are running in any given election
   * party: political party of the candidate
   * precinct_id: precinct identifier for the instance of the candidate's ballot in a specific precinct
   * last_name: last name of candidate
   * first_name: first name of candidate
   * num_votes: number of votes the candidate has received in the specific precinct
    
   _Sample Response:_
    
    {  
      "positions":{  
        "Governor":[  
          {  
            "party":"Republican",
            "precinct_id":"0405",
            "last_name":"Carpenter",
            "first_name":"Courtney",
            "num_votes":219
          },
          {  
            "party":"Democrat",
            "precinct_id":"0405",
            "last_name":"Anderson",
            "first_name":"Mark",
            "num_votes":220
          }
        ],
        "President":[  
          {  
            "party":"Republican",
            "precinct_id":"0405",
            "last_name":"West",
            "first_name":"Kanye",
            "num_votes":1831032
          },
          {  
            "party":"Democrat",
            "precinct_id":"0405",
            "last_name":"Winfrey",
            "first_name":"Oprah",
            "num_votes":9734
          }
        ]
      },
      "success":true
    }
    
   
## How to access the list of all the possible candidates
  The media outlet can access the list of all the past and current candidates by navigating to
    
    http://167.99.237.230:8000/candidates/<API-KEY>
    
   **Parameters:**
   * API-KEY: the 50 character hexadecimal unique media ID generated at /add_media_partner
    
   **Responses:**
   * pk: primary key of candidate, dynamically generated as iterative int at candidate creation
   * last_name: last name of candidate
   * first_name: first name of candidate
   * dob: candidate date of birth. Format: YYYY-MM-DD
    
   _Sample Response:_
    
    {  
      "candidates":[  
        {  
          "pk":1,
          "last_name":"West",
          "first_name":"Kanye",
          "dob":"1996-05-18"
        },
        {  
          "pk":2,
          "last_name":"Winfrey",
          "first_name":"Oprah",
          "dob":"1954-04-11"
        },
        {  
          "pk":3,
          "last_name":"Carpenter",
          "first_name":"Courtney",
          "dob":"1997-09-29"
        },
        {  
          "pk":4,
          "last_name":"Anderson",
          "first_name":"Mark",
          "dob":"1996-05-18"
        }
      ]
    }
    

## How to access information about a particular candidate
  The media outlet can access information about a particular candidate by simply navigating to
  
    http://167.99.237.230:8000/candidates/<Candidate First Name>-<Candidate Last Name>-<Candidate Year of Birth>/<API-KEY> 
    
   **Parameters:**
   * Candidate First Name: first name of candidate being queried
   * Candidate Last Name: last name of candidate being queried
   * Candidate Year of Birth: year of birth for candidate being queried. Format: YYYY
   * API-KEY: the 50 character hexadecimal unique media ID generated at /add_media_partner
    
   **Responses:**
   * Elections: specific election that a candidate ran in, by month. Format: YYYY-MM
   * position: position that the candidate ran for in a specific election
   * party: political party the candidate ran under in a specific election
   * num_votes the number of votes the candidate received when running for that specific election
    
   _Sample Response:_
   
    {  
      "success":true,
      "Elections":{  
        "1996-04":[  
          {  
            "position":"President",
            "party":"Democrat",
            "num_votes":13832
          }
        ],
        "2019-11":[  
          {  
            "position":"President",
            "party":"Democrat",
            "num_votes":22932
          }
        ]
      }
    }
    
