import requests
import json
import psycopg2
import time

db = psycopg2.connect("dbname=safesport")
c = db.cursor()
def scrape(coach):
 	print(coach[0])

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
		if val != 'id' and val !='regionDisplay':
			if response[val]:
				sql_update_query="Update coach set "+val+"='"+response[val]+"' where fullName='"+coach[0]+"'"
				c.execute(sql_update_query)
			print response[val]


def update(name):
	sql_update_query="""Update coach set checked = %s where fullName = %s"""	
	c.execute(sql_update_query,(True, str(name)))
	db.commit()

def fetch_coach():
	c.execute("SELECT * FROM coach where checked=false limit 1;")
	coach = c.fetchone()
	scrape(coach)
	update(coach[0])
	print("saved")

def throttle():
	for i in range(1,10):
		fetch_coach()

for i in range(1,100):
	throttle()
	time.sleep(20)




# curl 'https://safesport.org/api/userViolations' -H 'Origin: https://safesport.org' -H 'Accept-Encoding: gzip, deflate, br' -H 'Content-Type: application/json;charset=UTF-8' -H 'Accept: application/json, text/plain, */*' -H 'Connection: keep-alive' -H 'DNT: 1' --data-binary '{"name":{"title":"Adam Pike","image":""}}' --compressed
