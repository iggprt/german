import ctypes, time, threading
import msvcrt
import sys
import os
from datetime import date
import datetime
import Save
import time

prev_state = -1
flg_ex = 0
flg_id = 1
state = 1

due = date(2019, 1, 31)
d = (due - date.fromtimestamp(time.time())).days


os.system('cls')


# its a flag to exit all threads
def exit_flag():
	if flg_ex: 
		return 1
	return 0

def idle_flag():
	if flg_id: 
		return 1
	return 0

def looking_for_key():

	os.system('cls')
	data = Save.get_data()
	words_to_ask = Save.get_words_to_ask()
	print 'due days: ' + str(d) + '\nwords to: '+ str(len(words_to_ask)) +'\naverage : ' + str((len(data)- len(words_to_ask) )/d) + '\n'
	
	while True:
		
		if msvcrt.kbhit():
			key = msvcrt.getch()
			if key == 'q':
				print "nuuuuu.."
				flg_ex = 1
				flg_id = 0
				sys.exit()
			if key == 'a':
				print "add a word"
			
			if key == 'p':
				analize()
			
			if key == 'w':
				print "start the quiz"
				time.sleep(1)
				quiz()
			if key == 's':
				print "search a word"
				search_word_ger()
			if key == 'l':
				print "L pressed"
				#s = Save.get_words_to_ask(2)
				quiz()
				

	if exit_flag():
		threading.Timer(1, looking_for_key).start()
	
	
def search_word_ger():
	os.system('cls')
	data = Save.get_data()

	search = raw_input("Serch the word in german: ")
	for line in data:
		if search in line[7].lower():
			print line
	print "\npress any key..."
	#msvcrt.getch()
	
def analize():
	d = Save.get_data()
	words_to_ask = Save.get_words_to_ask()
	words_done = Save.get_words_done()
	sum_to_go = 0
	sum_so_far = 0
	for line in d:
		if line[4] < len(line[5]):
			sum_to_go += len(line[5]) - line[4]
			sum_so_far += line[4]
	
	print "words_to_go: "+ str(len(words_to_ask))
	print "words_done: "+ str(len(words_done))
	print "correct guesses: " + str(sum_so_far)
	print "total guesses: " + str(sum_to_go) + "\n"
	
def quiz():
	
	words_to_ask = Save.get_words_to_ask()
	print 'answer q to quit'
	d = Save.get_data()
	words_done = Save.get_words_done()
	sum_to_go = 0
	sum_so_far = 0
	for line in d:
		if line[4] < len(line[5]):
			sum_to_go += len(line[5]) - line[4]
			sum_so_far += line[4]
	
	if len(words_to_ask) == 0:
		Save.get_words_to_ask(1)
	
	questions = 5
	

	print "words_to_go: "+ str(len(words_to_ask))
	
	print "correct guesses: " + str(sum_so_far)
	print "total guesses: " + str(sum_to_go) + "\n"
	
	for _ in range(questions):
		rand = int(time.time()*100 % len(words_to_ask))
		answer = raw_input("%s = " % words_to_ask[rand][2])
		if answer == words_to_ask[rand][5].lower():
			Save.add_combos(words_to_ask[rand][0])
			print "CORECT - %s\n" % words_to_ask[rand][1]
		else:
			print "WRONG... %s - " % words_to_ask[rand][5] + " %s\n" % words_to_ask[rand][1]
			Save.add_wrongs(words_to_ask[rand][0])
	
	print 'gata'
	time.sleep(1)
	
def Main():
	
	if idle_flag():
		looking_for_key()
	
if __name__ == "__main__":
	Main()
	