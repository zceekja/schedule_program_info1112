#!/bin/bash

##############################################################
#                                                            #
# Function to test runstatus.py output                       #
#                                                            #
##############################################################
test_runner_status( ) {
	test=$1
	python3 testGenerator.py ${test}
	sleep 1
	echo ">>>>>>>>> Generating test $test: $2"
	echo ""
	sleep 1
	cat test1.in
	echo ""
	cat test1.in > ~/.runner.conf
	now=$(date +"%T")
	printf "************ Starting runner.py at $now *************\n\n"
	python3 runner.py > /dev/null & # run in background, redirect stdout to null 
	PID=$!
	sleep 1
	printf '>>>>>>>>> Expected output \n\n'
	cat test1.out
	echo ""
	sleep 1
	python3 runstatus.py > output.txt # redirect stdout to output.txt
	now=$(date +"%T")
	sleep 1
	printf ">>>>>>>>> Status output at $now\n\n"
	cat output.txt
	echo ""
	
	printf '>>>>>>>>> Comparing status output and expected output\n\n'
	
	sleep 1
	a=$(diff <(cat -A output.txt) <(cat -A test1.out))
	
	if [[ $a == "" ]]
	then
		echo "Passed!, result matched!"
	else
		echo "Output not matched!. Please manually check expected and status output, maybe there is a second delay"
	fi
	echo ""
	sleep 1
	
	printf '>>>>>>>>> Wait a moment (180 seconds left)\n'
	sleep 60
	printf '>>>>>>>>> Wait a moment (120 seconds left)\n'
	sleep 60
	printf '>>>>>>>>> Wait a moment (60 seconds left)\n\n'
	sleep 60

	printf '>>>>>>>>> Expected output \n\n'
	cat test2.out
	echo ""
	sleep 1
	python3 runstatus.py > output.txt # redirect stdout to output.txt
	now=$(date +"%T")
	
	sleep 1
	printf ">>>>>>>>> Status output at $now\n\n"
	cat output.txt
	echo ""
	
	sleep 1
	
	printf '>>>>>>>>> Comparing status output and expected output\n\n'
	
	sleep 1
	
	a=$(diff <(cat -A output.txt) <(cat -A test2.out))
	
	if [[ $a == "" ]]
	then
		echo "Passed!, result matched!"
	else
		echo "Output not matched!. Please manually check expected and status output, maybe there is a second delay"
	fi
	
	kill $PID
	echo ""
	echo "-----------------------------------------------------------------"
	echo "			Test $test Done"
	echo "-----------------------------------------------------------------"
	echo ""	
}

##############################################################
#                                                            #
# Function to test .runner.py output                         #
#                                                            #
##############################################################
test_runner_stdout(){
	test=$1
	echo ">>>>>>>>> Generating test $test: $2"

	python3 testGenerator.py $test
	sleep 1

	cat test1.in
	echo ""
	cat test1.in > ~/.runner.conf 
	now=$(date +"%T")
	printf "************ Starting runner.py at $now *************\n\n"
	python3 runner.py > output.txt & 

	printf '>>>>>>>>> Wait a moment (120 seconds left)\n'
	sleep 60
	printf '>>>>>>>>> Wait a moment (60 seconds left)\n\n'
	sleep 60

	echo ">>>>>>>>> Test $test expected stdout"
	echo

	cat test1.out
	sleep 1	
	echo ""
	printf '>>>>>>>>> Stdout Result \n\n'
	cat output.txt
	echo ""
	
	sleep 1
	printf '>>>>>>>>> Comparing stdout and expected output\n\n'
	
	sleep 1
	diff output.txt test1.out
	a=$(diff <(cat -A output.txt) <(cat -A test1.out))
	
	if [[ $a == "" ]]
	then
		echo "Passed!, result matched!"
	else
		echo "Output not matched!."
	fi
	echo "-----------------------------------------------------------------"
	echo "			Test $test Done"
	echo "-----------------------------------------------------------------"
	echo ""	
}
##############################################################
#                                                            #
# Function to test .runner.py stderr                         #
#                                                            #
##############################################################
test_runner_stderr(){
	
	test=$1
	echo ">>>>>>>>> Generating test $test: $2"
	echo ""
	sleep 1
	now=$(date +"%T")
	printf "************ Starting runner.py at $now *************\n\n"
	python3 testGenerator.py $test
	sleep 1
	if (( $test == 1 )) || (( $test == 8 ))
	then
		cat test1.in > ~/.runner.conf
	elif (( $test == 10 ))
	then
		FILE=~/.runner.conf
		if [ -f $FILE ]
		then
    		rm ~/.runner.conf
		fi
	fi
	python3 -u runner.py 2> output.txt & 
	sleep 1
	printf '>>>>>>>>> Expected output \n\n'

	cat test1.out
	sleep 1 
	printf '\n>>>>>>>>> Stderr output \n\n'

	cat output.txt 
	sleep 1
	echo ""
	printf '>>>>>>>>> Comparing stderr and expected output\n\n'

	a=$(diff <(cat -A output.txt) <(cat -A test1.out))

	if [[ $a == "" ]]
	then
		echo "Passed!, result matched!"
	else
		echo "Failed!, Output not matched"
	fi	
	echo "-----------------------------------------------------------------"
	echo "			Test $test Done"
	echo "-----------------------------------------------------------------"
	if (( $test == 10 ))
	then 
		touch test1.in
	fi	
}
##############################################################
#                                                            #
# Function to test file size of status file                  #
#                                                            #
##############################################################
test_status_truncate(){
	test=$1
	echo ">>>>>>>>> Generating test $test: $2"
	echo ""
	python3 testGenerator.py $test
	sleep 1
	cat test1.in > ~/.runner.conf
	now=$(date +"%T")
	printf "************ Starting runner.py at $now *************\n\n"
	python3 runner.py &
	sleep 1
	echo ">>>>>>>>> Test $test expected output"
	echo ""
	cat test1.out
	echo ""
	sleep 1
	python3 runstatus.py > output.txt
	sleep 1
	ls -al ~/ | grep [.]runner[.]status | awk {'print $5'} > output.txt

	echo ">>>>>>>>> Test $test output"
	echo ""
	cat output.txt
	echo ""
	sleep 1	
	printf '>>>>>>>>> Comparing output\n\n'

	a=$(diff <(cat -A output.txt) <(cat -A test1.out))
	
	if [[ $a == "" ]]
	then
		echo "Passed!, result matched!"
	else
		echo "Failed!, Output not matched"
	fi	

	echo "-----------------------------------------------------------------"
	echo "			Test $test Done"
	echo "-----------------------------------------------------------------"
}

#################################################
#                                               #
# clean() Remove test file                       #
#                                               #
#################################################

clean(){
	sleep 0.5
	rm output.txt
	sleep 0.5
	rm test*.in
	sleep 0.5
	rm test*.out
}

arg=$1 # store argument1 in arg

test1="INCORRECT-CONFIGURATION"
test2="ON/EVERY"
test3="AT"
test4="MULTIPLE-EVERY"
test5="MULTIPLE-ON"
test6="ERROR-STATUS"
test7="OUTPUT/EXIT"
test8="EMPTY-CONFIGURATION-FILE"
test9="TRUNCATE-.RUN.STATUS"
test10="CONF-FILE-NOT-EXIST"

if [ "$#" -ne 1 ]; then  # if argument is not given
	printf 'FOLLOW THIS FORMAT: ./test.sh [number]\n'
	printf " 0 - RUN ALL TESTS\n"
	printf " 1 - RUN INCORRECT CONFIGURATION TEST\n"
	printf " 2 - RUN 'ON' AND 'EVERY' TEST\n"
	printf " 3 - RUN 'AT' TEST\n"
	printf " 4 - RUN MULTIPLE 'EVERY' TEST\n"
	printf " 5 - RUN MULTIPLE ON TEST\n"
	printf " 6 - RUN ERROR STATUS TEST\n"
	printf " 7 - RUN OUTPUT/EXIT TEST\n"
	printf " 8 - RUN EMPTY CONFIGURATION-FILE-TEST\n"
	printf " 9 - RUN TRUNCATE TEST\n"
	printf " 10 - RUN CONFGURATION FILE NOT EXIST TEST\n"
	exit 1
fi

if (( $arg == 1 )) || (( $arg == 10 )) || (( $arg == 8 ))
then
	test_runner_stderr $arg 


elif (( $arg > 1 )) && (( $arg < 7 ))
then
	test_runner_status $arg 

elif (( $arg == 7 ))
then
	test_runner_stdout $arg 

elif (( $arg == 9 ))
then
	test_status_truncate $arg 

elif (( $arg == 0 ))
then
	test_runner_stderr 1 $test1
	test_runner_status 2 $test2
	test_runner_status 3 $test3
	test_runner_status 4 $test4
	test_runner_status 5 $test5
	test_runner_status 6 $test6
	test_runner_stdout 7 $test7
	test_runner_stderr 8 $test8
	test_status_truncate 9 $test9
	test_runner_stderr 10 $test10
else
	printf 'FOLLOW THIS FORMAT: ./test.sh [number]\n'
	printf " 0 - RUN ALL TESTS\n"
	printf " 1 - RUN INCORRECT CONFIGURATION TEST\n"
	printf " 2 - RUN 'ON' AND 'EVERY' TEST\n"
	printf " 3 - RUN 'AT' TEST\n"
	printf " 4 - RUN MULTIPLE 'EVERY' TEST\n"
	printf " 5 - RUN MULTIPLE ON TEST\n"
	printf " 6 - RUN ERROR STATUS TEST\n"
	printf " 7 - RUN OUTPUT/EXIT TEST\n"
	printf " 8 - RUN EMPTY CONFIGURATION-FILE-TEST\n"
	printf " 9 - RUN TRUNCATE TEST\n"
	printf " 10 - RUN CONFGURATION FILE NOT EXIST TEST\n"
	exit 1	
fi

clean # remove test file