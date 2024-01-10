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




def live_games(driver, list_sports):
	#############################################################
	# 				MAIN LOOP OVER LIST SPORTS 					#
	#############################################################
	for sport_name in list_sports:

		#################################################
		for country_league, legue_info in leagues_info_json[sport_name].items():

			###################### LIVE SECTION #######################
			# CLICK ON LIVE BUTTON
			livebutton = driver.find_element(By.XPATH, '//div[@class="filters__tab" and contains(.,"LIVE Games")]')
			livebutton.click()

			###################### LOOP OVER LIVE MATCHS #######################
			live_matchs = driver.find_elements(By.XPATH, '//div[@title="Click for match detail!"]')

			# Filter elements that contain the desired class
			live_matchs = [element for element in live_matchs if 'liveBet liveBet--animated' in element.get_attribute('outerHTML')]

			print(len(filtered_elements))

			for live_math in live_matchs:
			    
			    live_results = get_result(live_math)
			    
			    print(live_results)
			    print("#"*100)
