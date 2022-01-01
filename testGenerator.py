import os
import sys
import time


def getTime():

	day = time.ctime()[:3]
	hour = time.ctime()[11:13]
	minute = time.ctime()[14:16]
	return day+hour+minute

def convertTime(time, n):

	day = time[:3]
	hours = time[3:5]
	mins = time[5:7]
	minsOut = int(mins) + n
	hoursOut = int(hours)
	incrementMins = False
	incrementHours = False
	decrement = False
	if minsOut < 0:
		minsOut + 60
		hoursOut - 1
		if hoursOut == -1:
			hoursOut = 23
			decrement = True
	if minsOut >= 60:
		incrementMins = True
		minsOut -= 60
	if incrementMins:
		hoursOut += 1
	timeOut = ""
	if hoursOut >= 24:
		incrementHours = True
		hoursOut -= 24
	if hoursOut < 10:
		timeOut += "0"
	timeOut += str(hoursOut)

	if minsOut < 10 or minsOut == 60:
		timeOut += "0"
	if minsOut == 60:
		timeOut += "0"
	else:
		timeOut += str(minsOut)
	if incrementMins and incrementHours:
		if day == "Mon":
			dayOut = "Tuesday"
		elif day == "Tue":
			dayOut = "Wednesday"
		elif day == "Wed":
			dayOut = "Thursday"
		elif day == "Thu":
			dayOut = "Friday"
		elif day == "Fri":
			dayOut = "Saturday"
		elif day == "Sat":
			dayOut = "Sunday"
		elif day == "Sun":
			dayOut = "Monday"
	elif decrement:
		if day == "Mon":
			dayOut = "Sunday"
		elif day == "Tue":
			dayOut = "Monday"
		elif day == "Wed":
			dayOut = "Tuesday"
		elif day == "Thu":
			dayOut = "Wednesday"
		elif day == "Fri":
			dayOut = "Thursday"
		elif day == "Sat":
			dayOut = "Friday"
		elif day == "Sun":
			dayOut = "Saturday"		
	else:
		if day == "Mon":
			dayOut = "Monday"
		elif day == "Tue":
			dayOut = "Tuesday"
		elif day == "Wed":
			dayOut = "Wednesday"
		elif day == "Thu":
			dayOut = "Thursday"
		elif day == "Fr":
			dayOut = "Friday"
		elif day == "Sat":
			dayOut = "Saturday"
		elif day == "Sun":
			dayOut = "Sunday"
	return [dayOut, timeOut]
def getNextDay(day):

	if day == "Monday":
		return "Tuesday"
	elif day == "Tuesday":
		return "Wednesday"
	elif day == "Wednesday":
		return "Thursday"
	elif day == "Thursday":
		return "Friday"
	elif day == "Friday":
		return "Saturday"
	elif day == "Saturday":
		return "Sunday"
	elif day == "Sunday":
		return "Monday"

#########################################################################################
#											                  							#
#	>>> TEST 1 - CORRECT/INCORRECT CONFIGURATION  										#	   
#	- repeated day 																		#
#	- repeated time 																	#
#	- incorrect time 																	#
#	- incorrect dayname																	#
#	- no run keyword 													    			#
#	- bad syntax 																		#
#	- duplicate run time 																#
#	- program path missing 																#
#	- incorrect time 																	#
#	- day missing 																		#
#	- correct complex program argument                                                  #
#   - check for valid program (path exist, size > 0)									#
# 											                  							#
# 	>>> .runner.configuration 															#
#	every Friday 0230 run /bin/echo THIS IS NOT ERROR   		       				    #
#   every Monday,Tuesday at 1300,1301 run /bin/date                                     #
#   on Tuesday at 0000 run /bin/date                                                    #
#	every Tuesday,Wednesday,Tuesday at 1200,1201 run /bin/date              			#
#	every Tues at 1202 run /bin/date                                        			#
#	every Tuesday at 11000 run /bin/date                                    			#
#   every tuesday at 1203 run /bin/date                                     			#
#	on Tuesday at 1204 /bin/date                                            			#
#   on every Tuesday at 1205 run /bin/date                                  			#
#   on Tuesday at 2400 run /bin/date                                        			#
#   on Tuesday at 1206 run /bin/date   													#			
#   on Tuesday at 1206 run /bin/date                                        			#
#   on Tuesday at 1207 run                                                  			#
#   on Tuesday at 1260 run /bin/date                                        			#
#   on Tuesday at 123 run /bin/date                                         			#
#   on Tuesday at 12-0 run /bin/date                                                    #
#   on Monday at 1208,1209,1208 run /bin/echo Hello										#
#   every 1210 run /bin/date                     										#
#	on Monday at 1215 run /not/found                                                    #
#																						#
#	>>> OUTPUT                                                              			#
#	error in configuration: every Tuesday,Wednesday,Tuesday at 1200,1201 run /bin/date	#	
#	error in configuration:	every Tues at 1202 run /bin/date							#
#	error in configuration:	every Tues at 1202 run /bin/date							#
#	error in configuration:	every tuesday at 1203 run /bin/date							#
#	error in configuration:	on Tuesday at 1204 /bin/date								#
#	error in configuration:	on every Tuesday at 1205 run /bin/date						#
#	error in configuration:	on Tuesday at 2400 run /bin/date							#
#	error in configuration:	on Tuesday at 1206 run /bin/date							#
#	error in configuration:	on Tuesday at 1207 run										#
#	error in configuration:	on Tuesday at 1260 run /bin/date							#
#	error in configuration:	on Tuesday at 123 run /bin/date	 							#
#   error in configuration: on Tuesday at 12-0 run /bin/date                            #
#	error in configuration:	on Monday at 1208,1209,1210 run /bin/echo Hello	            #
#   error in configuration:	every 1210 run /bin/date                                    #
#   error in configuration: on Monday at 1215 run /not/found                            #
#										      				 							#
#########################################################################################
def create_test1():

	f = open("test1.in", "w+")
	f.write("every Friday at 0230 run /bin/echo THIS IS WORK\n") # correct - simple case
	f.write("every Monday,Tuesday at 1300,1301 run /bin/date\n") # correct -more complex program arguments
	f.write("on Tuesday at 0000 run /bin/date\n") # correct - time 0000
	f.write("every Tuesday,Wednesday,Tuesday at 1200,1201 run /bin/date\n")  #incorrect - repeated day
	f.write("every Tues at 1202 run /bin/date\n") #  incorrect dayname
	f.write("every Tuesday at 11000 run /bin/date\n") # incorrect time
	f.write("every tuesday at 1203 run /bin/date\n") # incorrect dayname (case is wrong)
	f.write("on Tuesday at 1204 /bin/date\n") # incorrect  no run keyword
	f.write("on every Tuesday at 1205 run /bin/date\n") # bad syntax
	f.write("on Tuesday at 2400 run /bin/date\n") # times range from 0000 to 2359
	f.write("on Tuesday at 1206 run /bin/date\n") # correct simple
	f.write("on Tuesday at 1206 run /bin/date\n") # duplicate run time
	f.write("on Tuesday at 1207 run\n") # program path missing
	f.write("on Tuesday at 1260 run /bin/date\n") # incorrect time
	f.write("on Tuesday at 123 run /bin/date\n") # incorrect time
	f.write("on Tuesday at 12-0 run /bin/date\n") # incorrect time
	f.write("on Monday at 1208,1209,1208 run /bin/echo Hello\n") # duplicate time in a line
	f.write("every 1210 run /bin/date\n")
	f.write("on Monday at 1215 run /wrong/path\n") # program not found
	f.close()
	f = open("test1.out", "w+")
	f.write("error in configuration: every Tuesday,Wednesday,Tuesday at 1200,1201 run /bin/date\n")
	f.write("error in configuration: every Tues at 1202 run /bin/date\n")
	f.write("error in configuration: every Tuesday at 11000 run /bin/date\n")
	f.write("error in configuration: every tuesday at 1203 run /bin/date\n")
	f.write("error in configuration: on Tuesday at 1204 /bin/date\n")
	f.write("error in configuration: on every Tuesday at 1205 run /bin/date\n")
	f.write("error in configuration: on Tuesday at 2400 run /bin/date\n")
	f.write("error in configuration: on Tuesday at 1206 run /bin/date\n")
	f.write("error in configuration: on Tuesday at 1207 run\n")
	f.write("error in configuration: on Tuesday at 1260 run /bin/date\n")
	f.write("error in configuration: on Tuesday at 123 run /bin/date\n")
	f.write("error in configuration: on Tuesday at 12-0 run /bin/date\n")
	f.write("error in configuration: on Monday at 1208,1209,1208 run /bin/echo Hello\n")
	f.write("error in configuration: every 1210 run /bin/date\n")
	f.write("error in configuration: on Monday at 1215 run /wrong/path\n")
	f.close()


###########################################################
#											              #
#	>>> TEST 2 - ON/EVERY  								  #	  
#	- test success "on" program							  #
#	- test success "every" program        				  #
#														  #
# 	>>> .runner.conf		                  			  #
#	on [day] at [time+120] run /bin/echo THIS IS ON       #
#	every [day] at [time+180] run /bin/echo THIS IS EVERY #
#	                                                      #
#   >>> Output 1 at timestamp + 10          		      #
#	will run at [time+120] /bin/echo THIS IS ON           #
#	will run at [time+180] /bin/echo THIS IS EVERY        #
#                                                         #
#	>>> Output 2 at timestamp + 190                 	  #
#	ran [time+120] /bin/echo THIS IS ON                   #
#   ran [time+180] /bin/echo THIS IS EVERY 				  #
#	will run at [time+180+week] bin/echo THIS IS EVERY    #
#														  #
###########################################################
def create_test2(times):

	f = open("test1.in", "w+")
	f.write("on "+ convertTime(times,2)[0]+" at "+ convertTime(times,2)[1] + " run /bin/echo THIS IS ON\n" )
	f.write("every "+ convertTime(times,3)[0]+" at "+ convertTime(times,3)[1] + " run /bin/echo THIS IS EVERY\n" )
	f.close()
	f = open("test1.out", "w+")
	time1 = time.ctime(time.time()-time.time()%60 +130).split()
	time2 = time.ctime(time.time()-time.time()%60 +190).split()
	f.write("will run at " + time1[0]+ " " + time1[1] + " " + time1[2] +" "+time1[3][0:6]+ "00 " + time1[4] + " /bin/echo THIS IS ON\n")
	f.write("will run at " + time2[0]+ " " + time2[1] + " " + time2[2] +" "+time2[3][0:6]+ "00 " + time2[4] + " /bin/echo THIS IS EVERY" +"\n")
	f.close()
	f = open("test2.out", "w+")
	time3 = time.ctime(time.time()-time.time()%60 +190+604800).split()
	f.write("ran " + time1[0]+ " " + time1[1] + " " + time1[2] +" "+time1[3][0:6]+ "00 " + time1[4] + " /bin/echo THIS IS ON\n")
	f.write("ran " + time2[0]+ " " + time2[1] + " " + time2[2] +" "+time2[3][0:6]+ "00 " + time2[4] + " /bin/echo THIS IS EVERY\n")
	f.write("will run at " + time3[0]+ " " + time3	[1] + " " + time3[2] +" "+time3[3][0:6]+ "00 " + time3[4] +  " /bin/echo THIS IS EVERY" +"\n")
	f.close()

###############################################################
#											                  #
#	>>> TEST 3 - AT  										  #	   
#	- test  "at" program "today"				              #
#	- test  "at" program "tommorow"                           #
#    			  										      #
# 	>>> .runner.conf		                  			      #
#	at [time+120] run /bin/echo THIS IS AT TODAY              #
#	at [time+day+-120] run /bin/echo THIS IS AT TOMORROW      #
#	                                                          #
#   >>> Output 1 at timestamp + 10          		          #
#	will run at [time+120] /bin/echo THIS IS AT TODAY         #
#	will run at [time+day-120] /bin/echo THIS IS AT TOMORROW  #
#                                                             #
#	>>> Output 2 at timestamp + 190                 	      #
#	ran [time+120] /bin/echo THIS IS ON                       #
#   will run at [time+day-120] /bin/echo THIS IS EVERY 	      #
#														      #
###############################################################

def create_test3(times):

	f = open("test1.in", "w+")
	f.write("at "+ convertTime(times,2)[1] + " run /bin/echo THIS IS AT TODAY\n" )
	f.write("at "+ convertTime(times,-2)[1] + " run /bin/echo THIS IS AT TOMORROW\n" )
	f.close()
	f = open("test1.out", "w+")
	time1 = time.ctime(time.time()-time.time()%60 +130).split()
	time2 = time.ctime(time.time()-time.time()%60 +60*60*24 - 100).split()
	f.write("will run at " + time1[0]+ " " + time1[1] + " " + time1[2] +" "+time1[3][0:6]+ "00 " + time1[4] + " /bin/echo THIS IS AT TODAY\n")
	f.write("will run at " + time2[0]+ " " + time2[1] + " " + time2[2] +" "+time2[3][0:6]+ "00 " + time2[4] + " /bin/echo THIS IS AT TOMORROW" +"\n")
	f.close()
	f = open("test2.out", "w+")
	f.write("ran " + time1[0]+ " " + time1[1] + " " + time1[2] +" "+time1[3][0:6]+ "00 " + time1[4] + " /bin/echo THIS IS AT TODAY\n")
	f.write("will run at " + time2[0]+ " " + time2[1] + " " + time2[2] +" "+time2[3][0:6]+ "00 " + time2[4] +  " /bin/echo THIS IS AT TOMORROW" +"\n")
	f.close()

#############################################################################
#											                  				#
#	>>> TEST 4 - MULTIPLE EVERY  								     		#	   
#	- test multiple day/time "every" program  				 				#
#											                  				#
# 	>>> .runner.conf		                  			      				#
#	every [day1,day2] at [time+120,time+600] run /bin/echo THIS IS EVERY    #
#	                                                          				#
#   >>> Output 1 at timestamp + 10          		          				#
#	will run at [time + 120] /bin/echo THIS IS EVERY          				#
#	will run at [time + 600] /bin/echo THIS IS EVERY          				#
#	will run at [time + day +120] /bin/echo THIS IS EVERY     				#
#	will run at [time + day + 600] /bin/echo THIS IS EVERY    				#
#                                                             				#
#	>>> Output 2 at timestamp + 190                 	      				#
#	ran [time+120] /bin/echo THIS IS EVERY         				            #
#	will run at [time + 600] /bin/echo THIS IS EVERY          				#
#	will run at [time + day +120] /bin/echo THIS IS EVERY     				#
#	will run at [time + day + 600] /bin/echo THIS IS EVERY                  #
#   will run at [time+7day+120] /bin/echo THIS IS EVERY 	      		    #
#														      				#
#############################################################################
def create_test4(times):

	f = open("test1.in", "w+")
	f.write("every "+ convertTime(times,2)[0]+","+getNextDay(convertTime(times,10)[0])+" at "+ convertTime(times,2)[1] +","+convertTime(times,10)[1] + " run /bin/echo THIS IS EVERY\n" )
	f.close()
	f = open("test1.out", "w+")
	time1 = time.ctime(time.time()-time.time()%60 +130).split()
	time2 = time.ctime(time.time()-time.time()%60 +610).split()
	time3 = time.ctime(time.time()-time.time()%60 +60*60*24 +130).split()
	time4 = time.ctime(time.time()-time.time()%60 +60*60*24 +610).split()
	time5 = time.ctime(time.time()-time.time()%60 +130 +60*60*24*7).split()
	f.write("will run at " + time1[0]+ " " + time1[1] + " " + time1[2] +" "+time1[3][0:6]+ "00 " + time1[4] + " /bin/echo THIS IS EVERY" + "\n")
	f.write("will run at " + time2[0]+ " " + time2[1] + " " + time2[2] +" "+time2[3][0:6]+ "00 " + time2[4] + " /bin/echo THIS IS EVERY" +"\n")
	f.write("will run at " + time3[0]+ " " + time3[1] + " " + time3[2] +" "+time3[3][0:6]+ "00 " + time3[4] + " /bin/echo THIS IS EVERY" + "\n")
	f.write("will run at " + time4[0]+ " " + time4[1] + " " + time4[2] +" "+time4[3][0:6]+ "00 " + time4[4] + " /bin/echo THIS IS EVERY" +"\n")
	f.close()
	f = open("test2.out", "w+")
	f.write("ran " + time1[0]+ " " + time1[1] + " " + time1[2] +" "+time1[3][0:6]+ "00 " + time1[4] + " /bin/echo THIS IS EVERY\n")
	f.write("will run at " + time2[0]+ " " + time2[1] + " " + time2[2] +" "+time2[3][0:6]+ "00 " + time2[4] + " /bin/echo THIS IS EVERY" +"\n")
	f.write("will run at " + time3[0]+ " " + time3[1] + " " + time3[2] +" "+time3[3][0:6]+ "00 " + time3[4] + " /bin/echo THIS IS EVERY" + "\n")
	f.write("will run at " + time4[0]+ " " + time4[1] + " " + time4[2] +" "+time4[3][0:6]+ "00 " + time4[4] + " /bin/echo THIS IS EVERY" +"\n")
	f.write("will run at " + time5[0]+ " " + time5[1] + " " + time5[2] +" "+time5[3][0:6]+ "00 " + time5[4] + " /bin/echo THIS IS EVERY" +"\n")
	f.close()

#############################################################################
#											                  				#
#	>>> TEST 5 - MULTIPLE ON				 								#	   
#	- test multiple day/time "on" program  									#
#   - test "on" program before current time    				 				#
#											                  				#
# 	>>> .runner.conf		                  			      				#
#	on [day1,day2] at [time+120,time-120] run /bin/echo THIS IS ON          #
#	                                                          				#
#   >>> Output 1 at timestamp + 10          		          				#
#	will run at [time + 120] /bin/echo THIS IS ON          				    #
#	will run at [time + day - 120] /bin/echo THIS IS ON     				#
#	will run at [time + 7day - 120] /bin/echo THIS IS ON    				#
#                                                             				#
#	>>> Output 2 at timestamp + 190                 	      				#
#	ran [time+120] /bin/echo THIS IS ON         				            #
#	will run at [time + day - 120] /bin/echo THIS IS ON     				#
#	will run at [time + day + 120] /bin/echo THIS IS ON          	        #
#   will run at [time+7day-120] /bin/echo THIS IS ON 	      		        #
#														      				#
#############################################################################
def create_test5(times):

	f = open("test1.in", "w+")
	f.write("on "+ convertTime(times,2)[0]+","+getNextDay(convertTime(times,2)[0])+" at "+ convertTime(times,2)[1] +","+convertTime(times,-2)[1] + " run /bin/echo THIS IS ON\n" )
	f.close()
	f = open("test1.out", "w+")
	time1 = time.ctime(time.time()-time.time()%60 +130).split()
	time2 = time.ctime(time.time()-time.time()%60 + 60*60*24 - 70).split()
	time3 = time.ctime(time.time()-time.time()%60 +60*60*24 + 130).split()
	time4 = time.ctime(time.time()-time.time()%60 +60*60*24*7 - 70).split()
	f.write("will run at " + time1[0]+ " " + time1[1] + " " + time1[2] +" "+time1[3][0:6]+ "00 " + time1[4] + " /bin/echo THIS IS ON" + "\n")
	f.write("will run at " + time2[0]+ " " + time2[1] + " " + time2[2] +" "+time2[3][0:6]+ "00 " + time2[4] + " /bin/echo THIS IS ON" +"\n")
	f.write("will run at " + time3[0]+ " " + time3[1] + " " + time3[2] +" "+time3[3][0:6]+ "00 " + time3[4] + " /bin/echo THIS IS ON" + "\n")
	f.write("will run at " + time4[0]+ " " + time4[1] + " " + time4[2] +" "+time4[3][0:6]+ "00 " + time4[4] + " /bin/echo THIS IS ON" +"\n")
	f.close()
	f = open("test2.out", "w+")
	f.write("ran " + time1[0]+ " " + time1[1] + " " + time1[2] +" "+time1[3][0:6]+ "00 " + time1[4] + " /bin/echo THIS IS ON\n")
	f.write("will run at " + time2[0]+ " " + time2[1] + " " + time2[2] +" "+time2[3][0:6]+ "00 " + time2[4] + " /bin/echo THIS IS ON" +"\n")
	f.write("will run at " + time3[0]+ " " + time3[1] + " " + time3[2] +" "+time3[3][0:6]+ "00 " + time3[4] + " /bin/echo THIS IS ON" + "\n")
	f.write("will run at " + time4[0]+ " " + time4[1] + " " + time4[2] +" "+time4[3][0:6]+ "00 " + time4[4] + " /bin/echo THIS IS ON" +"\n")
	f.close()

#############################################################################
#											                  				#
#	>>> TEST 6 - ERROR STATUS			 									#	   
#	- test for error status messge 			   				 				#
#											                  				#
# 	>>> .runner.conf		                  			      				#
#	every [day] at [time+120] run /bin/date THIS IS EVERY                   #
#	                                                          				#
#   >>> Output 1 at timestamp + 10          		          				#
#	will run at [time + 120] /bin/date THIS IS EVERY          				#
#                                                             				#
#	>>> Output 2 at timestamp + 190                 	      				#
#	error [time+120] /bin/date THIS IS ON         				            #
#	will run at [time + 120 +7day] /bin/echo THIS IS ON     				#
#														      				#
#############################################################################
def create_test6(times):

	f = open("test1.in", "w+")
	f.write("every "+ convertTime(times,2)[0]+" at "+ convertTime(times,2)[1] + " run /bin/date THIS IS EVERY\n" )
	f.close()
	f = open("test1.out", "w+")
	time1 = time.ctime(time.time()-time.time()%60 +130).split()
	time2 = time.ctime(time.time()-time.time()%60 +130 +24*7*60*60).split()
	f.write("will run at " + time1[0]+ " " + time1[1] + " " + time1[2] +" "+time1[3][0:6]+ "00 " + time1[4] + " /bin/date THIS IS EVERY\n")
	f.close()

	f = open("test2.out", "w+")
	f.write("error " + time1[0]+ " " + time1[1] + " " + time1[2] +" "+time1[3][0:6]+ "00 " + time1[4] + " /bin/date THIS IS EVERY\n")
	f.write("will run at " + time2[0]+ " " + time2[1] + " " + time2[2] +" "+time2[3][0:6]+ "00 " + time2[4] + " /bin/date THIS IS EVERY\n")
	f.close()

#############################################################################
#											                  				#
#	>>> TEST 7 - OUTPUT/EXIT  								     			#	   
#	- test whether program is actually execute 								#
#   - test whether program is exit after nothing left to run  				#
#											                  				#
# 	>>> .runner.conf		                  			      				#
#	on [day] at [time+120] run /bin/echo THIS IS ON       					#
#	                                                          				#
#   >>> Output 1 at timestamp + 10          		          				#
#	Hello World									          				    #
#	Nothing left to run                                                     #
#														      				#
#############################################################################		
def create_test7(times):

	f = open("test1.in", "w+")
	f.write("on "+ convertTime(times,2)[0]+" at "+ convertTime(times,2)[1] + " run /bin/echo Hello World\n" )
	f.close()
	f = open("test1.out", "w+")
	f.write("Hello World\n")
	f.write("nothing left to run\n")
	f.close()

#############################################################################
#											                  				#
#	>>> TEST 8 EMPTY CONFIGURATION FILE 	 								#	   
#	- test empty configuration file											#
#											                  				#
# 	>>> .runner.conf		                  			      				#
#	                                                          				#
#   >>> Output 1 at timestamp + 10          		          				#
#	configuration file Empty 												#
#														      				#
#############################################################################
def create_test8():

	f = open("test1.in", "w+")
	f.write("")
	f.close()
	f = open("test1.out", "w+")
	f.write("configuration file empty\n")
	f.close()

#############################################################################
#											                  				#
#	>>> TEST 9 TRUNCATE .RUN.STATUS	 	 								#	   
#	- test wheter runstatus.py truncate .run.status after print to stdout   #
#											                  				#
# 	>>> .runner.conf		                  			      				#
##	on [day] at [time+120] run /bin/echo THIS IS ON       					#
#	every [day] at [time+180] run /bin/echo THIS IS EVERY 					#
#																			#
#														      				#
#############################################################################
def create_test9(times):

	f = open("test1.in", "w+")
	f.write("on "+ convertTime(times,2)[0]+" at "+ convertTime(times,2)[1] + " run /bin/echo THIS IS ON\n" )
	f.write("every "+ convertTime(times,3)[0]+" at "+ convertTime(times,3)[1] + " run /bin/echo THIS IS EVERY\n" )
	f.close()

	f = open("test1.out", "w+")
	f.write("0\n")
	f.close()


#########################################################################################
# 																						#
# 	>>> TEST 10 - TEST CONFIGURATION FILE NOT EXIST 									#
#	- configuration file size = 0 														#
#																						#
#   >>> .runner.configuration 															#
#																						#
#	>>> Output 																			#
#	configuration file not found 														#
#                   																	#
#########################################################################################
def create_test10():

	f = open("test1.out", "w+")
	f.write("configuration file not found\n")
	f.close()


def main():

	test = sys.argv[1]
	if test == "1": 
		create_test1()
	elif test == "2":
		create_test2(getTime())
	elif test == "3":
		create_test3(getTime())
	elif test == "4":
		create_test4(getTime())
	elif test == "5":
		create_test5(getTime())
	elif test == "6":
		create_test6(getTime())
	elif test == "7":
		create_test7(getTime())
	elif test == "8":
		create_test8()
	elif test == "9":
		create_test9(getTime())
	elif test == "10":
		create_test10()


if __name__ == "__main__":
	main()

