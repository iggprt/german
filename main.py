import Save
from datetime import date
import datetime
import time
import os

due = date(2019, 1, 31)
d = (due - date.fromtimestamp(time.time())).days

os.system('cls')

data = Save.get_data()




while True:
	os.system('cls')
	print 'due days: ' + str(d) + '\naverage : ' + str(len(data)/d) + '\n'
	option = input("Option: ")
	
	
	Save.add_combos(option)
	