from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from datetime import date, timedelta, datetime
from selenium import webdriver
import chromedriver_autoinstaller
import random
import string
import requests
import json
import os
import re
import time
local_time_naive = datetime.now()
utc_time_naive = datetime.utcnow()
time_difference_naive = utc_time_naive - local_time_naive

#####################################################################
#					CHECK POINTS BLOCK 								#
#####################################################################
def int_folders():
	if not os.path.exists('check_points'):
		os.mkdir('check_points')
	if not os.path.exists('check_points/results/'):
		os.mkdir("check_points/results/")
	if not os.path.exists('check_points/fixtures/'):
		os.mkdir("check_points/fixtures/")
	if not os.path.exists('check_points/standings/'):
		os.mkdir("check_points/standings/")
	if not os.path.exists('images'):
		os.mkdir("images")
	if not os.path.exists('images/logos'):
		os.mkdir('images/logos')
	if not os.path.exists('images/players'):
		os.mkdir('images/players')
	if not os.path.exists('images/news'):
		os.mkdir("images/news")
	if not os.path.exists('images/news/small_images'):
		os.mkdir("images/news/small_images/")
	if not os.path.exists('images/news/full_images'):
		os.mkdir("images/news/full_images/")
	if not os.path.isfile('check_points/CONFIG.json'):
		CONFIG = {"get_news_m1": True, 	# Activate M1
			"sports_link": False, 		# 
			"update_links": True,    	#
			"get_news": False,			# Get news from each sport
			"DATA_BASE": False}			# Save in data base
		save_check_point('check_points/CONFIG.json', CONFIG)

def get_sports_links_news(driver):
	wait = WebDriverWait(driver, 1)
	buttonmore = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'arrow.topMenuSpecific__moreIcon')))

	mainsports = driver.find_elements(By.XPATH, '//div[@class="topMenuSpecific__items"]/a')

	dict_links = {}

	for link in mainsports[1:]:		
		sport_name = '_'.join(link.text.split())
		sport_url = link.get_attribute('href')
		if sport_name != '':			
			dict_links[sport_name] = sport_url	
	buttonmore.click()

	list_links = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'topMenuSpecific__dropdownItem')))
	list_links = driver.find_elements(By.CLASS_NAME, 'topMenuSpecific__dropdownItem')

	for link in list_links:
		sport_name = '_'.join(link.text.split())
		sport_url = link.get_attribute('href')		
		if sport_name == '':
			sport_name = sport_url.split('/')[-2].upper()
		dict_links[sport_name] = sport_url

	buttonminus = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'arrow.topMenuSpecific__moreIcon')))
	buttonminus.click()
	return dict_links

def load_json(filename):
    # Opening JSON file
    with open(filename, 'r') as openfile:        
        json_object = json.load(openfile)
    return json_object

def save_check_point(filename, dictionary):
    json_object = json.dumps(dictionary, indent=4)
    with open(filename, "w") as outfile:
        outfile.write(json_object)

def load_check_point(filename):
    # Opening JSON file
    if os.path.isfile(filename):
        with open(filename, 'r') as openfile:        
            json_object = json.load(openfile)
    else:
        json_object = {}
    return json_object

def check_previous_execution(file_path = 'check_points/scraper_control.json'):
    if os.path.isfile(file_path):
        dict_scraper_control = load_json(file_path)
    else:
        dict_scraper_control = {}
    return dict_scraper_control

def launch_navigator(url, database_enable):
	options = webdriver.ChromeOptions()
	options.add_argument("--disable-blink-features=AutomationControlled") 
	options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
	options.add_experimental_option("useAutomationExtension", False)
	if database_enable:
		options.add_argument('--headless')
	options.add_argument('--no-sandbox')
	options.add_argument('--disable-dev-shm-usage')
	# chrome_path = os.getcwd()+'/chrome_files'
	# print("chrome_path: ", chrome_path)
	# options.add_argument(r"user-data-dir={}".format(chrome_path))
	# options.add_argument(r"profile-directory=Profile1")

	drive_path = Service('/usr/local/bin/chromedriver')

	driver = webdriver.Chrome(service=drive_path,  options=options)
	driver.get(url)
	return driver

def login(driver, email_= "jignacio@jweglobal.com", password_ = "Caracas5050@\n"):
    wait = WebDriverWait(driver, 10)

    # Accept cookies
    accept_button = wait.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
    accept_button.click()
    # Click on login
    login_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'header__icon.header__icon--user')))
    # login_button = driver.find_element(By.CLASS_NAME, 'header__icon.header__icon--user')
    login_button.click()
    # Select login mode
    continue_email = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "ui-button.ui-formButton.social__button.email")))
    continue_email.click()

    email = driver.find_element(By.ID,'email')
    email = wait.until(EC.visibility_of_element_located((By.ID,'email')))
    email.send_keys(email_)

    email = driver.find_element(By.ID,'passwd')
    email.send_keys(password_)
    time.sleep(6)
    print("Login...")
    # webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

def wait_update_page(driver, url, class_name):
	wait = WebDriverWait(driver, 10)
	current_tab = driver.find_elements(By.CLASS_NAME, class_name)
	driver.get(url)

	if len(current_tab) == 0:
		current_tab = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, class_name)))
	else:
		element_updated = wait.until(EC.staleness_of(current_tab[0]))	

def wait_load_detailed_news(driver, url_news):	
	wait = WebDriverWait(driver, 10)
	class_name = 'fsNewsArticle__title'
	title = driver.find_elements(By.CLASS_NAME, class_name)
	driver.get(url_news)
	if len(title) == 0:
		title = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, class_name)))
	else:
		wait.until(EC.staleness_of(title[0]))

def get_mentions(driver):
	mention_list = ''
	mentions = driver.find_elements(By.XPATH, '//div[@class="fsNewsArticle__mentions"]/a')
	for mention in mentions:
		if mention_list == '':
			mention_list = mention.text
		else:
			mention_list = mention_list +', '+mention.text
	return mention_list

def save_image(driver, image_url, image_path):
	img_data = requests.get(image_url).content

	with open(image_path, 'wb') as handler:
		handler.write(img_data)

def process_date(date):
	date_format = "%d.%m.%Y %H:%M:%S"
	if 'min ago' in date:		
		min_ = int(re.findall(r'(\d+)\ min ago', date)[0])        
		news_time_post = local_time_naive - timedelta(minutes=min_)
	elif ' h ago' in date:
		hours_ = int(re.findall(r'(\d+)\ h ago', date)[0])        
		news_time_post = local_time_naive - timedelta(hours=hours_)
	elif 'Yesterday' in date:
		previous_day = local_time_naive - timedelta(days=1)
		time_post = re.findall(r'\d+:\d+', date)[0]+':00'
		time_post = datetime.strptime(time_post, "%H:%M:%S")
		news_time_post = datetime(
			previous_day.year,
			previous_day.month,
			previous_day.day,
			time_post.hour,
			time_post.minute,
			time_post.second,
		)
	elif 'Just now' in date:
		news_time_post = local_time_naive
	else:		
		date = date +':00'
		news_time_post = datetime.strptime(date, date_format)	

	news_utc_time = news_time_post + time_difference_naive
	return news_utc_time

def random_name(folder = 'news_images', termination = '.jpg'):
	file_name = ''.join(random.choice(string.ascii_lowercase) for i in range(16))
	return os.path.join(folder,file_name + termination)

def random_id():
	rand_id = ''.join(random.choice(string.ascii_lowercase) for i in range(16))
	rand_id = rand_id + str(random.choice([0, 9]))
	digits = ''.join([str(random.randint(0, 9)) for i in range(4)])
	return rand_id+digits

int_folders()