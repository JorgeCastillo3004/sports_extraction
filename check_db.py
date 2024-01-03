import psycopg2
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--value', type=str, default='zyltsnwfmwakyjuj07169')
parser.add_argument('--table', type=str, default='league_team')
parser.add_argument('--column', type=str, default='*')
parser.add_argument('--stadium', type=str, default='lavyynrspzzzlphf08860')
args = parser.parse_args()
value = args.value
table = args.table
column = args.column
stadium = args.stadium



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

print("######### STADIUM RESULTS ############3")
query = "SELECT {} FROM stadium WHERE stadium.stadium_id ='{}';".format(column, stadium)
print("delete table league_team")
cur = con.cursor()
cur.execute(query)

results = cur.fetchall()

print("Total results: ", len(results))
for result in results:
	print(result)