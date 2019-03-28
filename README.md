[![N|Solid](https://i.kinja-img.com/gawker-media/image/upload/s--FAznK8A_--/c_scale,f_auto,fl_progressive,q_80,w_1600/ewy0z4g29vfgheefkhyx.png)]()
# Tracking SafeSport
SafeSport is the U.S. Olympic Committee's program to handle reports of possible sexual abuse in Olympic sports. This is some code to track changes to the database.  
### Dependencies 
postgres,psycopg2,csv,requests,json
### Installation
1. `createdb safesport` -- create psql db.
2. `psql safesport < db/db.sql`
3. `psql safesport < db/import_common_names.sql` -- import 300 of the most common Male names
### Usage
 1. `python 1_get_autocomplete_from_commonname.py <OPTIONAL NAME>` -- this will get a list of coaches that autocomplete from a single common name on SafeSport's website.
2. `python 2_get_coach_details.py <OPTIONAL NAME>` -- This will get the details of a given coach from SafeSport. 
3. `python 3_check_log.py` -- this will check the log table to identify what logs should be included in the RSS feed.  
### Notes 
- The idea here is that each script runs independelty.  You can set the frequency through a CRON job.  This is just in case SafeSport decides to rate limit. Each script will only do what its supposed to do for a single record. This is why you need the cron job. 

