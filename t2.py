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

def get_list_results(league_id, table= 'season', column = 'season_name'):
	query = "SELECT {} FROM {}	WHERE league_id ='{}';".format(column, table, league_id)

	cur = con.cursor()
	cur.execute(query)	
	results = [row[0] for row in cur.fetchall()]
	return results

def get_dict_results(table= 'league', column = 'league_name, league_id'):
	query = "SELECT {} FROM {};".format(column, table)

	cur = con.cursor()
	cur.execute(query)	
	results_dict = [{row[0]: row[1]} for row in cur.fetchall()]
	return results_dict

con = getdb()

dict_leagues = get_dict_results(table= 'league', column = 'league_name, league_id')

league_info = dict_leagues[0]

print("league_info", league_info, type(league_info))
print("league_info.keys()[0]", league_info.keys(), type(league_info.keys()))

list_keys = list(league_info.keys())
print("Type list_keys ", type(list_keys))

league_id = league_info[list_keys[0]]

print("Make search for: ", league_id)
list_season = get_list_results(league_id, table= 'season', column = 'season_name')
print(list_season)

league_id = 'jdhvogpiqkledmte95214'
list_season = get_list_results(league_id, table= 'season', column = 'season_name')

print(list_season)


for league_name in list_leagues:
	print(league_name)