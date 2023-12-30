import psycopg2
from datetime import date, timedelta
from datetime import datetime
# import argparse

from common_functions import load_json
# parser = argparse.ArgumentParser()
# parser.add_argument('--option', type=int, default=1)
# parser.add_argument('--table', type=str, default='news')
# parser.add_argument('--column', type=str, default='title')

# parser.add_argument('--option', type=int, default=1, '--table', type=str, default='news')

def getdb():
	return psycopg2.connect(
			host="localhost",
			user="wohhu",
			password="caracas123",
	dbname='sports_db',
	)


# dict_player = {'player_id': 'lisushtfctkblfct95988', 'player_country': 'ARGENTINA', 'player_dob': datetime.now(),\
# 'player_name': 'Franco Armani', 'player_photo': 'tlbddnlkwthtwhhh.jpg', 'player_position': 'Goalkeeper'}
# save_player_info(dict_player)

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

def get_list_leagues(table= 'league', column = 'league_name'):
	query = "SELECT {} FROM {};".format(column, table)

	cur = con.cursor()
	cur.execute(query)
	results = cur.fetchall()
	return results



list_leagues = get_list_leagues(table= 'league', column = 'league_name')

for league_name in list_leagues:
	print(league_name)