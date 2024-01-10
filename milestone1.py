from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from common_functions import *
# from main import database_enable
# from common_functions import utc_time_naive
from data_base import *

def get_list_recent_news(driver, max_older_news, last_index, last_news_saved_sport):	
	print("max_older_news: ", max_older_news)
	print("last_news_saved_sport: ", last_news_saved_sport)
	global count_match, count_recent_news, more_recent_news
	count = 0	
	wait = WebDriverWait(driver, 10)
	#############################################################
	# 				FIND CONTAINER BLOCK OF EACH NEWS 			#
	#############################################################
	webdriver.ActionChains(driver).send_keys(Keys.END).perform()
	xpath_expression = '//div[@class="fsNewsSection fsNewsSection__mostRecent fsNewsSection__noTopped"]/a'
	container_news = driver.find_elements(By.XPATH, xpath_expression)
	dict_upate_news = {}
	count_match, count_recent_news, more_recent_news = 0, 0, []

	# LOOP OVER ALL NEWS FOUND SO FAR.
	for current_index, block in enumerate(container_news[last_index:]):
		# FIND NECESSARY FIELDS 
		image = wait.until(EC.element_to_be_clickable((By.XPATH, './/figure/picture/img')))
		news_link = block.get_attribute('href')
		news_date = block.find_element(By.XPATH, './/span[@data-testid="wcl-newsMetaInfo-date"]').text		
		news_timestamp = process_date(news_date)
		title = block.find_element(By.XPATH, './/div[@role="heading"]').text		
		image = image.get_attribute('src')		
		# image_url = block.find_element(By.XPATH, './/figure/picture/source').get_attribute('srcset').split(', ')[0]
		# image_url = re.sub(r'\s+\d+\w','', image_url)
		# if utc_time_naive - news_timestamp <timedelta(days=max_older_news):
		print("news_date: ", news_date, "#", news_timestamp,"#", utc_time_naive - news_timestamp)
		if utc_time_naive - news_timestamp < timedelta(days=max_older_news):
			print("NEWS TIME: ", news_timestamp)
			# CHECK IF IS A NEW NEWS AND IF IS NOT CONTAINED IN THE LAST NEWS LIST.
			enable_save_new = check_enable_add_news(title, news_timestamp, max_older_news, last_news_saved_sport)
			if enable_save_new:
				# Verificar base de datos
				print("--", end = '')
				image_path_small = random_name(folder = 'images/news/small_images', termination = '.avif')
				# save_image(driver, image_url, image_path_small)
				image_name_file = image_path_small.split('/')[-1]
				dict_current_news = {'title':title, 'published':news_date, 'image':image_name_file, 'news_link':news_link}				
				dict_upate_news[current_index] = dict_current_news
				print("New len")
				print(len(dict_upate_news))
			else:
				print("Duplicate news: ")
				print(len(dict_upate_news))
		else:
			print("Don't added ")
		print("#"*50, '\n')
	last_news_list = more_recent_news + last_news_saved_sport
	last_news_saved_sport = last_news_list[0:5]	
	print("NEW LIST: ", last_news_saved_sport)
	last_index = last_index + current_index
	return dict_upate_news, last_index, last_news_saved_sport

def check_enable_add_news(title, date_utc, max_older_news, last_news_saved_sport):
	global count_match, count_recent_news, more_recent_news
	enable_save_new = False
	if utc_time_naive - date_utc < timedelta(days=max_older_news):
		if len(last_news_saved_sport)!= 0 and count_match < 3:
			if title in last_news_saved_sport:
				enable_save_new = False
				count_match += 1
			else:
				enable_save_new = True
				if count_recent_news < 5:                
					more_recent_news.append(title)						
					count_recent_news += 1						
		if len(last_news_saved_sport) == 0:
			enable_save_new = True
			if count_recent_news < 5:
				more_recent_news.append(title)					
				count_recent_news += 1
	return enable_save_new

def get_list_recent_news_v2(driver, sport, max_older_news):	
	more_recent_news = []
	count = 0
	print("Case previous list: ", previous_list)
	wait = WebDriverWait(driver, 10)
	webdriver.ActionChains(driver).send_keys(Keys.END).perform()
	xpath_expression = '//div[@class="fsNewsSection fsNewsSection__mostRecent fsNewsSection__noTopped"]/a'
	container_news = driver.find_elements(By.XPATH, xpath_expression)
	list_upate_news = []
	for i, block in enumerate(container_news):
		news_link = block.get_attribute('href')
		news_date = block.find_element(By.CLASS_NAME, '_newsMeta_gh8ui_5').text
		date_utc = process_date(news_date)
		title = block.find_element(By.XPATH, './/div[@role="heading"]').text
		image = wait.until(EC.element_to_be_clickable((By.XPATH, './/figure/picture/img')))
		image = image.get_attribute('src')
		print('*', end ='')		
		####### BLOCK TO AVOID DUPLICATES NEWS #######
	
		if enable_save_new:
			# Verificar base de datos
			print("--", end = '')
			image_path_small = random_name(folder = 'images/news/small_images', termination = '.avif')
			# save_image(driver, image_url, image_path_small)
			image_name_file = image_path_small.split('/')[-1]
			dict_current_news = {'title':title, 'published':date_utc, 'image':image_name_file, 'news_link':news_link}
			list_upate_news.append(dict_current_news)
		else:
			print("Duplicate news: ")
			print("Title: ", title)
		enable_save_new = False
	last_news_list = more_recent_news + last_news_list
	last_news_saved[sport] = last_news_list[0:5]
	save_check_point('check_points/last_saved_news.json', last_news_saved)
	
	return list_upate_news

# def check_process_news(driver, sport, conf_enable_news['MAX_OLDER_DATE_ALLOWED'])

def click_show_more_news(driver, max_older_news, max_click_more = 5):
	wait = WebDriverWait(driver, 5)

	# FIND THE BUTTON SHOW MORE NEWS
	showmore = driver.find_elements(By.CLASS_NAME, 'showMore.showMore--fsNews')
	if len(showmore)!= 0:
		click_more = True
	else:
		click_more = False

	# LOAD THE CURRENT BLOCKS OF NEWS
	xpath_expression = '//div[@class="fsNewsSection fsNewsSection__mostRecent fsNewsSection__noTopped"]/a'
	container_news = driver.find_elements(By.XPATH, xpath_expression)
	current_len = len(container_news)

	# CHECK THE DATE OF THE LAST NEWS FOUND 
	news_date = container_news[-1].find_element(By.XPATH, '//div[@data-testid="wcl-newsMetaGroup"]').text	
	date_utc = process_date(news_date)
	click_count = 0
	while click_count < max_click_more and click_more and utc_time_naive - date_utc < timedelta(days=max_older_news):
		# CLICK ON MORE NEWS 
		print("MORE_NEWS: ", click_count, end ='')
		showmore = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'showMore.showMore--fsNews')))
		showmore.click()
		new_len = current_len

		# WAIT UNTIL LOAD ALL THE NEWS
		while current_len == new_len:
			time.sleep(0.8)
			new_len = len(driver.find_elements(By.XPATH, xpath_expression))
		time.sleep(1)

		# MOVE TO THE LAST PART OF THE PAGE
		webdriver.ActionChains(driver).send_keys(Keys.END).perform()
		webdriver.ActionChains(driver).send_keys(Keys.PAGE_UP).perform()

		# VERIFY IF STILL APPEAR SHOW MORE NEWS BUTTON
		showmore = driver.find_elements(By.CLASS_NAME, 'showMore.showMore--fsNews')
		if len(showmore)== 0:
			click_more = False
		container_news = driver.find_elements(By.XPATH, xpath_expression)
		# news_date = container_news[-1].find_element(By.CLASS_NAME, '_newsMeta_gh8ui_5').text
		news_date = container_news[-1].find_element(By.XPATH, '//div[@data-testid="wcl-newsMetaGroup"]').text
		print(news_date)
		date_utc = process_date(news_date)
		click_count += 1
	print("Total news found: ", len(container_news))
	return container_news

def get_news_info_v2(driver, dict_news):	
	wait = WebDriverWait(driver, 10)
	image = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="imageContainer__element"]/figure/picture/img')))
	image_url = image.get_attribute('src')
	articlebody = driver.find_element(By.CLASS_NAME, 'fsNewsArticle__content')
	summary = articlebody.find_element(By.XPATH, './/div[@class="fsNewsArticle__perex"]')
	body_html = articlebody.get_attribute('outerHTML')
	body_html = body_html.replace(str(summary.get_attribute('ourterHTML')), '')
	# image_path = random_name(folder = 'images/news/full_images')
	image_path = 'images/news/full_images/' + dict_news['image'].replace('.avif','.png')
	save_image(driver, image_url, image_path)
	mentions = get_mentions(driver)
	dict_news['news_id']= random_id()
	dict_news['news_summary'] = summary.text
	dict_news['news_content'] = body_html
	dict_news['image'] = dict_news['image'].replace('.avif','.png')
	dict_news['news_tags'] = mentions
	
	# dict_max_len = {'news_id':40, 'title':400, 'news_summary':8196, 'news_content':16392, 'news_tags':255}
	# for field_name, max_len in dict_max_len.items():
	# 	if len(str(dict_news[field_name])) > max_len:
	# 		print(field_name, "Exced max len: ", max_len,'/',len(str(dict_news[field_name])))
	# for key, field in dict_news.items():
	# 	print(key, len(str(field)), end='--')
	# dict_news = {'news_id':random_id(), 'news_summary':summary.text,
	# 			 'news_content':body_html[0:16392], 'image':image_path,
	# 			'published':date,'news_tags': mentions}
	return dict_news

def extract_news_info(driver):

	news_files = os.listdir('check_points/news/')
	file_paths = [os.path.join('check_points/news/', file) for file in news_files]

	continue_process = False
	for file_path in file_paths:		
		print("file_path: ", file_path)
		input_dict = load_check_point(file_path)
		for index, current_dict in input_dict.items():
			print("-", index, '/',len(input_dict), end= ' ')
			current_url = current_dict['news_link']
			wait_load_detailed_news(driver, current_url)
			dict_news = get_news_info_v2(driver, current_dict)
			dict_news['published'] = process_date(dict_news['published'])
			if database_enable:				
				# try:
				print("Insert news in db")
				save_news_database(dict_news)		
			
			
		os.remove(file_path)

def main_extract_news(driver, list_sports, MAX_OLDER_DATE_ALLOWED = 31):
	# dict_check_point = {} #check_previous_execution(file_path = 'check_points/check_point_m1_news.json')
	global_check_point = load_check_point('check_points/global_check_point.json')
	# conf_enable_news = check_previous_execution(file_path = 'check_points/CONFIG_M1.json')
	dict_url_news = load_json('check_points/sports_url_m1.json')
	last_news_saved = load_check_point('check_points/last_saved_news.json')
	check_point_loaded = False
	enable_start = False
	#############################################################
	# 				MAIN LOOP OVER LIST SPORTS 					#
	#############################################################
	for sport_name in list_sports:
		news_url = dict_url_news[sport_name]	
		# 	TITLE SECTION PRINT
		line_sport = "#" + " "*(50 - int(len(sport_name)/2)) + sport_name + " "*(50 - int(len(sport_name)/2)) + "#"
		print("#"*len(line_sport))
		print(line_sport)
		print("#"*len(line_sport))

		#############################################################
		#	SECTION TO LOAD CHECK POINT FROM LAST RUN 				#
		#############################################################
		# if not check_point_loaded:
		# 	if 'M1' in global_check_point.keys():			
		# 		sport_point = global_check_point['sport']
		# 		file_point = global_check_point['sport']['files']
		# 		extrac_point  = global_check_point['sport']['extract']
		# 	else:
		# 		global_check_point["M1"] = {'sport': sport_point, 'files':False}
		# 		sport_point = sport_name
		# 		file_point = False
		# 		extrac_point = 0
		# 	check_point_loaded = True
		# else:
		# 	sport_point = sport_name
		# 	file_point = False
		#############################################################
		# 				ENABLE CHECK POINT 		 					#
		#############################################################
		# if sport_name == sport_point:
		enable_start = True

		if enable_start:
			# WAIT UNTIL LOAD PAGE
			print(news_url)
			wait_update_page(driver, news_url, "section__mainTitle")
			file_point = False
			if not(file_point):
				####################### GET LAST NEWS SAVED #######################		
				if sport_name in list(last_news_saved.keys()):
					last_news_saved_sport = last_news_saved[sport_name]
				else:
					last_news_saved_sport = []

				last_index = 0 
				click_more_count = 0
				################ LIST OF CONTAINERS NEWS #################
				xpath_expression = '//div[@class="fsNewsSection fsNewsSection__mostRecent fsNewsSection__noTopped"]/a'
				container_news = driver.find_elements(By.XPATH, xpath_expression)
				while last_index < len(container_news):
					start_index = last_index

					list_upate_news, last_index, last_news_saved_sport = get_list_recent_news(driver, MAX_OLDER_DATE_ALLOWED,\
												 							last_index, last_news_saved_sport)
					print("list_upate_news: ", len(list_upate_news))
					if len(list_upate_news)!=0:
						save_check_point('check_points/news/{}_{}.json'.format(start_index, last_index), list_upate_news)					
						# container_news = click_show_more_news(driver, MAX_OLDER_DATE_ALLOWED, max_click_more = 5)
						last_news_saved[sport_name] = last_news_saved_sport
					last_index += 1
				# global_check_point["M1"] = {'sport': sport_point, 'files':True}
				save_check_point('check_points/last_saved_news.json', last_news_saved)
			# save_check_point('check_points/global_check_point.json', global_check_point)
			#################### SECTION PROCESS NEWS #########################
			extract_news_info(driver)

def initial_settings_m1(driver):
	# GET SPORTS AND SPORTS LINKS
	if not os.path.isfile('check_points/sports_url_m1.json'):
		driver.get('https://www.flashscore.com/news/football/')
		dict_url_news_m1 = get_sports_links_news(driver)
		save_check_point('check_points/sports_url_m1.json', dict_url_news_m1)

	# BUILD CONFIG_M1
	if not os.path.isfile('check_points/CONFIG_M1.json'):
		dict_enable_news = {'SPORTS':{}}
		dict_url_news_m1 = load_json('check_points/sports_url_m1.json')
		for sport in dict_url_news_m1.keys():
			dict_enable_news['SPORTS'][sport] = True
		dict_enable_news['MAX_OLDER_DATE_ALLOWED'] = 31
		save_check_point('check_points/CONFIG_M1.json', dict_enable_news)

CONFIG = load_json('check_points/CONFIG.json')
database_enable = CONFIG['DATA_BASE']

# if __name__ == "__main__":	
# 	driver = launch_navigator('https://www.flashscore.com', database_enable)
# 	initial_settings_m1(driver)
# 	login(driver, email_= "jignacio@jweglobal.com", password_ = "Caracas5050@\n")	
# 	main_extract_news(driver)