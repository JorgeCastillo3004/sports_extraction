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

def get_ligues_data(driver):
	block_ligue_team = driver.find_element(By.CLASS_NAME, 'container__heading')
	sport = block_ligue_team.find_element(By.XPATH, './/h2[@class= "breadcrumb"]/a[1]').text
	league_country = block_ligue_team.find_element(By.XPATH, './/h2[@class= "breadcrumb"]/a[2]').text
	league_name = block_ligue_team.find_element(By.CLASS_NAME,'heading__title').text
	season_name = block_ligue_team.find_element(By.CLASS_NAME, 'heading__info').text
	image_url = block_ligue_team.find_element(By.XPATH, './/div[@class= "heading"]/img').get_attribute('src')
	image_path = random_name(folder = 'images/logos/')
	save_image(driver, image_url, image_path)
	image_path = image_path.replace('images/logos/','')
	league_id = random_id()
	season_id = random_id()
	ligue_tornamen = {"league_id":league_id,"season_id":season_id, 'sport':sport, 'league_country': league_country,
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
	ligues_info = wait.until(EC.visibility_of_element_located((By.XPATH, xpath_expression)))
	dict_liguies = {}
	if not "To select your leagues " in ligues_info.text:
		# ligues = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@id="my-leagues-list"]/div/div/a')))        
		ligues = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@id="my-leagues-list"]/div/div/a')))
		print(len(ligues))        
		# ligues = driver.find_elements(By.XPATH, '//div[@id="my-leagues-list"]/div/div/a')
		# print(len(ligues))
		gender = ''
		for ligue in ligues:
			if '#man' in ligue.get_attribute('outerHTML'):
				gender = "_man"
			if '#woman' in ligue.get_attribute('outerHTML'):
				gender = "_woman"
			dict_liguies['_'.join(ligue.text.split())+gender] = ligue.get_attribute('href')			
	return dict_liguies

def get_result(row):
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
	link_id = re.findall(r'id="[a-z]_\d_(.+?)\"', html_block)[0]
	url_details = "https://www.flashscore.com/match/{}/#/match-summary/match-summary".format(link_id)
	result_dict = {'date':date, 'home_participant':home_participant,'away_participant':away_participant,\
				   'home_result':home_result,  'away_result':away_result, 'link_details':url_details}	
	return result_dict

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

def get_unique_key(id_section_new, list_keys):
	id_section_new = id_section_new.replace(' ','_').replace('/','*-*')
	# Sections with the same name.
	if id_section_new in list_keys:
		id_section_base = id_section_new
		count_sub_rounds = 1
		id_section_new = id_section_base +'_' +str(count_sub_rounds)
		while id_section_new in list_keys:
			count_sub_rounds += 1
			id_section_new = id_section_base +'_' +str(count_sub_rounds)
	return id_section_new

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
					stop_validate()
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

def extract_info_results(driver, start_index, results_block, section_name):
	global count_sub_section, event_number, current_section_name, current_id_section, dict_rounds, new_section_name
	for processed_index, row in enumerate(results_block[start_index:]):	
		print(processed_index, end ='-')
		try:
			HTML = row.get_attribute('outerHTML')
			class_name_section = re.findall(r'icon--flag.event__title fl_\d+', HTML)[0].replace(' ', '.')
			new_section_name = row.find_element(By.CLASS_NAME, class_name_section).text
			new_section_name = new_section_name.replace(' ', '_').replace('\n', '_').replace('/','*-*')
			os.mkdir("check_points/{}/{}".format(section_name, new_section_name))			
		except:
			try:
				result = get_result(row)
				dict_rounds[current_id_section][event_number] = result
				event_number += 1				
			except:
				# Get Rounds block
				try:
					# Only get section name or ROUND name
					id_section_new = row.find_element(By.CLASS_NAME, 'event__title--name').text.replace(' ','_').replace('/','*-*')
					#id_section = row.find_element(By.CLASS_NAME, 'event__round event__round--static').text.replace(' ','_')
				except:
					# Else get all available text					
					id_section_new = get_unique_key(row.text, dict_rounds.keys())					
				if count_sub_section != 0:
					# save current dict
					# stop_validate()
					file_name = 'check_points/{}/{}/round_{}.json'.format(section_name, current_section_name, current_id_section)					
					save_check_point(file_name, dict_rounds[current_id_section])
					webdriver.ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
				
				current_id_section = id_section_new
				current_section_name = new_section_name
				dict_rounds[id_section_new] = {}
				count_sub_section += 1
				event_number = 0
	return start_index + processed_index

def click_show_more_rounds(driver, current_results, section_name):
	wait = WebDriverWait(driver, 10)
	webdriver.ActionChains(driver).send_keys(Keys.END).perform()
	webdriver.ActionChains(driver).send_keys(Keys.PAGE_UP).perform()
	webdriver.ActionChains(driver).send_keys(Keys.PAGE_UP).perform()
	time.sleep(1.5)
	print("Action click more rounds: ---")
	show_more_list = driver.find_elements(By.CLASS_NAME, 'event__more.event__more--static')
	old_len = len(current_results)
	xpath_expression = '//div[@class="leagues--static event--leagues {}"]/div/div'.format(section_name)
	if len(show_more_list) != 0:
		show_more = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'event__more.event__more--static')))
		time.sleep(0.3)
		show_more.click()
		# Wait until upload page
		new_len = old_len 
		while new_len == old_len:
			time.sleep(0.3)			
			new_len = len(driver.find_elements(By.XPATH, xpath_expression))
		# wait.until(EC.staleness_of(current_results[1]))
		return True
	else:
		return False

def navigate_through_rounds(driver, section_name = 'results'):
	global count_sub_section, event_number, dict_rounds
	last_procesed_index = 0	
	xpath_expression = '//div[@class="leagues--static event--leagues {}"]/div/div'.format(section_name)
	print(xpath_expression)
	current_results = driver.find_elements(By.XPATH, xpath_expression)

	print("Total current results: ", len(current_results))
	count_sub_section = 0
	event_number = 0
	dict_rounds = {}
	
	while last_procesed_index < len(current_results):
		print("last_procesed_index: ", last_procesed_index)

		last_procesed_index = extract_info_results(driver, last_procesed_index, current_results, section_name)
		# more_rounds_loaded = click_show_more_rounds(driver, current_results, section_name) # UNCOMENT ## URGENT DELETE
		more_rounds_loaded = False ### URGENT DELETE
		print("Len list results not updated: ", len(current_results))
		if more_rounds_loaded:
			# Update of list of current results
			current_results = driver.find_elements(By.XPATH, xpath_expression)
		print("Len list results updated: ", len(current_results))
		last_procesed_index += 1

def get_match_info(driver, event_info):
	# Extract details about matchs
	match_info_elements = driver.find_elements(By.XPATH, '//div[@class="matchInfoData"]/div')
	for element in match_info_elements:        
		field_name = element.find_element(By.CLASS_NAME, 'matchInfoItem__name').text
		field_value = element.find_element(By.CLASS_NAME, 'matchInfoItem__value').text
		event_info[field_name] = field_value
	return event_info

def get_statistics_game(driver):
	wait = WebDriverWait(driver, 10)
	button_stats = driver.find_element(By.XPATH, '//button[contains(.,"Stats")]')
	button_stats.click()	
	# statistics = driver.find_elements(By.XPATH, '//div[@data-testid="wcl-statistics"]')
	statistics = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@data-testid="wcl-statistics"]')))
	statistics_info = {}
	for indicator in statistics:
		stat_name = indicator.find_element(By.CLASS_NAME, '_category_rbkfg_5').text
		stat_home = indicator.find_element(By.CLASS_NAME, '_value_1efsh_5._homeValue_1efsh_10').text
		stat_away = indicator.find_element(By.CLASS_NAME, '_value_1efsh_5._awayValue_1efsh_14').text
		statistics_info[stat_name] = {'home' : stat_home, 'away' : stat_away}

	return statistics_info

def wait_load_details(driver, url_details):
	wait = WebDriverWait(driver, 10)
	block_info = driver.find_elements(By.XPATH,'//div[@class="matchInfoData"]')
	driver.get(url_details)
	if len(block_info) == 0:
		element = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@class="matchInfoData"]')))
	else:
		wait.until(EC.staleness_of(block_info[0]))

def get_sections_links(driver):
	list_links = driver.find_elements(By.XPATH, '//div[@class="tabs__group"]/a')

	dict_links = {}
	for link in list_links[1:]:    
		url_termination = link.get_attribute('href')
		dict_links[url_termination.split('/')[-2]] = url_termination
	return dict_links

def buil_dict_map_values(driver):
	cell_names = driver.find_elements(By.XPATH,'//div[@class="ui-table__header"]/div')
	dict_map_cell = {}
	for index, cell_name in enumerate(cell_names[2:]):
		cell_name = cell_name.get_attribute('title').replace(' ', '_')    
		dict_map_cell[index] = cell_name
	return dict_map_cell    

def get_teams_info(driver):
	wait = WebDriverWait(driver, 10)	
	# teams_availables = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'ui-table__row')))
	xpath_expression = '//*[@id="tournament-table-tabs-and-content"]/div/div/div/div/div/div/span'
	all_cells = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath_expression)))
	print("Total cells: ", len(all_cells))
	dict_map_cell = buil_dict_map_values(driver)
	teams_availables = driver.find_elements(By.CLASS_NAME, 'ui-table__row')	
	# time.sleep(5)
	dict_teams_availables = {}

	for team in teams_availables:    
		team_name = team.find_element(By.XPATH, './/div[@class="tableCellParticipant"]').text
		team_position = team.find_element(By.XPATH, './/div[@class="tableCellRank"]').text
		team_position = int(re.search(r'\d+',team_position).group(0))
		games_hist = team.find_element(By.XPATH, './/div[@class="table__cell table__cell--form"]').text.split('\n')
		
		team_url = team.find_element(By.XPATH, './/a[@class="tableCellParticipant__image"]')
		team_statistic = team.find_elements(By.XPATH, './/span')    
		dict_statistic = {}
		print("Team: ", team_name)
		for index, cell_value in enumerate(team_statistic):
			dict_statistic[dict_map_cell[index]] = cell_value.text
		
		dict_teams_availables[team_name] = {'team_url': team_url.get_attribute('href'), 'statistics':dict_statistic,\
										   'position':team_position, 'last_results': games_hist}
	return dict_teams_availables

def get_complete_match_info(driver, sport, league_id, season_id, section = 'results'):
    
	base_dir = 'check_points/{}/'.format(section)
	list_folders = os.listdir(base_dir)

	for folder in list_folders:
		folder_path = os.path.join(base_dir, folder)
		print(folder_path)
		list_files = os.listdir(folder_path)
		print(list_files,'\n')
		for file in list_files:
			file_path = os.path.join(folder_path, file)
			print(file_path)   
			round_info = load_json(file_path)        
			for event_index, event_info in round_info.items():

				url_details = event_info['link_details']
				wait_load_details(driver, url_details)
				event_info = get_match_info(driver, event_info)
				
				event_info['statistic_info'] = get_statistics_game(driver)

				print(event_info, '\n')
				print("Save in data base match info")
				if database_enable:
					print("save in db")
				stop_validate()

		print("folder_path to delete: ", folder_path)
		shutil.rmtree(folder_path)
		stop_validate()

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

def navigate_through_teams(driver, sport_id, league_id, tournament_id, season_id, section = 'standings'):
	base_dir = 'check_points/{}/'.format(section)
	list_files = os.listdir(base_dir)
	
	for file_name in list_files:
		file_name = os.path.join(base_dir, file_name)
		dict_teams = load_check_point(file_name)
		count = 0
		for team_name, team_info in dict_teams.items():

			print("Save team statistics in database")
			
			wait_update_page(driver, team_info['team_url'], 'heading')

			dict_team = get_teams_data(driver, sport_id, league_id, season_id, team_info)			
			dict_team['tournament_id'] = tournament_id
			print("Save in database teams info")
			if database_enable:				
				save_team_info(dict_team)
				dict_team['player_meta'] = ''
				save_league_team_entity(dict_team)

			squad_button = driver.find_element(By.CLASS_NAME, 'tabs__tab.squad')
			squad_url = squad_button.get_attribute('href')
			wait_update_page(driver, squad_url, 'heading')
			dict_squad = get_squad_dict(driver)
			navigate_through_players(driver, dict_squad)
			count += 1
			if count == 3:
				break ### URGENT DELETE #######
		# Remove processed file
		os.remove(file_name)
#####################################################################

def main_m2(driver, flag_news = False):
	dict_sports = load_json('check_points/sports_url_m2.json')
	conf_enable_sport = check_previous_execution(file_path = 'check_points/CONFIG_M2.json')
	
	dict_with_issues = {}
	for sport, sport_info in conf_enable_sport.items():
		if sport_info['enable']:
			if database_enable:
				sport_dict = create_sport_dict(sport, sport_info['mode'])
				save_sport_database(sport_dict)

			print("Init: ", sport, dict_sports[sport])
			wait_update_page(driver, dict_sports[sport], "container__heading")
			
			dict_ligues_tornaments = find_ligues_torneos(driver)			

			for ligue_tournament, ligue_tournament_url in dict_ligues_tornaments.items():
					
					step = 'ligue_tournament'						
					print(" "*15, "############ Ligue: ", ligue_tournament_url)
					wait_update_page(driver, ligue_tournament_url, "container__heading")
					step = 'Ligues extraction'

					pin_activate = check_pin(driver)
					if pin_activate:
						print("Extract ligue info: ")
						league_tornamen_info = get_ligues_data(driver)
						dict_tournament = {'tournament_id':random_id(), 'team_country':league_tornamen_info['league_country'],\
						 			'desc_i18n':'','end_date':datetime.now(),'logo':'', 'name_i18n':'', 'season':league_tornamen_info['season_id'],\
						 			 'start_date':datetime.now(), 'tournament_year':2023}
						
						if database_enable:
							save_ligue_info(league_tornamen_info)
							save_season_database(league_tornamen_info)
							save_tournament(dict_tournament)
						print(league_tornamen_info)
						league_id = league_tornamen_info['league_id']
						tournament_id = dict_tournament['tournament_id']
						season_id = league_tornamen_info['season_id']
						
						print("League id: ", league_tornamen_info['league_id'])
						
						# Build dict links standings, fixtures, results
						dict_section_links = get_sections_links(driver)

						get_player_team_info = False
						if get_player_team_info:
							if sport != 'TENNIS':
								wait_update_page(driver, dict_section_links['standings'], "container__heading")
								dict_teams_availables = get_teams_info(driver)							
								league_name = league_tornamen_info['league_name'].replace(' ', '_')
								save_check_point('check_points/standings/{}.json'.format(league_name), dict_teams_availables)
								navigate_through_teams(driver, sport, league_id, tournament_id, season_id, section = 'standings')
						
						# tournament_id = 'aftjcxzeoeftlswi03330'
						# # Loop over teams link and complete information available.#####
						# ###############################################################


						# ###############################################################

						# wait_update_page(driver, dict_section_links['fixtures'], "container__heading")
						# navigate_through_rounds(driver, section_name = 'fixtures')
						# get_complete_match_info(driver, sport, league_id, season_id, section='fixtures')

						# wait_update_page(driver, dict_section_links['results'], "container__heading")
						# navigate_through_rounds(driver, section_name = 'results')

						# get_complete_match_info(driver, sport, league_id, season_id, section='results')

						print("#"*30, '\n'*2)						
						
						if flag_news:
							process_current_news_link(driver, driver.current_url)								
							wait_update_page(current_url)
						######## Block to check section results and fixtures.

						url_news = driver.current_url

def stop_validate():
	user_input = input("Type y to continue s to stop: ")
	if user_input == 'y':
		user_confirmation = True
	if user_input == 's':
		print(stop)

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

if __name__ == "__main__":  	
	driver = launch_navigator('https://www.flashscore.com', database_enable)
	login(driver, email_= "jignacio@jweglobal.com", password_ = "Caracas5050@\n")
	initial_settings_m2(driver)
	main_m2(driver, flag_news = False)
	if database_enable:
		con.close()