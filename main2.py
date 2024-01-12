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
from milestone5 import *
from milestone6 import *

days = {'monday': 0,
		'tuesday': 1,
		'wednesday': 2,
		'thursday': 3,
		'friday': 4,
		'saturday': 5,
		'sunday': 6}

database_enable = CONFIG['DATA_BASE']
if database_enable:
	con = getdb()

def main_live():
	driver = launch_navigator('https://www.flashscore.com', database_enable)
	login(driver, email_= "jignacio@jweglobal.com", password_ = "Caracas5050@\n")	
	day_execution_s7 = -1
	execute_ready_s7 = False

	list_s7 = []

	old_execution_schedule_s7 = '*'
	section_schedule = update_data()
	while True:

		new_execution_schedule_s7 = section_schedule['LIVE_SECTION']['TIME']
		print("Main live time: ", new_execution_schedule_s7)
		if new_execution_schedule_s7 != old_execution_schedule_s7:
			execution_schedule_s7 = new_execution_schedule_s7
			old_execution_schedule_s7 = execution_schedule_s7
			day_execution_s7 = -1
		enable_execution_s7, day_execution_s7, execute_ready_s7, execution_schedule_s7 = execute_section(execution_schedule_s7, day_execution_s7, execute_ready_s7)
		if enable_execution_s7:
			live_games(driver, driver, section_schedule['LIVE_SECTION']['SPORTS'])
			list_s7.append(datetime.now().time().strftime('%H:%M:%S'))
			print(list_s7, '\n')

		section_schedule = update_data()
		print("l-", end='')
		# print(stop)
		time.sleep(1)	

# if __name__ == "__main__":	
# 	main_live()
# 	if database_enable:
# 		con.close()
# 	driver.quit()