## Read Me!
0. This repo should only contain source code. No binaries, databases (please don't push the database), or other large files.

1. Tentative Source Control: Clone the repo locally and create your own branch. Push changes to your branch and make pull requests as needed.

2. Please set up docker, docker-compose, and Postman. Refer to the file setup_docker.md

3. Browse the repo structure to understand the project structure.

4. We will use Travis CI for continuous integration. It will check if the code you commit to your branch passes all tests. This will make pushing to master a lot easier.

## Import Links

Google Drive Folder: https://drive.google.com/drive/u/1/folders/1y6NvqFzQrZ47ByXMKgsk-_ArwnkaOov6

Slack Channel: https://goofy-goobers-uva.slack.com/

Digital Ocean: http://167.99.237.230:8000


## To create a superuser
Go to your terminal

docker-compose up (if it isn't currently running)

open a new terminal window

docker exec -it vote_web_1 bash

python web/manage.py createsuperuser

## Name of valid, registered voters
After logging in with your self-made superuser...

Precinct is "0405"

==========


Voter 1:

03c089cc206823df2fa4d3ef942882a24ea673efdfbb022c1620d42100e79c3d

Jessica

Edwards

513 Andrew Trace

2019-11

==========

Voter 2:

c6cb43345da687c4a602078265c6d60a3574d89e27bcb7995e06548ea77f7bba

Robert

Rogers

808 Brooks Squares

2019-11

==========

Voter 3:

72d0683d4241b7751b198077f17f06f7f14b13548b18ad78190d0c790a8fcf40

Darren

Johnson

507 Seth Street

2019-11

==========

Voter 4:

ae93669c45a812582a43cecdaf42c08f06766e0ab3fe4b7e1c8f3a3c437ba083

Patrick

Trevino

520 Nicole Island

2019-11

==========

## Set Up Printer
For Linux:

1. Run: python
2. Run: from escpos.printer import Usb
3. Run: p = Usb(0x456,0x808,0,0x81,0x03)
4. Run: p.qr("12345",size=7)
5. Run: p.cut()



The above sequence of steps should print "Hello World" from the thermal printer.

## Referendum Support
- Everyone needs to create a candidate First Name: In, Last Name: favor, dob doesn't matter
- ditto for First Name: Not in, Last Name: favor, dob doesn't matter

- then create ballot entry with position equal to referendum question -- Start with  "Referendum #x." for parsing purposes 

## API Key

-For media company "Eric" the key is:
- 9dcd336a8effa0e994aea532a5e949702ae96bf6caf14436c9
