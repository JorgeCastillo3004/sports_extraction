import psycopg2

def getdb():
	return psycopg2.connect(
			host="localhost",
			user="wohhu",
			password="caracas123",
	dbname='sports_db',
	)

con = getdb()

query = "DELETE FROM league_team"
print("delete table league_team")
cur = con.cursor()
cur.execute(query)

query = "DELETE FROM season"
print("delete table season")
cur = con.cursor()
cur.execute(query)

query = "DELETE FROM team"
print("delete table team")
cur = con.cursor()
cur.execute(query)

query = "DELETE FROM league"
print("delete table league")
cur = con.cursor()
cur.execute(query)

query = "DELETE FROM sport"
print("delete table sport")
cur = con.cursor()
cur.execute(query)

query = "DELETE FROM tournament"
print("delete table tournament")
cur = con.cursor()
cur.execute(query)

cur.close()