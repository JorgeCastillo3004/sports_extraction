import psycopg2
from datetime import date, timedelta
from datetime import datetime
from unidecode import unidecode
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
	dict_results = {row[0]: row[1] for row in cur.fetchall()}
	return dict_results

def get_dict_league_teams(sport_id = 'TENNIS'):
	query = """
		SELECT team.sport_id, league.league_country, team.team_country, team.team_name, team.team_id
		FROM team
		JOIN league_team ON team.team_id = league_team.team_id
		JOIN league ON league_team.league_id = league.league_id
		WHERE team.sport_id = '{}'""".format(sport_id)
	# 
	# -- WHERE team.sport_id = '{}'
	cur = con.cursor()
	cur.execute(query)
	results = cur.fetchall()	
	dict_results = {}
	for row in list_results:    
	    if not row[0] in list(dict_results.keys()):
	        dict_results[row[0]] = {}
	        
	    if not row[1] in list(dict_results[row[0]].keys() ):
	        dict_results[row[1]] = {}
	    
	    if not row[2] in list(dict_results[row[0]].keys() ):
	        dict_results[row[1]][row[2]] = {'team_id':row[3]}	

	return dict_results, results

con = getdb()
sport = 'TENNIS'
dict_sport, results = get_dict_league_teams(sport_id = sport)


print("dict_sport: ", list(dict_sport.keys()))
for sport, dict_teams in dict_sport.items():
	print("sport: ", sport)
	print("keys: ", list(dict_teams.keys()))

print(results)
print("#"*50)

dict_leagues = get_dict_results(table= 'league', column = 'league_name, league_id')

print("dict_leagues: ", dict_leagues)

first_key = list(dict_leagues.keys())[0]
print("First key: ", first_key)
league_id = dict_leagues[first_key]
print(league_id)

print("Make search for: ", league_id)
list_season = get_list_results(league_id, table= 'season', column = 'season_name')
print(list_season)

league_id = 'jdhvogpiqkledmte95214'
list_season = get_list_results(league_id, table= 'season', column = 'season_name')

print(list_season)