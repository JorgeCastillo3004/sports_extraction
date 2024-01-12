from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import psycopg2
import shutil

from common_functions import *
from data_base import *

#####################################################################
#					TENNIS PLAYER INFO EXTRACTION 					#
#####################################################################
def get_player_data_tennis(driver):
	dict_player_full_info = get_all_player_info_tennis(driver)    

	profile_block = driver.find_element(By.CLASS_NAME, 'container__heading')
	player_country = profile_block.find_element(By.XPATH, './/span[@class="breadcrumb__text"]').text
	if 'age' in dict_player_full_info.keys():
		date_str = dict_player_full_info['age'].split()[1].replace('(','').replace(')','')
		player_dob = datetime.strptime(date_str, "%d.%m.%Y")
	else:
		player_dob = datetime.strptime('01.01.1900', "%d.%m.%Y") 

	player_name = profile_block.find_element(By.XPATH, './/div[@class="heading__name"]').text
	player_name = clean_field(player_name)

	image_url = profile_block.find_element(By.XPATH, './/img').get_attribute('src')
	image_path = random_name_logos(player_name, folder = 'images/players/')	
	save_image(driver, image_url, image_path)
	player_photo = image_path.replace('images/players/','')
	
	player_id = random_id()
	player_dict = {'player_id':player_id, 'player_country':player_country, 'player_dob':player_dob, 'player_name':player_name,\
	 'player_photo':player_photo, 'player_position':''}
	return player_dict

def get_all_player_info_tennis(driver):
	player_block = driver.find_element(By.XPATH, '//div[@class="heading__info"]')
	lines = player_block.find_elements(By.XPATH, './/div[contains(@class, "heading__info")]')  # [contains(text(), "Age")]/span'
	dict_info = {}
	for line in lines:
		print("Curren_line: ",line.text, "#")
		if len(line.text) != 0 and ":" in line.text:
			tag, field = line.text.split(":")
			dict_info[tag] = field
	dict_info
	return dict_info

#####################################################################
#					SQUAD INFO EXTRACTION 							#
#####################################################################

def get_all_player_info(driver):
	player_block = driver.find_element(By.CLASS_NAME, 'playerHeader__wrapper')
	lines = player_block.find_elements(By.XPATH, './/span')
	dict_info = {}
	value = ''
	count = 0
	for line in lines:
		HTML = line.get_attribute('outerHTML')
		if 'info-bold' in HTML:
			if count != 0:
				dict_info[tag] = value
				value = ''
			tag = line.text.replace(' ','_').replace(':','').lower()
			count += 1
		else:        
			value = value + ' ' + line.text
	dict_info[tag] = value        
	return dict_info

def get_player_data(driver):
	dict_player_full_info = get_all_player_info(driver)

	profile_block = driver.find_element(By.ID, 'player-profile-heading')
	player_country = profile_block.find_element(By.XPATH, './/div/h2/span[2]').text
	if 'age' in dict_player_full_info.keys():
		date_str = dict_player_full_info['age'].split()[1].replace('(','').replace(')','')
		player_dob = datetime.strptime(date_str, "%d.%m.%Y")
	else:
		player_dob = datetime.strptime('01.01.1900', "%d.%m.%Y") 

	player_name = profile_block.find_element(By.CLASS_NAME, 'typo-participant-heading').text		
	
	image_url = profile_block.find_element(By.XPATH, './/div/div/div/img').get_attribute('src')
	image_path = random_name(folder = 'images/players/')
	save_image(driver, image_url, image_path)
	player_photo = image_path.replace('images/players/','')

	player_position = profile_block.find_element(By.CLASS_NAME, 'typo-participant-info-bold').text
	player_id = random_id()
	player_dict = {'player_id':player_id, 'player_country':player_country, 'player_dob':player_dob, 'player_name':player_name,\
	 'player_photo':player_photo, 'player_position':player_position}
	return player_dict

def get_squad_list(driver, sport_id = 'barketball'):
    if sport_id.lower() == 'football':
        sport_id = 'soccer'
    else:
        sport_id = sport_id.lower()
    # Function to get positions and url for each player
    class_name = '//div[@class="lineup lineup--{}"]'.format(sport_id)
    print("class_name: ", class_name)
    lineups_blocks = driver.find_element(By.XPATH, class_name)

    player_links = lineups_blocks.find_elements(By.XPATH, './/a[@class="lineup__cell lineup__cell--name"]')

    player_links = [link.get_attribute('href') for link in player_links]
    return player_links

def navigate_through_players(driver, country_league, team_name, season_id, team_id, list_squad, global_check_point):

	for player_link in list_squad:
		##########  ENABLE CHECK POINT PLAYER ############################
		if global_check_point['M6']['player'] != '':
			if global_check_point['M6']['player'] == player_link:
				enable_player = True
		else:
			enable_player = True
		#################################################################		

		if enable_player:			
			wait_update_page(driver, player_link, 'container__heading')
			player_dict = get_player_data(driver)			
			player_dict['season_id'] = season_id
			player_dict['team_id'] = team_id
			player_dict['player_meta'] = ''		
			# name_ = player_dict['player_country'] + '_' + player_dict['player_name']		
			player_dict['player_name'] = player_dict['player_name'].replace("'", " ")		
			players_ready = check_player_duplicates(player_dict['player_country'], player_dict['player_name'], player_dict['player_dob'])
			print('-e-', end = '')
			if len(players_ready) == 0:
				# players_ready.append(name_)
				if database_enable:
					save_player_info(player_dict) # player
					save_team_players_entity(player_dict) # team_players_entity
			global_check_point['M6']['player'] = player_link
			save_check_point('check_points/global_check_point.json', global_check_point)
	global_check_point['M6']['player'] = ''
	save_check_point('check_points/global_check_point.json', global_check_point)
		
	# 	break
	# break

def get_check_point(dict_players_ready, sport_id, country_league, team_name):
	if sport_id in list(dict_players_ready.keys()):
		if country_league in list(dict_players_ready[sport_id].keys()):
			if team_name in list(dict_players_ready[sport_id][country_league].keys()):
				list_players_ready = dict_players_ready[sport_id][country_league][team_name]
			else:
				dict_players_ready[sport_id][country_league][team_name] = []
		else:		
			dict_players_ready[sport_id][country_league] = {}
			dict_players_ready[sport_id][country_league][team_name] = []
	else:
		dict_players_ready[sport_id] = {}
		dict_players_ready[sport_id][country_league] = {}
		dict_players_ready[sport_id][country_league][team_name] = []
	return dict_players_ready

def players(driver, list_sports):
	leagues_info_json = load_check_point('check_points/leagues_info.json')	
	dict_sport_id = get_dict_sport_id()	# GET DICT SPORT FROM DATABASE
	inverted_dict = {value: key for key, value in dict_sport_id.items()}
	
	#############################################################
	# 				SECTION TO LOAD CHECK POINT					#
	#############################################################

	global_check_point = load_check_point('check_points/global_check_point.json')
	if 'M6' in global_check_point.keys():			
		sport_point = global_check_point['M6']['sport']
		league_point = global_check_point['M6']['league']
		team_point  = global_check_point['M6']['team_name']		
	else:
		global_check_point['M6'] = {}
		sport_point = ''
		league_point = ''
		team_point  = ''
		global_check_point['M6']['player'] = ''

	enable_sport = False
	enable_league = False
	enable_team = False

	#############################################################
	# 				MAIN LOOP OVER LIST SPORTS 					#
	#############################################################
	for sport_name in list_sports:		
		print_section(sport_name, space_ = 50)
		##########  ENABLE CHECK POINT SPORT #############
		if sport_point != '':
			if sport_point == sport_name:
				enable_sport = True
		else:
			enable_sport = True
		#################################################
		if enable_sport:
			print(leagues_info_json.keys())
			global_check_point['M6']['sport'] = sport_name
			for country_league, league_info in leagues_info_json[sport_name].items():
				print_section(country_league, space_ = 30)
				##########  ENABLE CHECK POINT LEAGUE #############
				print("country_league: ", country_league)
				if league_point != '':
					if league_point == country_league:
						enable_league = True
				else:
					enable_league = True
				#################################################				
				# for team_name, country_league_urls in league_info.items():
				##########  ENABLE CHECK POINT LEAGUE #############
				# if league_point != '':
				# 	if league_point == country_league:
				# 		enable_league = True
				# else:
				# 	enable_league = True
				#################################################
				path_leagues_teams_info = 'check_points/leagues_season/{}/{}.json'.format(sport_name, country_league)
				
				if os.path.isfile(path_leagues_teams_info) and enable_league:
					print("Start extraction for league: ", country_league)
					global_check_point['M6']['league'] = country_league
					#############################################################
					# 				LOAD TEAMS INFO 		 					#
					#############################################################
					dict_country_league_season = load_check_point(path_leagues_teams_info)

					for team_name, team_info in dict_country_league_season.items():
						print_section(team_name, space_ = 20)
						##########  ENABLE CHECK POINT TEAM #############
						if team_point != '':
							if team_point == team_name:
								enable_team = True
						else:
							enable_team = True
						#################################################
						if enable_team:
							# NAVIGATE THROUGH TEAMS
							global_check_point['M6']['team_name'] = team_name
							wait_update_page(driver, team_info['team_url'], "container__heading")
							print(" START PLAYER EXTRACTION")
							print(team_info['team_url'])
							# LOAD SQUAD URL, LOADED FROM TEAM INFO
							try:
								squad_button = driver.find_element(By.CLASS_NAME, 'tabs__tab.squad')
							except:
								squad_button = driver.find_element(By.XPATH, '//a[@title="Squad"]')
							squad_url = squad_button.get_attribute('href')

							# WAIT UNTIL COMPLETE LOAD
							wait_update_page(driver, squad_url, 'heading')
							# sport_name = inverted_dict[sport_id]

							# GET LIST OF PLAYERS AVAILABLES
							list_squad = get_squad_list(driver, sport_id = sport_name)

							# NAVIGATE AND EXTRACT INFO FROM EACH PLAYER LINK
							navigate_through_players(driver, country_league, team_name, league_info['season_id'],\
												 team_info['team_id'], list_squad, global_check_point)
							# global_check_point['M6'] = {'sport':sport_name, 'league':country_league, 'team_name':team_name}

CONFIG = load_json('check_points/CONFIG.json')
database_enable = CONFIG['DATA_BASE']
if database_enable:
	con = getdb()

# if __name__ == "__main__":  	
# 	driver = launch_navigator('https://www.flashscore.com', database_enable)
# 	login(driver, email_= "jignacio@jweglobal.com", password_ = "Caracas5050@\n")	
# 	main_m6(driver)
# 	if database_enable:
# 		con.close()
# 	driver.quit()