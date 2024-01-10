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

def execute_section(execution_schedule, day_execution, execute_ready):
	# global day_execution, execute_ready
	enable_execution = False	
	if 'montly' in execution_schedule and not execute_ready:		
		interval, day_exe, time_str = execution_schedule.split("|")
		if datetime.now().day == day_exe:
			time_execution = datetime.strptime(time_str, '%H:%M:%S').time()
			if datetime.now().time() > time_execution:
				print(time_execution)
				enable_execution = True
				execute_ready = True

	if 'weekly' in execution_schedule and not execute_ready:
		interval, day_exe, time_str = execution_schedule.split("|")
		time_execution = datetime.strptime(time_str, '%H:%M:%S').time()		
		if datetime.now().weekday() == days[day_exe] and datetime.now().time() > time_execution:			
			enable_execution = True
			execute_ready = True
			day_execution = datetime.now().day

	if 'daily' in execution_schedule and not execute_ready:		
		# print("Case daily")
		_, time_str = execution_schedule.split("|")		
		time_execution = datetime.strptime(time_str, '%H:%M:%S').time()
		if datetime.now().time() >= time_execution:
			enable_execution = True
			execute_ready = True
			day_execution = datetime.now().day
	
	if datetime.now().day != day_execution:		
		execute_ready = False
		day_execution = -1

	#################################################################
	# 			SECTION SECONDS-MINUTES 							#
	#################################################################
	if 'minute' in execution_schedule:
		# print("Case daily")
		part1, time_str = execution_schedule.split("|")		
		time_execution = datetime.strptime(time_str, '%H:%M:%S')
		if datetime.now().time() >= time_execution.time() and datetime.now().time() < (time_execution + timedelta(minutes=1)).time():
			enable_execution = True
			execute_ready = False
			time_execution = time_execution + timedelta(minutes=1)
			execution_schedule = part1 +'|'+str(time_execution.time())			
			# day_execution = datetime.now().day
	if 'seconds' in execution_schedule:
		if len(execution_schedule.split("|")) == 2:
			part1, seconds_str = execution_schedule.split("|")			
			option = 1
		if len(execution_schedule.split("|")) == 3:
			part1, seconds_str, time_str = execution_schedule.split("|")
			option = 2

		if option == 1:			
			time_execution = datetime.now()
			enable_execution = True
			execute_ready = False				
			time_execution = time_execution + timedelta(seconds = int(seconds_str))
			execution_schedule = part1 +'|' + seconds_str +'|'+ time_execution.time().strftime('%H:%M:%S') 
				
		if option == 2:
			time_execution = datetime.strptime(time_str, '%H:%M:%S')			
			if datetime.now().time() >= time_execution.time() and datetime.now().time() < (time_execution + timedelta(1)).time():
				enable_execution = True
				execute_ready = False
				time_execution = time_execution + timedelta(seconds = int(seconds_str))				
				execution_schedule = part1 +'|' + seconds_str +'|'+ time_execution.time().strftime('%H:%M:%S') 
				print(execution_schedule)
			# day_execution = datetime.now().day

	return enable_execution, day_execution, execute_ready, execution_schedule

driver = 1
# def extract_news(driver):
# 	print("Extracting news: ")

# def create_leagues(driver):
# 	print("Create Leagues: ")

# def create_teams(driver):
# 	print("Create_teams: ")

# def get_results(driver, section = 'results'):
# 	print("Get {}".format(section))

# def create_player(driver):
# 	print("Create_players: ")

def update_data():
	with open('execution_control.json', 'r') as file:
		section_schedule = json.load(file)
	return section_schedule

# section_schedule =	{
# 		"EXTRACT_NEWS": "daily|11:35:15",
# 	    "CREATE_LEAGUES": "weekly|tuesday|11:30:00",
# 	    "CREATE_TEAMS": "montly|9|11:30:15",
# 	    "GET_RESULTS": "minute|11:27:15",
# 	    "GET_FIXTURES": "seconds|30",
# 	    "GET_PLAYERS": "seconds|30|11:50:00"
# 	}

database_enable = CONFIG['DATA_BASE']
if database_enable:
	con = getdb()

def main(driver):
	day_execution_s1 = -1
	day_execution_s2 = -1
	day_execution_s3 = -1
	day_execution_s4 = -1
	day_execution_s5 = -1
	day_execution_s6 = -1
	execute_ready_s1 = False
	execute_ready_s2 = False
	execute_ready_s3 = False
	execute_ready_s4 = False
	execute_ready_s5 = False
	execute_ready_s6 = False

	list_s1 = []
	list_s2 = []
	list_s3 = []
	list_s4 = []
	list_s5 = []
	list_s6 = []
	old_execution_schedule_s1 = '*'
	old_execution_schedule_s2 = '*'
	old_execution_schedule_s3 = '*'
	old_execution_schedule_s4 = '*'
	old_execution_schedule_s5 = '*'
	old_execution_schedule_s6 = '*'
	section_schedule = update_data()
	while True:
		new_execution_schedule_s1 = section_schedule['EXTRACT_NEWS']['TIME']
		if new_execution_schedule_s1 != old_execution_schedule_s1:
			execution_schedule_s1 = new_execution_schedule_s1
			old_execution_schedule_s1 = execution_schedule_s1	
		enable_execution_s1, day_execution_s1, execute_ready_s1, _ = execute_section(execution_schedule_s1, day_execution_s1, execute_ready_s1)
		if enable_execution_s1:		
			main_extract_news(driver, section_schedule['EXTRACT_NEWS']['SPORTS'], section_schedule['EXTRACT_NEWS']['MAX_OLDER_DATE_ALLOWED'])
			list_s1.append(datetime.now().time().strftime('%H:%M:%S'))
			print(list_s1, '\n')

		new_execution_schedule_s2 = section_schedule['CREATE_LEAGUES']['TIME']
		if new_execution_schedule_s2 != old_execution_schedule_s2:
			execution_schedule_s2 = new_execution_schedule_s2
			old_execution_schedule_s2 = execution_schedule_s2	
		enable_execution_s2, day_execution_s2, execute_ready_s2, _ = execute_section(execution_schedule_s2, day_execution_s2, execute_ready_s2)
		if enable_execution_s2:
			create_leagues(driver, section_schedule['CREATE_LEAGUES']['SPORTS'])
			list_s2.append(datetime.now().time().strftime('%H:%M:%S'))
			print(list_s2, '\n')

		new_execution_schedule_s3 = section_schedule['CREATE_TEAMS']['TIME']
		if new_execution_schedule_s3 != old_execution_schedule_s3:
			execution_schedule_s3 = new_execution_schedule_s3
			old_execution_schedule_s3 = execution_schedule_s3
		enable_execution_s3, day_execution_s3, execute_ready_s3, _ = execute_section(execution_schedule_s3, day_execution_s3, execute_ready_s3)
		if enable_execution_s3:
			teams_creation(driver, section_schedule['CREATE_TEAMS']['SPORTS'])
			list_s3.append(datetime.now().time().strftime('%H:%M:%S'))
			print(list_s3, '\n')

		new_execution_schedule_s4 = section_schedule['GET_RESULTS']['TIME']
		if new_execution_schedule_s4 != old_execution_schedule_s4:
			execution_schedule_s4 = new_execution_schedule_s4
			old_execution_schedule_s4 = execution_schedule_s4
		enable_execution_s4, day_execution_s4, execute_ready_s4, execution_schedule_s4 = execute_section(execution_schedule_s4, day_execution_s4, execute_ready_s4)	
		if enable_execution_s4:
			results_fixtures_extraction(driver, section_schedule['GET_RESULTS']['SPORTS'], section = 'results')
			list_s4.append(datetime.now().time().strftime('%H:%M:%S'))
			print(list_s4, '\n')

		new_execution_schedule_s5 = section_schedule['GET_FIXTURES']['TIME']
		if new_execution_schedule_s5 != old_execution_schedule_s5:
			execution_schedule_s5 = new_execution_schedule_s5
			old_execution_schedule_s5 = execution_schedule_s5		
		enable_execution_s5, day_execution_s5, execute_ready_s5, execution_schedule_s5 = execute_section(execution_schedule_s5, day_execution_s5, execute_ready_s5)
		if enable_execution_s5:
			results_fixtures_extraction(driver, section_schedule['GET_FIXTURES']['SPORTS'], section = 'fixtures')
			list_s5.append(datetime.now().time().strftime('%H:%M:%S'))
			print(list_s5, '\n')

		new_execution_schedule_s6 = section_schedule['GET_PLAYERS']['TIME']
		if new_execution_schedule_s6 != old_execution_schedule_s6:
			execution_schedule_s6 = new_execution_schedule_s6
			old_execution_schedule_s6 = execution_schedule_s6
		enable_execution_s6, day_execution_s6, execute_ready_s6, execution_schedule_s6 = execute_section(execution_schedule_s6, day_execution_s6, execute_ready_s6)
		if enable_execution_s6:
			players(driver, section_schedule['GET_PLAYERS']['SPORTS'])
			list_s6.append(datetime.now().time().strftime('%H:%M:%S'))
			print(list_s6, '\n')

		section_schedule = update_data()

		# print(stop)
		time.sleep(1)	

if __name__ == "__main__":  	
	driver = launch_navigator('https://www.flashscore.com', database_enable)
	login(driver, email_= "jignacio@jweglobal.com", password_ = "Caracas5050@\n")	
	main(driver)
	if database_enable:
		con.close()
	driver.quit()