from escpos.printer import Usb
import json
from urllib import request
from time import sleep

def fetch():
	req = request.Request('127.0.0.1:8000')
	with request.urlopen(req) as response:
		result = json.loads(response.readall().decode('utf-8'))
	return result

def listen(printer, rate):
	if printer:
		while True:
			votes = fetch()
			for key in votes:
				printer.text(json.dumps(votes[key]))
				printer.cut()
			sleep(rate)

def main():
	PRINTER = None
	rate = 10
	try:
	    PRINTER = Usb(0x456, 0x808, 0, 0x81, 0x03)
	except:
	    PRINTER = None	
	listen(PRINTER, rate)

if __name__ == "__main__":
	main()

