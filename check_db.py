import psycopg2
import argparse
from common_functions import *
from data_base import *
from datetime import date, timedelta, datetime


parser = argparse.ArgumentParser()
parser.add_argument('--value', type=str, default='zyltsnwfmwakyjuj07169')
parser.add_argument('--table', type=str, default='league_team')
parser.add_argument('--column', type=str, default='league_id')
parser.add_argument('--stadium', type=str, default='lavyynrspzzzlphf08860')
parser.add_argument('--league_id', type=str, default='qnbwpoczwqqaetye99354')
parser.add_argument('--table_search', type=str, default='qnbwpoczwqqaetye99354')

args = parser.parse_args()
value = args.value
table = args.table
column = args.column
stadium = args.stadium
league_id = args.league_id
table_search = args.table_search

def getdb():
	return psycopg2.connect(
			host="localhost",
			user="wohhu",
			password="caracas123",
	dbname='sports_db',
	)

con = getdb()

cleaned_text = '15.12. 14:45'#re.findall(r'\d+\.\d+\.\s+\d+\:\d+', date)[0]
dt_object = datetime.strptime(cleaned_text, '%d.%m. %H:%M')
dt_object = dt_object.replace(year=2023)
# Extract date and time
date = dt_object.date()
time = dt_object.time()
print(date)
print(time)

# query = "SELECT {} FROM {} WHERE {}.league_id ='{}';".format(column, table, table_search, value)
query = "SELECT DISTINCT league_id FROM league_team;"
print(query)
cur = con.cursor()
cur.execute(query)
results  = cur.fetchall()

print("######## UNIQUE LEAGUE IDs ######## ")
for league_id in results:
	print(league_id)

query = "SELECT DISTINCT stadium_id FROM stadium;"
print(query)
cur = con.cursor()
cur.execute(query)
results  = cur.fetchall()

print("######## UNIQUE STADIUM IDs ######## ")
for stadium_id in results:
	print(stadium_id)

match_info = {"match_id":random_id(), "match_country":'VENEZUELA',"end_time":time,"match_date":date,\
			"name":"RIO JANEIRO","place":"RINCONADA","start_time":time,"league_id":league_id[0], "stadium_id":stadium_id[0]}
print(match_info, '\n')
print("match_info['league_id'], match_info['season_id']")
print(match_info['league_id'], match_info['stadium_id'])

def save_math_info(dict_match):
	print("dict_match INSIDE: ",dict_match)
	query = "INSERT INTO match VALUES(%(match_id)s, %(match_country)s, %(end_time)s,\
	 %(match_date)s, %(name)s, %(place)s, %(start_time)s, %(league_id)s, %(stadium_id)s)"
	cur = con.cursor()
	cur.execute(query, dict_match)
	con.commit()

save_math_info(match_info)

print("Register saved in match table")