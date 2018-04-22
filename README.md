## Read Me!
0. This repo should only contain source code. No binaries, databases (please don't push the database), or other large files.

1. Tentative Source Control: Clone the repo locally and create your own branch. Push changes to your branch and make pull requests as needed.

2. Please set up docker, docker-compose, and Postman. Refer to the file setup_docker.md

3. Browse the repo structure to understand the project structure.

4. We will use Travis CI for continuous integration. It will check if the code you commit to your branch passes all tests. This will make pushing to master a lot easier.

## Import Links

Google Drive Folder: https://drive.google.com/drive/u/1/folders/1y6NvqFzQrZ47ByXMKgsk-_ArwnkaOov6

Slack Channel: https://goofy-goobers-uva.slack.com/


## To create a superuser
Go to your terminal

docker-compose up (if it isn't currently running)

open a new terminal window

docker exec -it vote_web_1 bash

python web/manage.py createsuperuser

## Name of valid, registered voter
After logging in with your self-made superuser...

Hash:
9e9eefe71af76610bac9bee7c5793b64

Juan
Garcia
123 Main Street
2019-11


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
