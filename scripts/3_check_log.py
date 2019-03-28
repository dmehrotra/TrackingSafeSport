import sys
import psycopg2
import csv
import requests
import json
import re


db = psycopg2.connect("dbname=safesport_test")
c = db.cursor()

def fetch_log():
	try:
		c.execute("SELECT * FROM logging.t_history where checked=false limit 1;")
		log = c.fetchone()
		print("LOGGING::FoundLogID: " + str(log[0]))
		return log
	except:
		print("LOGGING: No new logs")
		sys.exit(1)

def check_log(l):
	action = l[4]
	new_value = l[-3]
	old_value = l[-2]
	if action == "INSERT":
		print("LOGGING::Now Tracking: "+ new_value['fullname'])
		# TODO Handle this
		
def insert(n):
	cq = """INSERT INTO coach (fullName) VALUES (%(fullName)s) ON CONFLICT (fullName) DO NOTHING"""
	c.execute(cq,n)


def mark_checked(log):
	c.execute("update logging.t_history set checked=true where id ="+str(log))
	db.commit()
	print("updated tables")


log = fetch_log()
if log:
	check_log(log)
	mark_checked(log[0])




