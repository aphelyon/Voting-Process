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

1. First name: john

2. Last name: doe

3. DOB: 01/01/1970


## Set Up Printer
For Linux:

1. Run: pip install python-escpos
2. Run: lsusb (this should show you that you have a printer connected)
3. Create the file /etc/udev/rules.d/99-escpos.rules and add the following: SUBSYSTEM=="usb", ATTRS{idVendor}=="1a2b", ATTRS{idProduct}=="1a2b", MODE="0664", GROUP="dialout" Replace idVendor and idProduct hex numbers with the ones that you got from the previous step. 
4. Run: usermod -a -G dialout yourcomputingid (if this doesn't work, run sudo !! and then run: sudo usermod -a -G dialout yourcomputingid)
5. Run: sudo python
6. Run: from escpos import printer
7. Run: p = printer.Usb(idVendor=0x0456, idProduct=0x0808, in_ep=0x81, out_ep=0x03)
8. Run: p.text("Hello World")
9. Run: p.cut()

The above sequence of steps should print "Hello World" from the thermal printer.
We need to use /dev/bus/usb/001/003 and add that to docker so we can print from Docker. 
