import sqlite3
import re
import random, time

# -*- coding: utf-8 -*-
# coding: utf-8

conn = sqlite3.connect('Voc4.db')
conn.text_factory = str
c = conn.cursor()

file = open('words.txt','r').read()	

def create_tables():
	c.execute("CREATE TABLE IF NOT EXISTS Voc (Voc_id integer primary key autoincrement, ger, eng, freq, rights, wrongs, total)")
	c.execute("CREATE TABLE IF NOT EXISTS Unsorted (Unsorted_id integer primary key autoincrement, ger, eng)")
	conn.commit()
	
def reset_tables():
	create_tables()
	c.execute("drop table Voc")
	c.execute("drop table Unsorted")
	create_tables()
	conn.commit()


def increment_rights(word_id):
	c.execute("select frequency from Voc where Voc_id = :id",{'id':word_id})
	freq = int(c.fetchall()[0][0])
	
	c.execute("""update word_tab 
					set frequency = :f
					where word_id = :id""",{
					'f':freq+1,
					'id':word_id})
	conn.commit()
	
def insert_word(ger, eng):
	c.execute("insert into Voc (ger, eng, freq, rights, wrongs, total) values(:g, :e, 0,0,0,0)",{'g':ger, 'e':eng})
	
def is_ascii(s):
    return all(ord(c) < 128 for c in s)



def create_db():
	i = 0;
	pat = re.compile('<td>(.+)<\/td>')
	matches = pat.findall(file)
	
	ger = ''
	eng = '' 
	
	for e in matches:
		if i == 0:
			pass 
		elif i == 1:
			ger = e
		else:
			eng = e
			i = -1
			insert_word(ger, eng)
		i += 1
	
	
#reset_tables()
#create_tables()		
#create_db()
#conn.commit()

def ascify(word):
	retVal = word
	for letter in word:
		if is_ascii(letter) is False:
			if ord(letter) == 252:
				retVal = retVal.replace(letter,'u')
			elif ord(letter) == 223:
				retVal = retVal.replace(letter,'ss')
			elif ord(letter) == 246:
				retVal = retVal.replace(letter,'o')
			elif ord(letter) == 228:
				retVal = retVal.replace(letter,'a')	
			elif ord(letter) == 220:
				retVal = retVal.replace(letter,'U')	
			elif ord(letter) == 196:
				retVal = retVal.replace(letter,'A')
			elif ord(letter) == 214:
				retVal = retVal.replace(letter,'O')
			elif ord(letter) == 239:
				retVal = retVal.replace(letter,'I')
			else:
				print 'error:' +  word + ' ' + str(ord(letter))
				
	return retVal
"""
c.execute("select * from Voc")
data = c.fetchall()

for line in data:
	if is_ascii(line[1]) is False:
		print line[1]
		print ascify(line[1])
		
	c.execute("update Voc set ger_ascii = :g where Voc_id = :id",
				{'id': int(line[0]), 'g':ascify(line[1])})
		
conn.commit()
"""

def get_data():
	c.execute("select * from WORDS")
	data = c.fetchall()
	return data
	
def add_wrongs(word_id):
	c.execute("select * from WORDS where WORDS_ID = :id",{'id':word_id})
	line = c.fetchall()[0]
	c.execute("update WORDS set wrong= :w where WORDS_ID = :id",{'w':line[3]+1,'id':word_id})
	c.execute("update WORDS set combo= :w where WORDS_ID = :id",{'w':0,'id':word_id})
	conn.commit()

def add_combos(word_id):
	c.execute("select * from WORDS where WORDS_ID = :id",{'id':word_id})
	line = c.fetchall()[0]
	c.execute("update WORDS set combo = :w where WORDS_ID = :id",{'w':line[4]+1,'id':word_id})
	conn.commit()	

def get_words_to_go():
	words_to_go = []
	data = get_data()
	for line in data:
		if line[3] == 0:
			words_to_go.append(line)
	
	return words_to_go
	
def get_words_done():
	data = get_data()
	words_done = []
	for line in data:
		if line[4] >= len(line[5]*2):
			words_done.append(line)
	
	return words_done
	
def get_words_to_ask( plus = 0):
	
	data = get_data()

	if plus > len(get_words_to_go()):
		plus = len(get_words_to_go())	
	
	while plus > 0:	
		i = 0
		words_to_go = get_words_to_go()
		rand = int(time.time()*100)%len(words_to_go)		
		add_wrongs(words_to_go[rand][0])
		plus = plus - 1
	
	words_to_ask = []
	for line in data:
		if line[3] > 0 and line[4] < len(line[5]*2):
			words_to_ask.append(line)
	
	return words_to_ask
	
	
"""
c.execute("select * from Voc")
data = c.fetchall()
for line in data:
	c.execute("insert into WORDS (ger, eng, wrong, combo, ascii_ger) values(:g, :e,0,0, :asc)",{'g':line[1], 'e':line[2], 'asc':line[7]})
	print line
	
conn.commit()
"""


