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

	image_url = profile_block.find_element(By.XPATH, './/img').get_attribute('src')
	image_path = random_name(folder = 'images/players/')
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

def navigate_through_players(driver, sport_id, country_league, team_name, season_id, team_id, list_squad, dict_players_ready):
	players_ready = dict_players_ready[sport_id][country_league][team_name]

	for player_link in list_squad:
		wait_update_page(driver, player_link, 'container__heading')
		player_dict = get_player_data(driver)			
		player_dict['season_id'] = season_id
		player_dict['team_id'] = team_id
		player_dict['player_meta'] = ''			
		print("Save player info in database")
		# name_ = player_dict['player_country'] + '_' + player_dict['player_name']
		print(player_dict)
		print("Input name: ", player_dict['player_name'])
		player_dict['player_name'] = player_dict['player_name'].replace("'", " ")
		print("out name: ", player_dict['player_name'])
		players_ready = check_player_duplicates(player_dict['player_country'], player_dict['player_name'], player_dict['player_dob'])
		print("players_ready ", players_ready)
		if len(players_ready) == 0:
			# players_ready.append(name_)
			if database_enable:
				save_player_info(player_dict) # player
				save_team_players_entity(player_dict) # team_players_entity
				# dict_players_ready[sport_id][country_league][team_name] = players_ready
				# save_check_point('check_points/players_ready.json', dict_players_ready)
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

def players(driver):
	sports_dict = load_check_point('check_points/leagues_info.json')
	dict_sport_id = load_check_point('check_points/sports_id.json')
	inverted_dict = {value: key for key, value in dict_sport_id.items()}
	dict_players_ready = load_check_point('check_points/players_ready.json')
	for sport_id, sport_dict in sports_dict.items():	
		for country_league, country_league_urls in sport_dict.items():			
			file_country_league_season = 'check_points/leagues_season/{}_{}.json'.format(sport_id, country_league)
			print(file_country_league_season)
			
			if os.path.isfile(file_country_league_season):				
				print("Start extraction for league: ", country_league)
				dict_country_league_season = load_check_point(file_country_league_season)

				for team_name, team_info in dict_country_league_season.items():
					wait_update_page(driver, team_info['team_url'], "container__heading")
					print(" START PLAYER EXTRACTION")
					print(team_info['team_url'])
					try:
						squad_button = driver.find_element(By.CLASS_NAME, 'tabs__tab.squad')
					except:
						squad_button = driver.find_element(By.XPATH, '//a[@title="Squad"]')
					squad_url = squad_button.get_attribute('href')
					wait_update_page(driver, squad_url, 'heading')
					# sport_name = inverted_dict[sport_id]
					print("squad_url URL: ", squad_url)
					list_squad = get_squad_list(driver, sport_id = sport_id)
					dict_players_ready = get_check_point(dict_players_ready, sport_id, country_league, team_name)
					navigate_through_players(driver, sport_id, country_league, team_name, country_league_urls['season_id'],\
										 team_info['team_id'], list_squad, dict_players_ready)

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