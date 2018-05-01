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

f49775986dd6892ca4fb9fe9ec176a8e6e6c4bef5c9eb05fbc67264a4f38d585

Robert

Rogers

808 Brooks Squares

2019-11

==========

Voter 3:

8a74a5ab4ca5a1f125e2fa71ec82d7ef9ecf70b65634e87af0eaaa3bc3e2d0fa

Darren

Johnson

507 Seth Street

2019-11

==========

Voter 4:

24b4eaaca5d2b44708e30f2a6e2d2865cf0bb4e6a49166235e5454af89cfb54f

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
- First, create a candidate with First Name: "In", Last Name: "favor", Date of Birth doesn't matter
- Second, create a candidate with First Name: "Not in", Last Name: "favor", Date of Birth doesn't matter

- Then, for each of the two "candidates" created above, create a ballot entry with position equal to the referendum question -- Start with  "Referendum #x." for parsing purposes, then make the Party equal to "Referendum", and assign the precinct as needed. 

## Quickly creating same ballot entry for all precincts
- Set up candidates and ballot as you normally would, but instead of putting a precinct id in the slot, put the word "all", which will automatically generate ballot entry objects for all of the precincts found in the voter registration database.
