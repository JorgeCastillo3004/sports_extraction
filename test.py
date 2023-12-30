import psycopg2
from datetime import date, timedelta
from datetime import datetime
import argparse

from common_functions import load_json
parser = argparse.ArgumentParser()
parser.add_argument('--option', type=int, default=1)
parser.add_argument('--table', type=str, default='news')
parser.add_argument('--column', type=str, default='title')

# parser.add_argument('--option', type=int, default=1, '--table', type=str, default='news')

def getdb():
	return psycopg2.connect(
			host="localhost",
			user="wohhu",
			password="caracas123",
	dbname='sports_db',
	)

def save_news_database(dict_news):      
	query = "INSERT INTO news VALUES(%(news_id)s, %(news_content)s, %(image)s,\
					 %(published)s, %(news_summary)s, %(news_tags)s, %(title)s)"
	cur = con.cursor()
	cur.execute(query, dict_news)
	con.commit

def save_sport_database(sport_dict):
	try:
		query = "INSERT INTO sport VALUES(%(sport_id)s, %(is_active)s, %(desc_i18n)s,\
										 %(logo)s, %(sport_mode)s, %(name_i18n)s, %(point_name)s)"
		cur = con.cursor()
		cur.execute(query, sport_dict)
		con.commit
	except:
		con.rollback()

def save_season_database(season_dict):
	query = "INSERT INTO season VALUES(%(season_id)s, %(season_name)s, %(season_end)s,\
									 %(season_start)s, %(league_id)s)"
	cur = con.cursor()
	cur.execute(query, sport_dict)
	con.commit

def create_sports_selected_in_db():
	CONFIG_M1 = load_json('check_points/CONFIG_M1.json')
	for sport, enable_mode in CONFIG_M1['SPORTS'].items():
		sport_dict = {'sport_id' : '', 'is_active' : True, 'desc_i18n' : '', 'logo' : '', 'sport_mode' : '', 'name_i18n' : '', 'point_name': ''}
		print(enable_mode['enable'])
		if enable_mode['enable']:
			print(sport, "Save in data base:")
			sport_dict[sport] = sport_dict
			sport_dict['sport_mode'] = enable_mode['mode']
			save_sport_database(sport_dict)

def save_player_info(dict_team):
	query = "INSERT INTO player VALUES(%(player_id)s, %(player_country)s, %(player_dob)s,\
	 %(player_name)s, %(player_photo)s, %(player_position)s)"
	cur = con.cursor()
	cur.execute(query, dict_team)
	con.commit()
	print("Player insert ready")

args = parser.parse_args()
option = args.option
table = args.table
column = args.column
print("Option: ", option)
print("Table: ", table)
con = getdb()
print("Connections stablished")


# dict_player = {'player_id': 'lisushtfctkblfct95988', 'player_country': 'ARGENTINA', 'player_dob': datetime.now(),\
# 'player_name': 'Franco Armani', 'player_photo': 'tlbddnlkwthtwhhh.jpg', 'player_position': 'Goalkeeper'}
# save_player_info(dict_player)

def get_list_leagues(table= 'league', column = 'league_name'):
	query = "SELECT {} FROM {};".format(column, table)

	cur = con.cursor()
	cur.execute(query)
	results = cur.fetchall()
	return results



def get_team_id(league_id, season_id, team_name):
	query = """
	SELECT team.team_id, 
	FROM league_team AS t1
	JOIN team AS t2 ON t1.team_id = t2.team_id
	WHERE t1.league_id = '{}' AND t1.season_id = '{}' AND t2.team_name = '{}'""".format(league_id, season_id, team_name)

	cur = con.cursor()
	cur.execute(query)
	results = cur.fetchone()
	return results[0]

# list_leagues = get_list_leagues(table= 'league', column = 'league_name')

# for league_name in list_leagues:
# 	print(league_name)

# league_id, season_id, team_name ='rajhojpckdwqlzop90727', 'odbywghgtznsunmp08026', 'Boca Juniors'
# result = get_team_id(league_id, season_id, team_name)
# print("First test get team id")
# print(result)
# get_list_leagues(table= 'league', column = 'league_name')

if option  == 1:
	print("Select all from news")
	query = "SELECT {} FROM {};".format(column, table)

if option == 2:
	print("Cound duplicates")
	query = "SELECT title, COUNT(*) as count\
	FROM news\
	GROUP BY title\
	HAVING COUNT(*) > 1;"

if option == 3:
	print("Delete all")
	input_user = input("Type Y to continue")
	query = "DELETE FROM {};".format(table)

cur = con.cursor()
cur.execute(query)

if option != 3:
	results = cur.fetchall()

	for result in results:
		print(result)
	print("Total results: ", len(results))
else:
	if input_user == 'Y':
		con.commit()

cur.close()