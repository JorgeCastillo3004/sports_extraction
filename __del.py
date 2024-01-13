# NOT ROUNDS PRESENT 
# url = 'https://www.flashscore.com/hockey/finland/liiga/fixtures/'
# driver.get(url)

count_sub_section = 0
event_number = 0
section_name = 'fixtures'
xpath_expression = '//div[@class="leagues--static event--leagues {}"]/div/div'.format(section_name)
last_procesed_index = 0
results_block = confirm_results(driver, section_name, max_count = 10)
country_league = 'SPAIN LEAGUE'	
list_rounds_ready = []
start_index = 0

def extract_info_results(driver, start_index, results_block, section_name, country_league, list_rounds_ready):
	

	print(len(results_block))
	 # list to save round name, index_start index_end
	dict_rounds_index = {}
	all_list_results = []
	count = 0
	#########################################################
	#               LOOP OVER ALL MATCH                     #
	#########################################################
	for processed_index, result in enumerate(results_block[start_index:]):
		print(result.text.replace('\n',' '))
		HTML = result.get_attribute('outerHTML')
		if 'event__round event__round--static' in HTML: # TAKE ROUND NAME
			if count == 0:
				list_index = []
				round_name = round_name = get_unique_key(row.text, dict_rounds_index.keys())
				list_index[0] = processed_index + 1
				count = 1
			else:
				list_index[1] = processed_index - 1
				dict_rounds_index[round_name] = list_index            
				count = 0
		if 'Click for match detail!' in HTML: # EXTRACT MATHC INFO
			result = get_result(row)
			all_list_results.append(result)
		else:
			all_list_results.append('')

	#######################################################################
	#  SAVE FILES BY ROUNDS AND ORGANIZE THEM ACCORDING TO THE MATCH      #
	#######################################################################
	if len(dict_rounds_index) != 0:
		for round_name, index_star_end in dict_rounds_index.items():
			if not round_name in list_rounds_ready:
				# CREATE FOLDER AND FILE NAME.
				file_name = 'check_points/{}/{}/{}.json'.format(section_name, country_league, round_name)
				folder_name = 'check_points/{}/{}/'.format(section_name, country_league)		
				if not os.path.exists(folder_name):
					os.mkdir(folder_name)
				# CREATE DICT WITH ALL ENVENTS INFO.
				envent_number = 0
				dict_round = {}
				for index in range(index_star_end[0], index_star_end[1]):
					dict_round[event_number] = all_list_results[index]
					envent_number += 1
				# SAVE ROUND DICT
				save_check_point(file_name, dict_round)
				envent_number = 0
	else:
		event_number = 0
		dict_round = {}
		for index, match_info in enumerate(all_list_results):
			dict_round[index] = match_info

		# CREATE FOLDER AND FILE NAME.
		file_name = 'check_points/{}/{}/{}.json'.format(section_name, country_league, 'UNIQUE')
		folder_name = 'check_points/{}/{}/'.format(section_name, country_league)		
		if not os.path.exists(folder_name):
			os.mkdir(folder_name)
		
		# SAVE ROUND DICT
		round_enable = True
		save_check_point(file_name, dict_round)

	return start_index + processed_index, round_enable