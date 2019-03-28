import sys
import psycopg2
import csv
import requests
import json
import re


db = psycopg2.connect("dbname=safesport_test")
c = db.cursor()

def fetch_name(name=""):
	if (name == ""):
		try:
			c.execute("SELECT * FROM common_name where checked=false limit 1;")
			name = c.fetchone()[0]
			return name
		except:
			c.execute("UPDATE common_name set checked=false;")
			print("AUTOCOMPLETE::RestartingCycle")
			db.commit()
			sys.exit(1)
	else:
		try:
			c.execute("SELECT * FROM common_name where checked=false and name like \'"+name+"\' limit 1;")
			name = c.fetchone()[0]	
			return name
		except:
			print("AUTOCOMPLETE::CheckedOrNotCommon")
			sys.exit(1)
		
def search_autocomplete(name):
	response = requests.get('https://safesport.org/api/userviolations/names?q='+name)
	response = json.loads(response.text)
	for n in response["items"]:		
		na = {"fullName":n["title"]}
		insert(na)
		print("AUTOCOMPLETE::Name: " + n['title'])

	mark_checked(name)

def insert(n):
	cq = """INSERT INTO coach (fullName) VALUES (%(fullName)s) ON CONFLICT (fullName) DO NOTHING"""
	c.execute(cq,n)


def mark_checked(name):
	c.execute("update common_name set checked=true where name like \'"+name+"\'")
	db.commit()
	print("AUTOCOMPLETE::UpdatedTables")


if (len(sys.argv)>1):
	name = fetch_name(sys.argv[1].upper())
	print("Searching: ", name)
	search_autocomplete(name)

else:
	name = fetch_name()
	if name:
		print("AUTOCOMPLETE::Searching: ", name)
		search_autocomplete(name)

