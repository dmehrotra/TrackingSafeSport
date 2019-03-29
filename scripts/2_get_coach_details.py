import requests
import json
import psycopg2
import time
import sys
import datetime

db = psycopg2.connect("dbname=safesport_test")
c = db.cursor()
def scrape(coach):
	c_name=coach[0].replace("'",r"\'")
	headers = {
	    'Origin': 'https://safesport.org',
	    'Accept-Encoding': 'gzip, deflate, br',
	    'Content-Type': 'application/json;charset=UTF-8',
	    'Accept': 'application/json, text/plain, */*',
	    'Connection': 'keep-alive',
	    'DNT': '1',
	}
	data = '{"name":{"title":"'+str(coach[0])+'","image":""}}'

	r = requests.post('https://safesport.org/api/userViolations', headers=headers, data=data)

	response = json.loads(r.text)[0]
	for val in response:
		if val != 'id' and val !='regionDisplay' and val !='fullName' and val !='firstName' and val !='lastName':
			if response[val]:
				sql_update_query = "UPDATE coach set "+val+"='"+response[val]+"' where fullName = E\'"+c_name+"\'"
				c.execute(sql_update_query)
	update(c_name)


def update(name):
	sql_update_query="""Update coach set checked = %s where fullName = %s"""	
	c.execute(sql_update_query,(True, str(name)))
	db.commit()
	print("DETAILS::Updated: " + name)

def fetch_coach(d="none"):
	if (d != "none"):
		d=d.replace("'",r"\'")
		print d
		q = "SELECT * FROM coach where fullName = E\'"+d+"\' and checked=false limit 1"
	else:
		q = "SELECT * FROM coach where checked=false limit 1;"
	try:
		c.execute(q)
		coach = c.fetchone()
		print("found: "+coach[0])
		return coach
	except:
		c.execute("UPDATE coach set checked=false;")
		print("DETAILS::Restarting Cycle")
		db.commit()
		sys.exit(1)

if (len(sys.argv)>1):
	coach = fetch_coach(sys.argv[1])
else:
	coach = fetch_coach()

print("DETAILS::Scraping: " + coach[0])
scrape(coach)



