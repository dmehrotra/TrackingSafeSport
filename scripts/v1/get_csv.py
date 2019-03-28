import sys
import psycopg2
import csv

import csv

f = open(sys.argv[1])
csv_f = csv.reader(f)
l=[]
nl=[]

db = psycopg2.connect("dbname=safesport")
c = db.cursor()

for row in csv_f:
	if row:
		n = {"fullName":row[0]}
		cq = """INSERT INTO coach (fullName) VALUES (%(fullName)s) ON CONFLICT (fullName) DO NOTHING"""
		c.execute(cq,n)


db.commit()

# common names table
##import common names.sh

# coach names table
# log table

# autocomplete.sh - runs once every minute to check to see if there are any new autocompletes and adds them to the database
# updatedetails.sh runs once every minute to check a name for updates.  If theres an update log it. 
# notify.sh notify...make rss api?