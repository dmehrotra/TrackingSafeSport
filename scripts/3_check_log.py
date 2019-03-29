import sys
import psycopg2
import csv
import requests
import json
import re
from lxml import etree as ET
import datetime


db = psycopg2.connect("dbname=safesport_test")
c = db.cursor()

def write_rss(action,content):
	parser = ET.XMLParser(remove_blank_text=True)
	tree = ET.parse("rss.xml", parser)
	channel = tree.getroot()
	item = ET.SubElement(channel, "item")

	if (action == "INSERT"):
		title = ET.SubElement(item, "title")
		title.text = "Tracking a New Coach"
		description = ET.SubElement(item, "description")
		description.text = content["content"] + " is now being tracked"
		date = ET.SubElement(item, "date")
		now = datetime.datetime.now()
		date.text=now.isoformat()
	if (action == "UPDATE"):
		title = ET.SubElement(item, "title")
		title.text = content["title"]
		description = ET.SubElement(item, "description")
		description.text = content["content"]
		date = ET.SubElement(item, "date")
		now = datetime.datetime.now()
		date.text=now.isoformat()
	
	channel.find(".//item").addprevious(item)
	tree.write("rss.xml", pretty_print=True, xml_declaration=True)
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
		print("LOGGING::AddingInsertToFeed")
		content={"content":new_value['fullname']}
		write_rss("INSERT",content)
	if action == "UPDATE":
		content={"title": new_value["fullname"] + "'s details have been updated","content":""}
		updated_values=[]
		for val in old_value:
			if (old_value[val] != new_value[val]):
				updated_values.append(val)
		for uv in updated_values:
			content["content"] += uv + " has been updated from "+str(old_value[uv])+" to " + str(new_value[uv])

		write_rss("UPDATE",content)
		print("LOGGING::AddingUpdateToFeed")


def insert(n):
	cq = """INSERT INTO coach (fullName) VALUES (%(fullName)s) ON CONFLICT (fullName) DO NOTHING"""
	c.execute(cq,n)


def mark_checked(log):
	c.execute("update logging.t_history set checked=true where id ="+str(log))
	db.commit()
	print("LOGGING::UpdatedLog")


log = fetch_log()
if log:
	check_log(log)
	mark_checked(log[0])




