import psycopg2

con = getdb()

query = "DELETE FROM team;"
cur = con.cursor()
cur.execute(query)


query = "DELETE FROM season;"
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