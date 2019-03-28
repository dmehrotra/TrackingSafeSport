import csv

f = open('results.csv')
csv_f = csv.reader(f)
l=[]
nl=[]
for row in csv_f:
	if row:
		l.append(row[0])

for i in l:
  if i not in nl:
    nl.append(i)

for p in nl:
	print p