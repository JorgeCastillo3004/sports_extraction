from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
from selenium import webdriver
from datetime import datetime
import pandas as pd
import random
import time
import json
import re
import os
from selenium.webdriver.support.ui import Select
from datetime import date, timedelta
import string

from common_functions import *
from data_base import *
from milestone1 import *
from milestone2 import *
from milestone3 import *
from milestone4 import *
# from milestone5 import *
from milestone6 import *
from milestone7 import *

CONFIG = load_json('check_points/CONFIG.json')
database_enable = CONFIG['DATA_BASE']
if database_enable:
	con = getdb()

def main(driver):
	main_extract_news_enable = False  	# 1
	create_leagues_flag = False 	    # 2
	teams_creation_flag = False	  	    # 3
	results_extraction_flag = False		# 4
	fixture_extraction_flag = False		# 5
	players_flag = False 				# 6	
	live_games_flag = True	
	dict_sports = load_json('check_points/sports_url_m2.json')
	
	if main_extract_news_enable:
		main_extract_news(driver, ["FOOTBALL"], MAX_OLDER_DATE_ALLOWED = 30)

	if create_leagues_flag:
		create_leagues(driver, ["FOOTBALL"])

	if teams_creation_flag:
		teams_creation(driver, ["FOOTBALL"])

	if results_extraction_flag:
		results_fixtures_extraction(driver, ["HOCKEY"], name_section = 'results')

	if fixture_extraction_flag:
		results_fixtures_extraction(driver, ["HOCKEY"], name_section = 'fixtures')

	if players_flag:
		players(driver, ["HOCKEY", "BASKETBALL"])

	if live_games_flag:
		live_games(driver, ["FOOTBALL", "TENNIS", "BASKETBALL", "HOCKEY",
					  "BASEBALL","BOXING", "VOLLEYBALL"])

if __name__ == "__main__":  	
	driver = launch_navigator('https://www.flashscore.com', database_enable)
	login(driver, email_= "jignacio@jweglobal.com", password_ = "Caracas5050@\n")	
	main(driver)
	if database_enable:
		con.close()
	driver.quit()