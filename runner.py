import os
import sys
import time
import re
import signal


home = os.path.expanduser('~')
status_message = []
programs_list = []

################################################################
#                                                              #
#  class program - This class is for collect program data      #
#															   #
################################################################
class program:

	def __init__(self, status= "null", day= "null", time = 0, path = "null", args = []):
		self.status = status # This variable Store "on" or "every"
		self.day = day # This varialbe store day
		self.time = time # This variable store time
		self.path = path # This variable store path
		self.args = args # This variable store argument
		self.countdown = 1000000 

	# This method is to set countdown
	def setCountdown(self):
		day_now = time.ctime().split()[0]
		if day_now == "Mon":
			day_now = 0
		elif day_now == "Tue":
			day_now = 1
		elif day_now == "Wed":
			day_now = 2
		elif day_now == "Thu":
			day_now = 3
		elif day_now == "Fri":
			day_now = 4
		elif day_now == "Sat":
			day_now = 5
		elif day_now == "Sun":
			day_now = 6
		if self.day == "Mon":
			day_program = 0
		elif self.day == "Tue":
			day_program = 1
		elif self.day == "Wed":
			day_program = 2
		elif self.day == "Thu":
			day_program = 3
		elif self.day == "Fri":
			day_program = 4
		elif self.day == "Sat":
			day_program = 5
		elif self.day == "Sun":
			day_program = 6

		days = day_program - day_now
		hours = int(self.time[:2]) - int(time.ctime().split()[3][:2])
		mins = int(self.time[2:4]) - int(time.ctime().split()[3][3:5])
		seconds = 0 - int(time.ctime().split()[3][6:8])
		self.countdown = ((days*24 + hours)*60+mins)*60 + seconds
		if self.countdown <= 0:
			self.countdown = 7*24*60*60 + self.countdown

	# This method is to set day
	def setDay(self, day):
		self.day = day

	# This method is to set time
	def setTime(self, time):
		self.time = time

	# This method is to set status
	def setStatus(self, status):
		self.status = status

	# This method is to set path
	def setPath(self, path):
		self.path = path

	# This method is to set list of argument
	def setArgs(self, args):
		self.args =args

	# This method is to get day
	def getDay(self):
		return self.day

	# This method is to get time
	def getTime(self):
		return self.time

	# This method is to get path
	def getPath(self):
		return self.path

	# This method is to get list of argument
	def getArgs(self):
		return self.args

	# This method is to get argument in string format
	def getArgsString(self):
		args =""
		for i in self.args:
			args += i + " "
		args = args.strip()
		return args

	# This method is to get status
	def getStatus(self):
		return self.status

	# This method is to get countdown
	def getCountdown(self):
		return self.countdown
		
	# This method is to format class to human readable form
	def __repr__(self):
		return "{} {} {} {} {} countdown:{}".format(self.status, self.day, self.time, self.path, self.args, self.countdown)

###################################################################
#                                                                 #
#  class programsList - This class is for collect list of program #
#															      #
###################################################################
class programsList:

	def __init__(self):
		self.programlist = []

	# This method is to add program to programlist
	def add(self, program):
		self.programlist.append(program)

	# This method is to get list of programList
	def getList(self):
		return self.programlist

	# This method is to sort list by countdown
	def sortTime(self):
		self.programlist.sort(key = lambda x: x.countdown)

	# This method is to get sleep duration for frist element in list
	def getSleepDuration(self):
		return self.programlist[0].countdown 

	# This method is to remove first program in list
	def removeLastRunProgram(self):
		self.programlist.pop(0)

	# This method is to recalculate program countdown time
	def setProgramCountdown(self):
		for i in self.programlist:
			i.setCountdown()

	# This method is to check for duplicate time for "at"
	def checkDuplicateTimeAt(self, dayTimeLists ):
		for i in dayTimeLists:
			if len(i) == 1:
				pass
			if len(i) > 1:
				for j in i[1:len(i)]:
					for k in self.programlist:
						if k.getDay() == i[0]:
							if k.getTime() == j:
								return True
		return False

	# This method is to check for duplicate time for "on" and "every"
	def checkDuplicateTime(self, day, time ):
		for i in self.programlist:
			for j in day:
				if i.getDay() == j:
					for k in time:
						if i.getTime() == k:
							return True
		return False

	# This method is to get path of the first element in list
	def getPath(self):
		return self.programlist[0].getPath()

	# This method is to get argument of the fist element in list
	def getArgs(self):
		return self.programlist[0].getArgs()

	# This method is to get status of the first element in list
	def getStatus(self):
		return self.programlist[0].getStatus()

	# This method is to get argument in string format of the first element in list
	def getArgsString(self):
		return self.programlist[0].getArgsString()

	# This method is to get size of the list
	def checkSize(self):
		return len(self.programlist)
		
	# This method is to format class to human readable form 
	def __repr__(self):
		allprogram = ""
		for i in self.programlist:
			allprogram += i.__repr__() +"\n"
		return allprogram

#########################################################
#                                      			        #
# write_process_id(): - is to write PID to .runner.pid. #
#												        #
#########################################################
def write_process_id():
	try:
		file = open(home + "/.runner.pid", 'w')
		file.write(str(os.getpid()))
		file.close()
	except FileNotFoundError:
		pass
	if not os.path.isfile(home + "/.runner.pid"):
		print("file .runner.pid cannot be create", file=stderr)
		exit()
			
###################################################################
#                                      				  			  #
# create_runner_status(): - is to write status to .runner.status. #
#													  			  #
###################################################################
def create_runner_status():
	try:
		file = open(home + "/.runner.status", 'w')
		file.write("")
	except FileNotFoundError:
		pass

	if not os.path.isfile(home + "/.runner.status"):
		print("file .runner.status cannot be create", file=stderr)
		exit()

#########################################################################
#                                      				                    #
# execute(path,arg): - is to create child process and create program.   #
#													            		#
#########################################################################
def execute(path,arg):

	pid = os.fork()
	signal.signal(signal.SIGALRM, handler)
	if pid == 0:  # Child process
		os.execv( path,arg)
		exit(0)
	elif pid == -1: # Error during os.fork()
		print("Fork failed", file=stderr)
	else: # Parent process
		wval = ["Timeout", 256]
		signal.alarm(59)  # Set timeout limit to 59 seconds
		try:
			wval = os.wait()
		except:
			pass
		signal.alarm(0)
		if wval[1] >> 8:
			return "error" + " " + time.ctime()  # If there is error, return error
		else:
			return "ran" + " " + time.ctime() # If program execute succesfully, return ran

#################################################################
#                                      				            #
# run(): - program loop after start up.                         # 
#													            #
#################################################################
def run():

	global status_message
	global programs_list

	if not programs_list.checkSize():
		exit()
	while True:
		time.sleep(programs_list.getSleepDuration())   # Sleep until next program
		result = execute(programs_list.getPath() , programs_list.getArgs()) # Time up, execute program
		status_message.append(result+ " " +programs_list.getArgsString()) # Execute done, save status message

		if programs_list.getStatus() == "on": # If program that just execute is "on" 
			programs_list.removeLastRunProgram() # Remove program

			if programs_list.getList() == []: # If there is nothing left to run, terminate runner.py
				print("nothing left to run")
				exit()
			programs_list.setProgramCountdown()  # Set program time
			programs_list.sortTime() # Sort list by time

		elif programs_list.getStatus() == "every": # If program that just execute is "every"
			programs_list.setProgramCountdown() # Set program time 
			programs_list.sortTime() # Sort list by time 

#################################################################
#                                      				            #
# handler(): - is to set program timer during fork/exec to 59.  # 
#													            #
#################################################################
def handler(signum, frame):  

	print("timeout 59 seconds")
	raise Exception("end of time")


#################################################################
#                                      				            #
# receive_signal(): - function triggle when receive SIGUSR1     # 
#													            #
#################################################################
def receive_signal(signum, frame):

	try:
		file = open(home+"/.runner.status","w") # Open .runner.status in write mode

		for i in status_message: # Write ran and error programs
			file.write(i + "\n")
		programs_list_dup = programs_list
		programs_list_dup.setProgramCountdown()

		for i in programs_list_dup.getList(): # Write upcoming program
			file.write("will run at " + time.ctime(time.time() + i.getCountdown()) + " " + i.getArgsString() + "\n")
		file.close() # Close file
	except FileNotFoundError:
		print("file .runner.status is not found", file = stderr) 

#################################################################
#                                      				            #
# get_days(): - Check for valid day and parse into list         # 
#													            #
#################################################################
def get_days(days):

	days = days.split(",") # Split days by ","
	day_list = []
	for i in days:
		if i == "Monday":
			day_list.append("Mon")
		elif i == "Tuesday":
			day_list.append("Tue")
		elif i == "Wednesday":
			day_list.append("Wed")
		elif i == "Thursday":
			day_list.append("Thu")
		elif i == "Friday":
			day_list.append("Fri")
		elif i == "Saturday":
			day_list.append("Sat")
		elif i == "Sunday":
			day_list.append("Sun")
		else:
			return False
	index = 1
	for i in day_list: # Check for duplicate day 
		for j in day_list[index:len(day_list)]:
			if i == j:
				return False
		index += 1
	return day_list

#################################################################
#                                      				            #
# get_days(): - Check for valid time and parse into list        # 
#													            #
#################################################################
def get_times(times):

	times = times.split(",") # Split times by ","
	time_list = []
	for i in times:
		if len(i) != 4: # If time length not equal 4, it is invalid
			return False
		if i.isdigit(): # Check for valid time
			if int(i[:2]) > 23 or int(i) < 0 or int(i[2:4]) > 59 or int(i) >= 2500 or int(i) < 0:
				return False
			else:
				time_list.append(i)
		else:
			return False
	index = 1
	for i in time_list: # Check for duplicate time
		for j in time_list[index:len(time_list)]:
			if i == j:
				return False
		index += 1
	return time_list

######################################################################
#                                      				                 #
# convert_day(time): - convert time "at" day/time to "on" day/time   #
#					 - return [[day1,time1,time2.. ],[day2,time1,..]]#
#													                 #
######################################################################
def convert_day(timee):

	day = time.ctime()[:3] # Parse day from ctime
	hour = time.ctime()[11:13] # Parse hour from ctime
	minute = time.ctime()[14:16] # Parse minute from ctime
	today = [day] # Make a list, index 0 is day, index 1+ is time 
	if day == "Mon":
		tommorrow = ["Tue"] # Make a list, index 0 is day, index 1+ is time
	elif day == "Tue":
		tommorrow = ["Wed"] # Make a list, index 0 is day, index 1+ is time
	elif day == "Wed":
		tommorrow = ["Thu"] # Make a list, index 0 is day, index 1+ is time
	elif day == "Thu":
		tommorrow = ["Fri"] # Make a list, index 0 is day, index 1+ is time
	elif day == "Fri":
		tommorrow = ["Sat"] # Make a list, index 0 is day, index 1+ is time
	elif day == "Sat":
		tommorrow = ["Sun"] # Make a list, index 0 is day, index 1+ is time
	elif day == "Sun":
		tommorrow = ["Mon"] # Make a list, index 0 is day, index 1+ is time
	days = [today, tommorrow] 
	timeee =timee.split(",")
	for i in timeee:
		if int(hour + minute ) > int(i): # Compare current time and given time
				tommorrow.append(i) # If current time > given time, add time to tomorrow list
		else:
			today.append(i) # If current time <= given time, add time to today list
	return days  

#######################################################################
#                                      				                  #
# getArg(line, start ,end): - funciton to split line into list of arg #         
#													                  #
#######################################################################
def getArg(line, start,end):
	arg =[]
	for i in line.split()[start:end]:
		arg.append(i)

	return arg

#############################################################################
#																			#
# check_valid_path(path): -Check for exist program, and prgram siz must > 0 #
#																			#
#############################################################################
def check_valid_path(path):
	if not os.path.isfile(path):
		return False
	if os.stat(path).st_size == 0:
		return False
	return True

#############################################################################
#																			#
# read_conf(path): - Parse configuration file in to list of program         #
#																			#
#############################################################################
def read_conf():

	if not os.path.isfile(home+"/.runner.conf"):  # If ./runner.conf not exist, exit
		print("configuration file not found", file=sys.stderr)
		exit()

	filesize = os.path.getsize(home+"/.runner.conf") 
	if filesize == 0: # If ./runner.conf is empty, exit
		print("configuration file empty", file=sys.stderr)
		exit()

	file = open(home+"/.runner.conf","r") # Read .runner.conf
	programs = programsList()
	program_tmp = program()
	error_check = False
	while True: # Read conf until EOF
		line = file.readline()
		if line == '':
			break
		lineArray = line.split() # Split line in to list
		line_length = len(lineArray)
		if line_length < 4: # Check valid line length
			print("error in configuration: {}".format(line), end = '' , file=sys.stderr)
			error_check = True;
			continue
		else:
			if lineArray[0] == "at": # Check valid line begin with at
				if not get_times(lineArray[1]): # Check valid time in index 1
					print("error in configuration: {}".format(line), end = '' , file=sys.stderr)
					error_check = True;
					continue
				elif lineArray[2] != "run": # Check for run in index 2
					print("error in configuration: {}".format(line), end = '' , file=sys.stderr)
					error_check = True;
					continue
				elif not check_valid_path(lineArray[3]):
					print("error in configuration: {}".format(line), end = '' , file=sys.stderr)
					error_check = True;
				else: 
					convert_days = convert_day(lineArray[1]) # Convert day/time
					if programs.checkDuplicateTimeAt(convert_days): # Check for duplicate time
						print("error in configuration: {}".format(line), end = '' , file=sys.stderr)
						error_check = True;
					else:
						for i in convert_days[0][1:]:
							program_tmp.setStatus("on") # Set status
							program_tmp.setDay(convert_days[0][0]) # Set day
							program_tmp.setTime(i) # Set time
							program_tmp.setPath(lineArray[3]) # Set path
							if line_length > 4: 
								program_tmp.setArgs(getArg(line,3,line_length)) # Set argument
							program_tmp.setCountdown() # Set countdown
							programs.add(program_tmp) # Add program into program list
							program_tmp = program() # reset program_tmp
						if len(convert_days[1]) > 1:
							for i in convert_days[1][1:]: 
								program_tmp.setStatus("on") # Set status
								program_tmp.setDay(convert_days[1][0]) # Set day
								program_tmp.setTime(i) # Set time
								program_tmp.setPath(lineArray[3]) # Set path
								if line_length > 4: 
									program_tmp.setArgs(getArg(line, 3, line_length)) # Set argument
								program_tmp.setCountdown() # Set countdown
								programs.add(program_tmp) # Add program_tmp into program list
								program_tmp = program() # reset program_tmp
						continue
			elif lineArray[0] == "on": 
				pass
			elif lineArray[0] == "every":
				pass
			else:
				print("error in configuration: {}".format(line), end = '' , file=sys.stderr)
				error_check = True;
				continue
			if lineArray[0] == "at": 
				pass
			if len(lineArray) < 6: # Check for valid line length for "on" and "every" program
				print("error in configuration: {}".format(line), end = '' , file=sys.stderr)
				error_check = True;

			elif  not get_days(lineArray[1]):# Check for valid day in index 1
				print("error in configuration: {}".format(line), end = '' , file=sys.stderr)
				error_check = True;
				continue
			elif lineArray[2] != "at": # Check for at in index 2
				print("error in configuration: {}".format(line), end = '' , file=sys.stderr)
				error_check = True;
				continue
			elif not get_times(lineArray[3]):  # Check for time in index 3
				print("error in configuration: {}".format(line), end = '' , file=sys.stderr)
				error_check = True;
				continue
			elif lineArray[4] != "run": # Check for run in index 4
				print("error in configuration: {}".format(line), end = '' , file=sys.stderr)
				error_check = True;
				continue
			elif not check_valid_path(lineArray[5]):
				print("error in configuration: {}".format(line), end = '' , file=sys.stderr)
				error_check = True;
			else:
				days = get_days(lineArray[1])  
				times = get_times(lineArray[3])
				if programs.checkDuplicateTime(days, times): # Check for duplicate time
					print("error in configuration: {}".format(line), end = '' , file=sys.stderr)
					error_check = True;
				else:
					for i in days:
						for j in times:
							if lineArray[0] == "on":
								program_tmp.setStatus("on") # Set status
							else:
								program_tmp.setStatus("every") # Set status
							program_tmp.setDay(i) # Set day
							program_tmp.setTime(j) # Set time
							program_tmp.setPath(lineArray[5]) # Set path
							program_tmp.setArgs(getArg(line, 5, line_length)) # Set length
							program_tmp.setCountdown() # Set Countdown
							programs.add(program_tmp) # Add program_tmp to program list
							program_tmp = program() # Reset program_tmp
					continue
	file.close()
	#sort time!
	if error_check:
		exit()
	programs.sortTime()
	return programs

###################################################
#												  #			
# 				Main program                      #                                    
#											      #
###################################################
def main():
	global programs_list

	signal.signal(signal.SIGUSR1, receive_signal)
	write_process_id()  # Write process id
	create_runner_status() # Create runner status
	programs_list = read_conf() # Read configuration file
	run() # Run program

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:  #This exception is for testing purpose
		sys.exit(0)
