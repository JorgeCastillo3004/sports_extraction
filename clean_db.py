import psycopg2
from datetime import date, timedelta
from datetime import datetime
import argparse
from common_functions import load_json


def getdb():
	return psycopg2.connect(
			host="localhost",
			user="wohhu",
			password="caracas123",
	dbname='sports_db',
	)

con = getdb()

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



print("Delete all from league_team ")
query = "DELETE FROM league_team;"
cur = con.cursor()
cur.execute(query)
con.commit()



print("Delete all from season ")
query = "DELETE FROM season;"
cur = con.cursor()
cur.execute(query)
con.commit()


print("Delete all from league ")
query = "DELETE FROM league;"
cur = con.cursor()
cur.execute(query)
con.commit()


print("Delete all from team ")
query = "DELETE FROM team;"
cur = con.cursor()
cur.execute(query)
con.commit()

print("Delete all from sport ")
query = "DELETE FROM sport;"
cur = con.cursor()
cur.execute(query)
con.commit()

cur.close()