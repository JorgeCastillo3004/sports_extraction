

list_rounds = []
section_name = 'results'
results_block = confirm_results(driver, section_name, max_count = 10)
start_index = 0
count_sub_section = 0
print(len(results_block))
dict_rounds = {}
round_enable = False
for processed_index, row in enumerate(results_block[start_index:]):
	try:
		HTML = row.get_attribute('outerHTML')
		title_section = re.findall(r'icon--flag.event__title fl_\d+', HTML)[0].replace(' ', '.')
	except:
		try:
			result = get_result(row)
			if round_enable:
				dict_rounds[current_round_name][event_number] = result
				event_number += 1
		except:
			try:
				round_name = row.find_element(By.CLASS_NAME, 'event__title--name').text.replace(' ','_').replace('/','*-*')

			except:
				round_name = get_unique_key(row.text, dict_rounds.keys())
			if round_name in list_rounds:
				round_enable = True
			else:
				round_enable = False
			if len(dict_rounds) != 0:
				print("Round name: ", round_name, "Saved")
				list_rounds.append(round_name)
#                 file_name = 'check_points/{}/{}/{}.json'.format(section_name, country_league, current_round_name)
#                 save_check_point(file_name, dict_rounds[current_round_name])
				webdriver.ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
			current_round_name = round_name
			dict_rounds[current_round_name] = {}
			count_sub_section += 1
			event_number = 0            
return round_enable