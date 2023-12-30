import psycopg2

def getdb():
	return psycopg2.connect(
			host="localhost",
			user="wohhu",
			password="caracas123",
	dbname='sports_db',
	)

con = getdb()

query = "DELETE FROM league_team;"
cur = con.cursor()
cur.execute(query)

query = "DELETE FROM season;"
cur = con.cursor()
cur.execute(query)

query = "DELETE FROM team;"
cur = con.cursor()
cur.execute(query)

query = "DELETE FROM league;"
cur = con.cursor()
cur.execute(query)

query = "DELETE FROM sport;"
cur = con.cursor()
cur.execute(query)

query = "DELETE FROM tournament;"
cur = con.cursor()
cur.execute(query)

cur.close()