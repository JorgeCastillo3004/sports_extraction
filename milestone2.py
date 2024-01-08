from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import psycopg2
import shutil

from common_functions import *
# from main import database_enable
# from common_functions import utc_time_naive
from data_base import *

# import argparse
# parser = argparse.ArgumentParser()
# parser.add_argument('--db', type=bool, default=False)
# args = parser.parse_args()
# database_enable = args.db

# print("Type: ", type(database_enable))

# print("database_enable: ", database_enable)
# if database_enable:
# 	print("Write on db activate")
# else:
# 	print("Don't write in database")

def getdb():
	return psycopg2.connect(
				host="localhost",
				user="wohhu",
				password="caracas123",
		dbname='sports_db',
		)

def get_sports_links(driver):
	wait = WebDriverWait(driver, 10)
	buttonmore = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'menuMinority__arrow')))

	mainsports = driver.find_elements(By.XPATH, '//div[@class="menuTop__items"]/a')

	dict_links = {}

	for link in mainsports:
		sport_name = '_'.join(link.text.split())
		sport_url = link.get_attribute('href')
		dict_links[sport_name] = sport_url

	buttonmore.click()

	list_links = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'menuMinority__item')))

	list_links = driver.find_elements(By.CLASS_NAME, 'menuMinority__item')

	for link in list_links:
		sport_name = '_'.join(link.text.split())
		sport_url = link.get_attribute('href')
		if sport_name == '':
			sport_name = sport_url.split('/')[-2].upper()
		dict_links[sport_name] = sport_url
		
	buttonminus = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'menuMinority__arrow')))
	buttonminus.click()
	
	return dict_links

def create_sport_dict(sport_mode, sport_name):
	sport_id = random_id_short()
	sport_dict = {'sport_id' : sport_id, 'is_active' : True, 'desc_i18n' : '', 'logo' : '',\
	'sport_mode' : sport_mode, 'name_i18n' : '', 'point_name': '', 'name':sport_name}
	return sport_dict, sport_id

def click_news(driver):
	wait = WebDriverWait(driver, 10)
	newsbutton = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'tabs__tab.news')))  # "tabs__tab news selected"
	newsbutton.click()

def check_pin(driver):
	pin = driver.find_element(By.ID, "toMyLeagues")
	if 'pinMyLeague active 'in pin.get_attribute('outerHTML'):
		return True
	else:
		return False

def get_league_data(driver, league_team, sport_id):
	block_ligue_team = driver.find_element(By.CLASS_NAME, 'container__heading')
	sport = block_ligue_team.find_element(By.XPATH, './/h2[@class= "breadcrumb"]/a[1]').text
	league_country = block_ligue_team.find_element(By.XPATH, './/h2[@class= "breadcrumb"]/a[2]').text
	league_name = block_ligue_team.find_element(By.CLASS_NAME,'heading__title').text
	season_name = block_ligue_team.find_element(By.CLASS_NAME, 'heading__info').text
	image_url = block_ligue_team.find_element(By.XPATH, './/div[@class= "heading"]/img').get_attribute('src')
	image_path = random_name_logos(league_team, folder = 'images/logos/')
	save_image(driver, image_url, image_path)
	image_path = image_path.replace('images/logos/','')
	league_id = random_id()
	season_id = random_id()	
	ligue_tornamen = {"sport_id":sport_id,"league_id":league_id,"season_id":season_id, 'sport':sport, 'league_country': league_country,
					 'league_name': league_name,'season_name':season_name, 'league_logo':image_path,
					  'league_name_i18n':'', 'season_end':datetime.now(), 'season_start':datetime.now()}
	return ligue_tornamen

def get_teams_data(driver, sport_id, league_id, season_id, team_info):
	block_ligue_team = driver.find_element(By.CLASS_NAME, 'container__heading')


	sport = block_ligue_team.find_element(By.XPATH, './/h2[@class= "breadcrumb"]/a[1]').text
	team_country = block_ligue_team.find_element(By.XPATH, './/h2[@class= "breadcrumb"]/a[2]').text
	team_name = block_ligue_team.find_element(By.CLASS_NAME,'heading__title').text


	stadium = block_ligue_team.find_element(By.CLASS_NAME, 'heading__info').text
	image_url = block_ligue_team.find_element(By.XPATH, './/div[@class= "heading"]/img').get_attribute('src')
	image_path = random_name(folder = 'images/logos/')
	save_image(driver, image_url, image_path)
	logo_path = image_path.replace('images/logos/','')
	team_id = random_id()
	instance_id = random_id()	
	meta_dict = str({'statistics':team_info['statistics'], 'last_results':team_info['last_results']})
	team_info = {"team_id":team_id,"team_position":team_info['position'], "team_country":team_country,"team_desc":'', 'team_logo':logo_path,\
			 'team_name': team_name,'sport_id': sport_id, 'league_id':league_id, 'season_id':season_id,\
			 'instance_id':instance_id, 'team_meta':meta_dict, 'stadium':stadium}
	return team_info

def find_ligues_torneos(driver):
	wait = WebDriverWait(driver, 5)
	xpath_expression = '//div[@id="my-leagues-list"]'
	leagues_info = wait.until(EC.visibility_of_element_located((By.XPATH, xpath_expression)))
	dict_liguies = {}
	if not "To select your leagues " in leagues_info.text:
		# ligues = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@id="my-leagues-list"]/div/div/a')))        
		leagues = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@id="my-leagues-list"]/div/div/a')))		
		# ligues = driver.find_elements(By.XPATH, '//div[@id="my-leagues-list"]/div/div/a')
		# print(len(ligues))
		gender = ''
		for league in leagues:
			if '#man' in league.get_attribute('outerHTML'):
				gender = "_man"
			if '#woman' in league.get_attribute('outerHTML'):
				gender = "_woman"
			# dict_liguies['_'.join(ligue.text.split())+gender] = ligue.get_attribute('href')
			league_url = league.get_attribute('href')
			dict_liguies[('_'.join(league_url.split('/')[-3:-1])+gender).upper()] = league_url
	return dict_liguies

def get_result_basketball(row):
	date = row.find_element(By.CLASS_NAME, 'event__time').text
	try:
		home_participant = row.find_element(By.CLASS_NAME, 'event__participant.event__participant--home.fontExtraBold').text
	except:
		home_participant = row.find_element(By.CLASS_NAME, 'event__participant.event__participant--home').text
	try:    
		away_participant = row.find_element(By.CLASS_NAME, 'event__participant.event__participant--away.fontExtraBold').text
	except:
		away_participant = row.find_element(By.CLASS_NAME, 'event__participant.event__participant--away').text

	home_result = row.find_element(By.CLASS_NAME, 'event__score.event__score--home').text
	away_result = row.find_element(By.CLASS_NAME, 'event__score.event__score--away').text
	html_block = row.get_attribute('outerHTML')
	print('#'*50)
	print(html_block, '\n')
	print("New regular expression: ")
	link_id = re.findall(r'id="[a-z]_\d_(.+?)\"', html_block)[0]
	url_details = "https://www.flashscore.com/match/{}/#/match-summary/match-summary".format(link_id)
	result_dict = {'date':date, 'home_participant':home_participant,'away_participant':away_participant,\
				   'home_result':home_result,  'away_result':away_result, 'link_details':url_details}
	print(result_dict, '\n')
	return result_dict

def extract_info_results__(driver):
#     xpath_expression = '//div[@class="sportName {}"]/div'.format(sport)
	xpath_expression = '//div[@class="leagues--static event--leagues results"]/div/div'
	results_block = driver.find_elements(By.XPATH, xpath_expression)

	dict_rounds = {}
	count_sub_section = 0
	count_section = 0
	for i, row in enumerate(results_block):	
		print(row.get_attribute('outerHTML'))

		try:
			# Get seruls block
			result = get_result(row)
			dict_rounds[current_id_section][event_number] = result
			event_number += 1
		except:
			try:
				# Get Rounds block				
				try:
					# Only get section name or ROUND name
					id_section_new = row.find_element(By.CLASS_NAME, 'event__title--name').text.replace(' ','_')
					#id_section = row.find_element(By.CLASS_NAME, 'event__round event__round--static').text.replace(' ','_')
				except:
					# Else get all available text
					id_section_new = row.text
					id_section_new = get_unique_key(id_section_new, dict_rounds.keys())
				if count_sub_section != 0:
					# save current dict
					# stop_validate()
					file_name = 'check_points/events/{}/round_{}.json'.format(section_name, current_id_section)
					save_check_point(file_name, dict_rounds[current_id_section])
				count_sub_section += 1
				dict_rounds[id_section_new] = {}
				event_number = 0
				current_id_section = id_section_new
			except:				
				# Get name complete section.
				print("Get name complete section: ")				
				section_name = row.find_element(By.CLASS_NAME, 'icon--flag.event__title.fl_22')
				print("section_name: ", section_name)
				section_name = section_name.replace(' ', '_')
				print("section_name: ", section_name)
				os.mkdir("check_points/events/{}".format(section_name))
		print("#"*40, '\n')
		
	return dict_rounds

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

def get_squad_dict(driver):
	# Function to get positions and url for each player
	lineups_blocks = driver.find_element(By.XPATH, '//div[@class="lineup lineup--soccer"]')
	sections = lineups_blocks.find_elements(By.CLASS_NAME, 'lineup__rows')

	dict_squad = {}
	for section in sections:
		position = section.find_element(By.CLASS_NAME, 'lineup__title').text
		players = section.find_elements(By.CLASS_NAME, 'lineup__cell.lineup__cell--name')
		list_links = []
		for player in players:        
			list_links.append(player.get_attribute('href'))
		dict_squad[position] = list_links    

	return dict_squad

def navigate_through_players(driver, dict_squad):
	for position, list_links in dict_squad.items():
		for player_link in list_links: ### URGENT DELETE #######
			wait_update_page(driver, player_link, 'container__heading')
			player_dict = get_player_data(driver)
			print(player_dict)
			print("Save player info in database")
			if database_enable:
				save_player_info(player_dict)
			break ### URGENT DELETE #######
		break ### URGENT DELETE #######

def get_sections_links(driver):
	list_links = driver.find_elements(By.XPATH, '//div[@class="tabs__group"]/a')

	dict_links = {}
	for link in list_links[1:]:    
		url_termination = link.get_attribute('href')
		dict_links[url_termination.split('/')[-2]] = url_termination
	return dict_links
#####################################################################

def create_leagues(driver, flag_news = False):
	dict_sports = load_json('check_points/sports_url_m2.json')
	dict_sport_id = get_dict_sport_id()
	conf_enable_sport = check_previous_execution(file_path = 'check_points/CONFIG_M2.json')	
	dict_sport_info = load_check_point('check_points/leagues_info.json')
	print("dict_sport_info: ", dict_sport_info)
	for sport_name, sport_info in conf_enable_sport.items():
		if sport_info['enable']:
			###################################################################
			#				SECTION GET SPORT ID 							  #
			###################################################################
			if not sport_name in dict_sport_id.keys():				
				sport_dict, sport_id = create_sport_dict(sport_info['mode'], sport_name)
				if database_enable:					
					save_sport_database(sport_dict)
			else:
				sport_id = dict_sport_id[sport_name]				
			###################################################################
			#		GET DICT WITH LEAGUES SAVED IN DATA_BASE 				  #
			#		'{ sport_id _ league_country _ league_name : league_id}   #
			#																  #
			dict_leagues_ready = get_dict_results(table= 'league', column = 'sport_id, league_country, league_name, league_id')
			print("#"*50, '\n', dict_leagues_ready, '\n', "#"*50, '\n')
			###################################################################
			#				SECTION GET CURRENT LEAGUES						  #
			###################################################################
			print("SPORT NAME: ", sport_name)
			wait_update_page(driver, dict_sports[sport_name], "container__heading")			
			dict_leagues_tornaments = find_ligues_torneos(driver)			

			###################################################################
			#		CHECK IF SPORT WAS SAVED PREVIOUSLY						  #
			###################################################################
			if sport_name in list(dict_sport_info.keys()):
				dict_leagues_ready = dict_sport_info[sport_name]
			else:
				dict_leagues_ready = {}			
			count_league = 1			
			for league_name_url, league_url in dict_leagues_tornaments.items():
				print("***", league_name_url,"***", " "*(50-len(league_name_url)), count_league, "/" ,len(dict_leagues_tornaments))
				wait_update_page(driver, league_url, "container__heading")
				count_league += 1
				pin_activate = check_pin(driver) # CHECK PIN ACTIVE.
				if pin_activate:
					league_info = get_league_data(driver, league_name_url, sport_id)
					sport_leag_countr_name = sport_name +"_"+ league_info['league_country'] +'_'+ league_info['league_name']
					print(sport_leag_countr_name, end = '')
					###################################################################
					#			SECTION CHECK LEAGUE SAVED PREVIUSLY				  #
					###################################################################
					if sport_leag_countr_name in list(dict_leagues_ready.keys()):
						enable_save = False
						print(" "*(60-len(sport_leag_countr_name))," READY")							
						league_id = dict_leagues_ready[sport_leag_countr_name]['league_id']
						# league_info['league_id'] = league_id						
					else:
						enable_save = True
						print(" "*(60-len(sport_leag_countr_name)), " NEW LEAGUE")
						league_id = league_info['league_id']
						if database_enable:							
							save_league_info(league_info) # UNCOMENT

					print(" "*30, "League_id: ", league_id)
					###################################################################
					#			SECTION CHECK SEASON SAVED PREVIUSLY				  #
					###################################################################
					list_seasons = get_seasons(league_id, league_info['season_name'])
					# list_seasons = [] # UNCOMENT
					print("list_seasons: ", list_seasons)
					
					if len(list_seasons) == 0:
						print(" "*30, "SAVE NEW SEASON", league_info['season_id'])
						if database_enable:
							save_season_database(league_info) # UNCOMENT
					if enable_save:
						dict_leagues_ready[sport_leag_countr_name] = {'league_name':league_info['league_name'] , 'url':league_url,\
															 'league_id':league_id, 'season_id':league_info['season_id']}

					print("league info to save in file json: ")
					print(dict_leagues_ready[sport_leag_countr_name])

					# GET SECTIONS LINKS
					dict_sections_links = get_sections_links(driver)
					for section, url_section in dict_sections_links.items():						
						dict_leagues_ready[sport_leag_countr_name][section] = url_section

				# SAVE JSON FILE WITH THE INFORMATION RELATED TO EACH LEAGUE
				if enable_save:
					dict_sport_info[sport_name] = dict_leagues_ready
				save_check_point('check_points/leagues_info.json', dict_sport_info)
				# stop_validate()

def initial_settings_m2(driver):

	# GET SPORTS AND SPORTS LINKS
	if not os.path.isfile('check_points/sports_url_m1.json'):
		driver.get('https://www.flashscore.com')
		dict_sports = get_sports_links(driver)
		save_check_point('check_points/sports_url_m2.json', dict_sports)

	# BUILD CONFIG_M2
	if not os.path.isfile('check_points/CONFIG_M2.json'):
		dict_sports = load_json('check_points/sports_url_m2.json')
		dict_sports
		dict_config_m2 = {}
		for sport in dict_sports.keys():
			dict_config_m2[sport] = False
		save_check_point('check_points/CONFIG_M2.json', dict_config_m2)

CONFIG = load_json('check_points/CONFIG.json')
database_enable = CONFIG['DATA_BASE']
if database_enable:
	con = getdb()

# if __name__ == "__main__":  	
# 	driver = launch_navigator('https://www.flashscore.com', database_enable)
# 	login(driver, email_= "jignacio@jweglobal.com", password_ = "Caracas5050@\n")
# 	initial_settings_m2(driver)
# 	main_m2(driver, flag_news = False)
# 	if database_enable:
# 		con.close()
# 	driver.quit()