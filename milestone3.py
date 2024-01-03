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


def buil_dict_map_values(driver):
	cell_names = driver.find_elements(By.XPATH,'//div[@class="ui-table__header"]/div')
	dict_map_cell = {}
	for index, cell_name in enumerate(cell_names[2:]):
		cell_name = cell_name.get_attribute('title').replace(' ', '_')    
		dict_map_cell[index] = cell_name
	return dict_map_cell    

# def click_main_section(driver):
# 	wait = WebDriverWait(driver, 0.6)
# 	xpath_expression = '//button[@data-testid="wcl-tab"]'

# 	list_buttons = driver.find_elements(By.XPATH, xpath_expression)
# 	for button in list_buttons:
# 		print(button.text, end='')
# 		try:
# 			button.click()        
# 			xpath_expression = '//button[@data-testid="wcl-tab" and contains(.,"{}")]'.format('Standings')        
# 			standing_button = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_expression)))
# 			standing_button.click()
# 			break;
# 		except:
# 			pass    
	# xpath_expression = '//button[@data-testid="wcl-tab" and contains(.,"{}")]'.format(torneo)
	# button_main = driver.find_elements(By.XPATH, xpath_expression)
	# if len(button_main)!=0:
	# 	button_main[0].click()

def get_teams_info_part1(driver):
	wait = WebDriverWait(driver, 10)
	# teams_availables = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'ui-table__row')))
	xpath_expression = '//*[@id="tournament-table-tabs-and-content"]/div/div/div/div/div/div/span'	
	# all_cells = driver.find_elements(By.XPATH, xpath_expression)
	# print("All cells found: ", len(all_cells))
	try:
		all_cells = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath_expression)))	
		dict_map_cell = buil_dict_map_values(driver)
	except:
		print("--")
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
		print("-", team_name, end = ' ')
		for index, cell_value in enumerate(team_statistic):
			dict_statistic[dict_map_cell[index]] = cell_value.text
		
		dict_teams_availables[team_name] = {'team_url': team_url.get_attribute('href'), 'statistics':dict_statistic,\
										   'position':team_position, 'last_results': games_hist}
	return dict_teams_availables

def get_teams_info_part2(driver, sport_id, league_id, season_id, team_info):
	block_ligue_team = driver.find_element(By.CLASS_NAME, 'container__heading')


	sport = block_ligue_team.find_element(By.XPATH, './/h2[@class= "breadcrumb"]/a[1]').text
	team_country = block_ligue_team.find_element(By.XPATH, './/h2[@class= "breadcrumb"]/a[2]').text
	team_name = block_ligue_team.find_element(By.CLASS_NAME,'heading__title').text

	try:
		stadium = block_ligue_team.find_element(By.CLASS_NAME, 'heading__info').text
	except:
		stadium = ''
	image_url = block_ligue_team.find_element(By.XPATH, './/div[@class= "heading"]/img').get_attribute('src')
	image_path = random_name(folder = 'images/logos/')
	save_image(driver, image_url, image_path)
	logo_path = image_path.replace('images/logos/','')
	team_id = random_id()
	instance_id = random_id()	
	meta_dict = str({'statistics':team_info['statistics'], 'last_results':team_info['last_results']})
	team_info = {"team_id":team_id,"team_position":team_info['position'], "team_country":team_country,"team_desc":'', 'team_logo':logo_path,\
			 'team_name': team_name,'sport_id': sport_id, 'league_id':league_id, 'season_id':season_id,\
			 'instance_id':instance_id, 'team_meta':meta_dict, 'stadium':stadium, 'player_meta' :''}
	return team_info

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

			dict_team = get_teams_info_part2(driver, sport_id, league_id, season_id, team_info)			
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

def main_m3(driver):
	sports_dict = load_check_point('check_points/leagues_info.json')
	
	for sport_id, sport_dict in sports_dict.items():
		# dict_teams_db = get_dict_teams(sport_id = 'FOOTBALL') # add return stadium result

		for country_league, country_league_urls in sport_dict.items():
			json_name = 'check_points/leagues_season/{}_{}.json'.format(sport_id, country_league)
			dict_teams_db = {}
			print("#"*30, "DATA FROM DICT ", "#"*30)
			print(country_league_urls)
			if not os.path.isfile(json_name) and 'standings' in list(country_league_urls.keys()):
				wait_update_page(driver, country_league_urls['standings'], "container__heading")
				# click_main_section(driver)
				
				dict_teams_availables = get_teams_info_part1(driver)
				print("Len dict teams_availables: ", len(dict_teams_availables))
				dict_country_league_season = {}
				for team_name, team_info_url in dict_teams_availables.items():
					#league.league_country, league.league_name, team.team_name
					try:
						list_teams_saved = dict_teams_db[country_league.split('_')[0]].keys()
					except:
						list_teams_saved = []

					if team_name.upper() in list_teams_saved:
						print("READY")
						team_id = dict_teams_db[country_league.split('_')[0]]['team_id']					
					else:
						# sport_id, league_id, season_id
						wait_update_page(driver, team_info_url['team_url'], 'heading')
						dict_team = get_teams_info_part2(driver, sport_id, country_league_urls['league_id'],\
															 country_league_urls['season_id'], team_info_url)
						print(" "*30, "New INSERT ")
						print(dict_team.keys())
						print(dict_team,  '\n'*2)
						if database_enable:
							save_team_info(dict_team)
							save_league_team_entity(dict_team)
							
						team_id = dict_team['team_id']
					dict_country_league_season[team_name] = {'team_id':team_id}
				# Save file sport_country_league_season.jso
				print("Len of dict teams: ", len(dict_country_league_season))
				if len(dict_teams_availables) != 0:
					save_check_point(json_name, dict_country_league_season)


CONFIG = load_json('check_points/CONFIG.json')
database_enable = CONFIG['DATA_BASE']
if database_enable:
	con = getdb()

if __name__ == "__main__":  	
	driver = launch_navigator('https://www.flashscore.com', database_enable)
	login(driver, email_= "jignacio@jweglobal.com", password_ = "Caracas5050@\n")	
	main_m3(driver)
	if database_enable:
		con.close()
	driver.quit()