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


if database_enable:
	con = getdb()
# 	SELECT stadium.stadium_id
# 	FROM stadium
# 	JOIN match ON stadium.stadium_id = match.stadium_id
# 	JOIN league ON league.league_id = match.league_id
# 	WHERE league.sport_id = 'toce7765';

# ### DELETE MATCH ROWS
# USING match
# #### 	WORKING 
# SELECT score_entity.match_detail_id
# FROM league
# JOIN match ON league.league_id = match.league_id
# JOIN match_detail ON match.match_id = match_detail.match_id
# JOIN score_entity ON match_detail.match_detail_id = score_entity.match_detail_id
# WHERE league.sport_id = 'toce7765';

# DELETE FROM match
# WHERE match_id IN (
#     SELECT match.match_id
#     FROM league
#     JOIN match ON league.league_id = match.league_id    
#     WHERE league.sport_id = 'toce7765');

# SELECT COUNT(*)
#     FROM league
#     JOIN match ON league.league_id = match.league_id    
#     WHERE league.sport_id = 'toce7765'

# # 	WORKING 
# DELETE score_entity
# FROM league
# JOIN match ON league.league_id = match.league_id
# JOIN match_detail ON match.match_id = match_detail.match_id
# JOIN score_entity ON match_detail.match_detail_id = score_entity.match_detail_id
# WHERE league.sport_id = 'toce7765';


# DELETE FROM score_entity
# WHERE league.league_id = match.league_id
#   AND league.sport_id = 'toce7765';



# ### DELETE STADIUM ROWS
# DELETE FROM match_detail
# USING match
# JOIN league ON league.league_id = match.league_id
# WHERE stadium.stadium_id = match.stadium_id
#   AND league.sport_id = 'toce7765';

# """DELETE MATCH
# 	FROM match
# 	JOIN league ON league.league_id = match.league_id
# 	WHERE league.sport_id ='toce7765' """
# ##########################################################################
# DELETE FROM player
# WHERE player_id IN (SELECT player.player_id
# FROM team
# JOIN team_players_entity ON team.team_id = team_players_entity.team_id
# JOIN player ON team_players_entity.player_id = player.player_id
# WHERE team.sport_id = 'toce7765');


# DELETE FROM player
# WHERE player_id IN ();

def get_players_id(sport_id):
	query = """SELECT player.player_id
			FROM team
			JOIN team_players_entity ON team.team_id = team_players_entity.team_id
			JOIN player ON team_players_entity.player_id = player.player_id
			WHERE team.sport_id = '{}' """.format(sport_id)
	cur = con.cursor()
	cur.execute(query)	
	return [result[0] for result in cur.fetchall()]

def del_players_entity(player_ids):
	query = """DELETE FROM team_players_entity WHERE player_id IN ('{}');""".format("','".join(map(str, player_ids)) )
	cur = con.cursor()
	cur.execute(query)
	con.commit()

def del_players(player_ids):
	query = """DELETE FROM player WHERE player_id IN ('{}');""".format("','".join(map(str, player_ids)) )
	cur = con.cursor()
	cur.execute(query)
	con.commit()

playesr_id_list = get_players_id('toce7765')
print(playesr_id_list)

print("#"*80)
player_ids2 = ['dtxi09524', 'dtxi09524']
del_players_entity(player_ids)
del_players(player_ids)
##########################################################################3