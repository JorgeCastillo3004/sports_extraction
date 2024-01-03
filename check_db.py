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

query = "SELECT * FROM league_team WHERE league_id = 'qnbwpoczwqqaetye99354';"
print(query)
cur = con.cursor()
cur.execute(query)
results = cur.fetchall()
print("Total results: ", len(results))
for result in results:
	print(result)



# league_team , league_id = 'league_team' , 'league_id'
# value = 'qnbwpoczwqqaetye99354'
# query = "SELECT {} FROM {} WHERE {}.league_id ='{}';".format(column, table, table_search, value)
# print(query)
# cur = con.cursor()
# cur.execute(query)


# league_id = cur.fetchone()[0]
# print("league_id: ", league_id)
# print("Total results: ", len(results))
# for result in results:
# 	print(result)

cleaned_text = '15.12. 14:45'#re.findall(r'\d+\.\d+\.\s+\d+\:\d+', date)[0]

dt_object = datetime.strptime(cleaned_text, '%d.%m. %H:%M')
dt_object = dt_object.replace(year=2023)
# Extract date and time
date = dt_object.date()
time = dt_object.time()
print(date)
print(time)

match_info = {"match_id":random_id(), "match_country":'VENEZUELA',"end_time":time,"match_date":date,\
			"name":"RIO JANEIRO","place":"RINCONADA","start_time":time,"league_id":"qnbwpoczwqqaetye99354", "stadium_id":'mshhyqazpmavxwck02760'}

save_math_info(match_info)


print("######### STADIUM RESULTS ############3")
query = "SELECT {} FROM stadium WHERE stadium.stadium_id ='{}';".format(column, stadium)
cur = con.cursor()
cur.execute(query)

results = cur.fetchall()

print("Total results: ", len(results))
for result in results:
	print(result)

