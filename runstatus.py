import os
import sys
import time
import re
import signal


home = os.path.expanduser('~')

def main():

	if not os.path.isfile(home+"/.runner.pid"): # Check for PID file
		print("PID file is missing", file=stderr)
		exit()
	filesize = os.path.getsize(home+"/.runner.pid") # Check for size of PID file
	if filesize == 0:
		print("PID file is empty", file=stderr)
		exit()

	file = open(home+"/.runner.pid","r") # Open .runner.pid in read mode
	pid = file.readline()
	file.close()
	os.kill(int(pid), signal.SIGUSR1) # sent SIGUSR1 signal
	seconds = 5
	check_size = False

	if not os.path.isfile(home+"/.runner.status"):
		print("Status file is missing", file=stderr)
		exit()

	while seconds: # Check every 1 second for 5 second
		time.sleep(1)
		filesize = os.path.getsize(home+"/.runner.status")
		if filesize > 0: # If file size is not 0 anymore, exit loop 
			check_size = True 
			break
		seconds -= 1

	if check_size: 
		file = open(home+"/.runner.status","r") # Open .runner.status in read mode
		line= file.readline() 
		while True:  # Print all contents to stdout
			if line == "":
				break
			print(line,end='')
			line = file.readline()  
		file.close() # Close file
		file = open(home+"/.runner.status","w") # Open .runner.status in write mode
		file.write("") # Truncate it to zero length
		file.close() # Close file

	else: # Status not arrive in 5 second, print status timeout
		print("status timeout", file=stderr) 

if __name__ == "__main__":
  main()