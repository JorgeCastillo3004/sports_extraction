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

def get_list_recent_news(driver, sport, max_older_news):
	last_news_saved = check_previous_execution(file_path = 'check_points/last_saved_news.json')
	try:
		last_news_list = last_news_saved[sport]
		previous_list = True		
		count_match = 0
		
	except:
		last_news_list = []
		previous_list = False
	
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
		
		# image_url = block.find_element(By.XPATH, './/figure/picture/source').get_attribute('srcset').split(', ')[0]
		# image_url = re.sub(r'\s+\d+\w','', image_url)
		# if utc_time_naive - date_utc <timedelta(days=max_older_news):
		if utc_time_naive - date_utc < timedelta(days=max_older_news):
			if previous_list and count_match < 3:
				if title in last_news_list:
					enable_save_new = False
					count_match += 1					
					# input_user = input("Type any to continue s to stop ")
					# if input_user =='s':
					# 	print(stop)
				else:
					enable_save_new = True
					if count < 5:                
						more_recent_news.append(title)						
						count += 1
					# if count == 5:
					# 	more_recent_news.extend(last_news_list)
						
			if not previous_list:
				enable_save_new = True
				if count < 5:
					last_news_list.append(title)					
					count += 1		
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
	# print("len more_recent_news, last_news_list ", len(more_recent_news), len(last_news_list))
	# print("more_recent_news: ", more_recent_news)
	# print("last_news_list: ", last_news_list)
	last_news_list = more_recent_news + last_news_list
	last_news_saved[sport] = last_news_list[0:5]
	# print("Saving new list of last news by the sport: ", sport)
	# print("last_news_saved: ", last_news_saved)
	save_check_point('check_points/last_saved_news.json', last_news_saved)
	
	return list_upate_news

def get_list_recent_news_v2(driver, sport, max_older_news):
	last_news_saved = check_previous_execution(file_path = 'check_points/last_saved_news.json')
	try:
		last_news_list = last_news_saved[sport]
		previous_list = True		
		count_match = 0
		
	except:
		last_news_list = []
		previous_list = False
	
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

		if utc_time_naive - date_utc < timedelta(days=max_older_news):
			if previous_list and count_match < 3:
				if title in last_news_list:
					enable_save_new = False
					count_match += 1
				else:
					enable_save_new = True
					if count < 5:                
						more_recent_news.append(title)						
						count += 1						
			if not previous_list:
				enable_save_new = True
				if count < 5:
					last_news_list.append(title)					
					count += 1		
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

def click_show_more_news(driver, max_older_news):
	wait = WebDriverWait(driver, 5)	
	count = 0 
	showmore = driver.find_elements(By.CLASS_NAME, 'showMore.showMore--fsNews')
	if len(showmore)!= 0:
		click_more = True
	else:
		click_more = False
	# container_news = driver.find_elements(By.XPATH, '//div[@class="fsNewsSection fsNewsSection__mostRecent fsNewsSection__noTopped"]/a')
	# print(len(container_news))
	
	xpath_expression = '//div[@class="fsNewsSection fsNewsSection__mostRecent fsNewsSection__noTopped"]/a'
	container_news = driver.find_elements(By.XPATH, xpath_expression)
	current_len = len(container_news)
	news_date = container_news[-1].find_element(By.CLASS_NAME, '_newsMeta_gh8ui_5').text
	date_utc = process_date(news_date)


	while click_more and utc_time_naive - date_utc < timedelta(days=max_older_news):
		print("Count: ", count)
		showmore = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'showMore.showMore--fsNews')))
		showmore.click()
		new_len = current_len
		while current_len == new_len:
			time.sleep(0.8)
			new_len = len(driver.find_elements(By.XPATH, xpath_expression))
		time.sleep(1)
		webdriver.ActionChains(driver).send_keys(Keys.END).perform()
		webdriver.ActionChains(driver).send_keys(Keys.PAGE_UP).perform()

		showmore = driver.find_elements(By.CLASS_NAME, 'showMore.showMore--fsNews')
		if len(showmore)== 0:
			click_more = False
		container_news = driver.find_elements(By.XPATH, xpath_expression)
		news_date = container_news[-1].find_element(By.CLASS_NAME, '_newsMeta_gh8ui_5').text
		date_utc = process_date(news_date)
		# container_news = driver.find_elements(By.XPATH, '//div[@class="fsNewsSection fsNewsSection__mostRecent fsNewsSection__noTopped"]/a')
		print("Total news found: ", len(container_news))

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

def extract_news_info(driver, list_upate_news, dict_check_point):
	continue_process = False
	for index, current_dict in enumerate(list_upate_news):

		if dict_check_point['index'] == index:
			continue_process = True

		if continue_process:
			pending_extract = True
			count = 0
			# while pending_extract and count < 5:
			# 	try:
			print("-", index, '/',len(list_upate_news), end= ' ')
			current_url = current_dict['news_link']
			wait_load_detailed_news(driver, current_url)
			dict_news = get_news_info_v2(driver, current_dict)
			if database_enable:
				
				try:
					save_news_database(dict_news)
				except:
					max_size = load_check_point('check_points/max_size.json')
					if len(max_size)!= 0:
						compare = True
					else:
						compare = False
						
					for key, field in dict_news.items():
						if key != 'published':
							if compare:
								if max_size[key] < len(field):
									max_size[key] = len(field)
							else:								
								max_size[key] = len(field)
					save_check_point('check_points/max_size.json', max_size)


			dict_check_point['index'] = index
			# save_check_point('check_points/check_point_m1_news.json', dict_check_point)
			pending_extract = False
				# except:
				# 	count += 1
				# 	print("Loading again")

def main_extract_news(driver):
	dict_check_point = {} #check_previous_execution(file_path = 'check_points/check_point_m1_news.json')
	conf_enable_news = check_previous_execution(file_path = 'check_points/CONFIG_M1.json')
	dict_url_news = load_json('check_points/sports_url_m1.json')
	
	print("New update function: ")

	if len(dict_check_point) == 0:
		print("Create an empty check point ")
		dict_check_point = {'sport':'', 'index':0}
		continue_sport = True
	else:
		dict_check_point['index'] = dict_check_point['index'] + 1
		continue_sport = False

	for sport, news_url in dict_url_news.items():
		if conf_enable_news['SPORTS'][sport]['enable']:
			print("Current sport: ", sport, "#")
			# if dict_check_point['sport'] == sport:
			# 	print("Process sport activated: ")
			# 	continue_sport = True
			# if sport == "FOOTBALL":
			# 	conf_enable_news['MAX_OLDER_DATE_ALLOWED'] = 8
			if continue_sport:
				# dict_check_point['sport'] = sport
				print(sport, news_url)
				wait_update_page(driver, news_url, "section__mainTitle")

				new_test = False

				if new_test:
					check_process_news(driver, sport, conf_enable_news['MAX_OLDER_DATE_ALLOWED'])
				else:
					click_show_more_news(driver,  conf_enable_news['MAX_OLDER_DATE_ALLOWED'])
					list_upate_news = get_list_recent_news(driver, sport, conf_enable_news['MAX_OLDER_DATE_ALLOWED'])

					extract_news_info(driver, list_upate_news, dict_check_point)
					# dict_check_point['index'] = 0

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

if __name__ == "__main__":	
	driver = launch_navigator('https://www.flashscore.com', database_enable)
	initial_settings_m1(driver)
	login(driver, email_= "jignacio@jweglobal.com", password_ = "Caracas5050@\n")	
	main_extract_news(driver)