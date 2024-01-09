import psycopg2
from datetime import date, timedelta
from datetime import datetime
import argparse



def getdb():
	return psycopg2.connect(
			host="localhost",
			user="wohhu",
			password="caracas123",
	dbname='sports_db',
	)

def save_math_info(dict_match):	
	query = "INSERT INTO match VALUES(%(match_id)s, %(match_country)s, %(end_time)s,\
	 %(match_date)s, %(name)s, %(place)s, %(start_time)s, %(league_id)s, %(stadium_id)s, %(rounds)s)"
	cur = con.cursor()
	cur.execute(query, dict_match)
	con.commit()


con = getdb()
# dict_match = {'match_id': 'vwku03936', 'match_country': 'VENEZUELA', 'end_time':datetime.now(),
# 				"match_date":datetime.now(), 'name':'ENCUENDTRO', 'place':'caracas123', 'start_time':datetime.now()
# 				,'league_id':'kubw94420', 'stadium_id':'lwewwwexwfnwcybs09550', 'rounds':'RONDA 112'}
# save_math_info(dict_match)

print("Delete all from score_entity ")
query = "DELETE FROM score_entity;"
cur = con.cursor()
cur.execute(query)
con.commit()


print("Delete all from match_detail ")
query = "DELETE FROM match_detail;"
cur = con.cursor()
cur.execute(query)
con.commit()

print("Delete all from match ")
query = "DELETE FROM match;"
cur = con.cursor()
cur.execute(query)
con.commit()