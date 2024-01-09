import psycopg2
from common_functions import load_json
from unidecode import unidecode
CONFIG = load_json('check_points/CONFIG.json')
database_enable = CONFIG['DATA_BASE']

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
	con.commit()

def save_sport_database(sport_dict):
	try:
		query = "INSERT INTO sport VALUES(%(sport_id)s, %(is_active)s, %(desc_i18n)s,\
										 %(logo)s, %(sport_mode)s, %(name_i18n)s, %(point_name)s, %(name)s)"
		cur = con.cursor()
		cur.execute(query, sport_dict)
		con.commit()
	except:
		con.rollback()

def get_dict_sport_id():
	query = "SELECT sport.name, sport.sport_id FROM sport"
	# 
	# -- WHERE team.sport_id = '{}'
	cur = con.cursor()
	cur.execute(query)	
	dict_results = {row[0] : row[1] for row in cur.fetchall()}
	return dict_results


def save_league_info(dict_ligue_tornament):	
	query = "INSERT INTO league VALUES(%(league_id)s, %(league_country)s, %(league_logo)s, %(league_name)s, %(league_name_i18n)s, %(sport_id)s)"
	cur = con.cursor()																			 
	cur.execute(query, dict_ligue_tornament)														 
	con.commit()																					 

def save_season_database(season_dict):
	query = "INSERT INTO season VALUES(%(season_id)s, %(season_name)s, %(season_end)s,\
									 %(season_start)s, %(league_id)s)"
	cur = con.cursor()
	cur.execute(query, season_dict)
	con.commit()

def save_tournament(dict_tournament):
	query = "INSERT INTO tournament VALUES(%(tournament_id)s, %(team_country)s, %(desc_i18n)s,\
									 %(end_date)s, %(logo)s, %(name_i18n)s, %(season)s, %(start_date)s, %(tournament_year)s)"
	cur = con.cursor()
	cur.execute(query, dict_tournament)
	con.commit()

def save_team_info(dict_team):
	query = "INSERT INTO team VALUES(%(team_id)s, %(team_country)s, %(team_desc)s,\
	 %(team_logo)s, %(team_name)s, %(sport_id)s)"
	cur = con.cursor()																			 
	cur.execute(query, dict_team)														 
	con.commit()

def save_league_team_entity(dict_team):
	query = "INSERT INTO league_team VALUES(%(instance_id)s, %(team_meta)s, %(team_position)s, %(league_id)s, %(season_id)s, %(team_id)s)"	
	cur = con.cursor()
	cur.execute(query, dict_team)
	con.commit()

def save_player_info(dict_team):	
	query = "INSERT INTO player VALUES(%(player_id)s, %(player_country)s, %(player_dob)s,\
	 %(player_name)s, %(player_photo)s, %(player_position)s)"
	cur = con.cursor()
	cur.execute(query, dict_team)
	con.commit()

def save_team_players_entity(player_dict):
	query = "INSERT INTO team_players_entity VALUES(%(player_meta)s, %(season_id)s, %(team_id)s,\
	 %(player_id)s)"
	cur = con.cursor()
	cur.execute(query, player_dict)
	con.commit()

def get_team_id(league_id, season_id, team_name):
	query = """
	SELECT t2.team_id \
	FROM league_team AS t1\
	JOIN team AS t2 ON t1.team_id = t2.team_id\
	WHERE t1.league_id = '{}' AND t1.season_id = '{}' AND t2.team_name = '{}'""".format(league_id, season_id, team_name)

	cur = con.cursor()
	cur.execute(query)
	results = cur.fetchone()
	return results[0]

def get_seasons(league_id, season_name):
	query = "SELECT season_name, season_id FROM season	WHERE league_id ='{}' and season_name = '{}';".format(league_id, season_name)
	cur = con.cursor()
	cur.execute(query)	
	results = [row[0] for row in cur.fetchall()]
	for row in cur.fetchall():
		print(row)
	return results

def get_list_id_teams(sport_id, team_country, team_name):
	query = "SELECT team_id FROM team WHERE sport_id ='{}' and team_country = '{}' and team_name = '{}';".format(sport_id, team_country, team_name)
	cur = con.cursor()
	cur.execute(query)	
	results = [row[0] for row in cur.fetchall()]
	return results

def get_dict_results(table= 'league', column = 'sport_id, league_country, league_name, league_id'):
	query = "SELECT {} FROM {};".format(column, table)
	cur = con.cursor()
	cur.execute(query)
	# dict_results = {unidecode('-'.join(row[0].replace('&', '').split())).upper() + '_'\
	#  				+ unidecode('-'.join(row[1].split())).upper() : row[2] for row in cur.fetchall()}
	dict_results = {row[0] + '_'+ row[1] + '_' + row[2]: row[3] for row in cur.fetchall()}
	return dict_results

def get_dict_teams(sport_id = 'FOOTBALL'):
	query = """
	SELECT league.league_country, team.team_name, team.team_id\
	FROM team \
	JOIN league_team ON team.team_id = league_team.team_id\
	JOIN league league_team.league_id = league.league_id	
	WHERE team.id_sport = '{}'""".format(sport_id)

	cur = con.cursor()
	cur.execute(query)

	dict_results = {unidecode('-'.join(row[0].replace('&', '').split() ) ).upper():\
					{'team_name': unidecode('-'.join(row[1].split() ) ).upper(),\
	 				 'team_id': row[2]} for row in cur.fetchall()}
	return dict_results

def get_dict_league_ready(sport_id = 'TENNIS'):
	query = """
		SELECT team.sport_id, team.team_country, league.league_country, team.team_name, team.team_id
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
	for row in results:
		dict_results.setdefault(row[0], {}).setdefault(row[1], {}).setdefault(row[2], {})[row[3]] = {'team_id': row[4]}	

	return dict_results

def save_math_info(dict_match):
	query = "INSERT INTO match VALUES(%(match_id)s, %(match_country)s, %(end_time)s,\
	 %(match_date)s, %(name)s, %(place)s, %(start_time)s, %(league_id)s, %(stadium_id)s, %(rounds)s ,%(season_id)s)"
	cur = con.cursor()
	cur.execute(query, dict_match)
	con.commit()

def save_details_math_info(dict_match):
	query = "INSERT INTO match_detail VALUES(%(match_detail_id)s, %(home)s, %(visitor)s,\
	 %(match_id)s, %(team_id)s)"
	cur = con.cursor()
	cur.execute(query, dict_match)
	con.commit()

def save_score_info(dict_match):
	query = "INSERT INTO score_entity VALUES(%(score_id)s, %(points)s, %(match_detail_id)s)"
	cur = con.cursor()
	cur.execute(query, dict_match)
	con.commit()

def save_stadium(dict_match):
	query = "INSERT INTO stadium VALUES(%(stadium_id)s, %(capacity)s, %(country)s,\
	 %(desc_i18n)s, %(name)s, %(photo)s)"
	cur = con.cursor()
	cur.execute(query, dict_match)
	con.commit()

def get_rounds_ready(league_id, season_id):
	query = "SELECT DISTINCT rounds FROM match WHERE league_id = '{}' AND season_id = '{}';".format(league_id, season_id)	
	print("query inside rounds ready: ")
	print(query)
	cur = con.cursor()
	cur.execute(query)	
	results = [row[0] for row in cur.fetchall()]	
	return results

def check_player_duplicates(player_country, player_name, player_dob):
	query = "SELECT player_id FROM player WHERE player_country ='{}' AND player_name ='{}' AND player_dob ='{}';".format(player_country, player_name, player_dob)
	cur = con.cursor()
	cur.execute(query)	
	results = [row[0] for row in cur.fetchall()]
	return results


if database_enable:
	con = getdb()