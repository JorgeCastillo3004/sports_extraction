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