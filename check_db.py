import psycopg2
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--value', type=str, default='zyltsnwfmwakyjuj07169')
parser.add_argument('--table', type=str, default='league_team')
parser.add_argument('--column', type=str, default='*')
args = parser.parse_args()
value = args.value
table = args.table
column = args.column



def getdb():
	return psycopg2.connect(
			host="localhost",
			user="wohhu",
			password="caracas123",
	dbname='sports_db',
	)

con = getdb()


league_team , league_id = 'league_team' , 'league_id'
value = 'zyltsnwfmwakyjuj07169'
query = "SELECT {} FROM {} WHERE league_team.league_id ='{}';".format(column , table, value)
print("delete table league_team")
cur = con.cursor()
cur.execute(query)

results = cur.fetchall()

print("Total results: ", len(results))
for result in results:
	print(result)