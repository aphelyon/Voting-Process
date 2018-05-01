from escpos.printer import Usb
import json
from urllib import request
from time import sleep

def fetch():
	req = request.Request('http://167.99.237.230:8000/print_queue/ajsda_8u8ehaso_ih09_3uawjdioah839ry_hask8a2')
	try:
		with request.urlopen(req) as response:
			result = json.loads(response.readline().decode('utf-8'))
	except:
		return {}
	return result

def listen(printer, rate):
	if printer:
		while True:
			votes = fetch()
			for key in votes:
				printer.text("VOTER BALLOT:\n")
				printer.text("--------------------\n")
				vote = votes[key]
				printer.text("VOTER_HASH: " + vote["VOTER_HASH"] + "\n")
				for pos in vote:
					if pos == "VOTER_HASH": continue
					printer.text(pos + ": " + vote[pos] + "\n")
				printer.text("--------------------\n\n")
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

