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
from milestone6 import *


def get_live_result(row):
# 	match_date = row.find_element(By.CLASS_NAME, 'event__time').text	
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
	match_id = random_id()
	result_dict = {'match_id':match_id,'match_date':'','start_time':'', 'end_time':'',\
						'name':home_participant + '-' + away_participant,'home':home_participant,'visitor':away_participant,\
						'home_result':home_result,  'visitor_result':away_result, 'place':''}
	return result_dict

def extract_info_results(driver, results_block, section_name):
	global count_sub_section, event_number, current_id_section, dict_rounds, new_section_name	
	
	for processed_index, row in enumerate(results_block):		
		try:
			# SECTION MAIN TITLE, ONLY FIND TITLE, IT IS NOT USED
			HTML = row.get_attribute('outerHTML')
			title_section = re.findall(r'icon--flag.event__title fl_\d+', HTML)[0].replace(' ', '.')
		except:
			try:
				# SECTION TO FIND MATCH INFO, EXTRACT DETAILS
				result = get_result(row)
				if round_enable:					
					dict_rounds[current_round_name][event_number] = result
					event_number += 1
			except:
				# SECTION TO FIND ROUND NAME.
				try:
					round_name = row.find_element(By.CLASS_NAME, 'event__title--name').text.replace(' ','_').replace('/','*-*')

				except:
					round_name = get_unique_key(row.text, dict_rounds.keys())
				# SECTION TO CHECK ROUND SAVED PREVIOUSLY
				round_name = '_'.join(round_name.split())
				print("round_name: ", round_name)
				if round_name in list_rounds:
					round_enable = False
				else:
					print("New round: ", round_name)
					round_enable = True				
				# IF round dictionary IS FILLED PROCEED TO SAVE DICT FOR PROCESSING IN THE NEXT STAGE
				if len (dict_rounds)!= 0 and len(dict_rounds[current_round_name]) != 0:					
					list_rounds.append(current_round_name)					
					file_name = 'check_points/{}/{}/{}.json'.format(section_name, country_league, current_round_name)
					folder_name = 'check_points/{}/{}/'.format(section_name, country_league)					
					print(file_name)
					if not os.path.exists(folder_name):
						os.mkdir(folder_name)
					save_check_point(file_name, dict_rounds[current_round_name])
					webdriver.ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
				# RESTAR NEW DICTIONARY AND UPDATE CURRENT NAMES
				current_round_name = round_name
				dict_rounds[current_round_name] = {}
				count_sub_section += 1
				event_number = 0
	print(round_enable)
	return start_index + processed_index, round_enable

def give_click_on_live(driver):
	wait = WebDriverWait(driver, 10)
	xpath_expression = '//div[@title="Click for match detail!"]'
	current_tab = driver.find_elements(By.XPATH, xpath_expression)
	livebutton = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="filters__tab" and contains(.,"LIVE Games")]')))	
	livebutton.click()

	if len(current_tab) == 0:
		current_tab = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, class_name)))
	else:
		element_updated = wait.until(EC.staleness_of(current_tab[0]))

def get_live_match(driver, sport_name='FOOTBALL'):
	if sport_name=='FOOTBALL':
		sport_name = 'soccer'
	else:
		sport_name = sport_name.lower()
	
	rows = driver.find_elements(By.XPATH, '//div[@class="sportName {}"]/div'.format(sport_name))	
	enable_load = False
	list_match = []
	for index, row in enumerate(rows):
		try:			
			title = row.find_element(By.XPATH, './/div[@class="event__titleBox"]')
			enable_load = False
			league_country = row.find_element(By.XPATH, './/span[@class="event__title--type"]').text 
			league_name= row.find_element(By.XPATH, './/span[@class="event__title--name"]').text
			HTML = row.get_attribute('outerHTML')
			if 'pin--active"' in HTML:
				enable_load = True
		except:
			try:				
				if enable_load:
					game_results = get_live_result(row)
					HTML = row.get_attribute('outerHTML')
					game_results['league_name'] = league_name
					game_results['league_country'] = league_country
					list_match.append(game_results)
			except:
				pass
	return list_match


def live_games(driver, list_sports):
	dict_sports_url = load_json('check_points/sports_url_m2.json')
	current_date = datetime.now().date()#.strftime('%H:%M:%S')
	print("Current_date: ", current_date, '\n')
	# date = dt_object.date()
	# time = dt_object.time()

	#############################################################
	# 				MAIN LOOP OVER LIST SPORTS 					#
	#############################################################
	for sport_name in list_sports:

		print_section("LIVE SECTION: " + sport_name, space_ = 50)

		#################################################
		# LOAD SPORT LINK
		wait_update_page(driver, dict_sports_url[sport_name], "container__heading")		

		###################### LIVE SECTION ############################################
		# CLICK ON LIVE BUTTON		
		give_click_on_live(driver)

		###############################################################################
		count = 0
		while count < 1000:
			list_live_match = get_live_match(driver, sport_name=sport_name)		
			print(len(list_live_match))
			for match_info in list_live_match:
				print(match_info)
				# get match id
				match_id = 'dsada26263'
				match_id = get_match_id(match_info['league_country'],\
									 match_info['league_name'], current_date, match_info['name'])

				print("Match id: ", match_id)

				stop_validate()
				match_id = 'ywse92791'
				# update_data base
				# Get score_id home and score_id visitor
				#{match_detail_id_visitor: False, match_detail_id_home:True}
				dict_match_detail_id = get_math_details_ids(match_id) # UNCOMENT
				print("dict_match_detail_id: ", dict_match_detail_id)
				# dict_match_detail_id = {'KAFHD3536':True, 'dkdfkd': False}

				for match_detail_id, home_flag in dict_match_detail_id.items():
					if home_flag:
						# Update home score
						params = {'match_detail_id': match_detail_id,
								'points': match_info['home_result'] }
						update_score(params)# UNCOMENT
					else:
						# Update visitor score
						params = {'match_detail_id': match_detail_id,
								'points': match_info['visitor_result'] }
						update_score(params)# UNCOMENT
			print("Updated")
			count += 1
			time.sleep(15)

		###################### LOOP OVER LIVE MATCHS #######################	

