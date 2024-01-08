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
import schedule
from common_functions import *
from data_base import *
from milestone1 import *
from milestone2 import *
from milestone3 import *
from milestone4 import *
from milestone5 import *
from milestone6 import *


CONFIG = load_json('check_points/CONFIG.json')
database_enable = CONFIG['DATA_BASE']
if database_enable:
	con = getdb()


# def section1():
#     print("Milestone 1")
	
# def section2():
#     print("Milestone 2")

# def section3():
#     print("Milestone 3")

# def section4():
#     print("Milestone 3")
	
# def section5():
#     print("Milestone 3")

# def execute_function(function_name):
#     print(f"Ejecutando función: {function_name}")

# Cargar el archivo JSON
with open('input.json', 'r') as file:
	data = json.load(file)

# Procesar las secciones y programar la ejecución
for section, config in data.items():
	frequency, interval, execution_time = config.split('|')
	hour, minute, second = map(int, execution_time.split(':'))
	print(section, config)
	if frequency == "weekly":
		schedule.every(7).days.at(f"{hour:02d}:{minute:02d}:{second:02d}").do(main_extract_news(driver), section)
	elif frequency == "daily":
		schedule.every(1).days.at(f"{hour:02d}:{minute:02d}:{second:02d}").do(create_leagues(driver), section)
	elif frequency == "monthly":
		# Aproximación: usar días múltiplos del intervalo como una aproximación al mes
		schedule.every(30).days.at(f"{hour:02d}:{minute:02d}:{second:02d}").do(teams_creation(driver), section)
	elif frequency == "minutes":
		schedule.every().day.at(f"{hour:02d}:{minute:02d}:{second:02d}").do(results_fixtures_extraction(driver, name_section = 'results'), section)
		schedule.every(1).minutes.do(execute_function, section).tag('interval_task')
		
	elif frequency == "seconds":
		schedule.every().day.at(f"{hour:02d}:{minute:02d}:{second:02d}").do(results_fixtures_extraction(driver, name_section = 'fixtures'), section)
		schedule.every(15).seconds.do(execute_function, section).tag('interval_task')

	elif frequency == "seconds":
		schedule.every().day.at(f"{hour:02d}:{minute:02d}:{second:02d}").do(results_fixtures_extraction(driver, name_section = 'fixtures'), section)
		schedule.every(15).seconds.do(execute_function, section).tag('interval_task')
	# elif frequency == "minutes":
	#     schedule.every().day.at(f"{hour:02d}:{minute:02d}:{second:02d}").do(results_fixtures_extraction(driver, name_section = 'results'), section)
	#     schedule.every(1).minutes.do(execute_function, section).tag('interval_task')
		
	# elif frequency == "seconds":
	#     schedule.every().day.at(f"{hour:02d}:{minute:02d}:{second:02d}").do(results_fixtures_extraction(driver, name_section = 'fixtures'), section)
	#     schedule.every(15).seconds.do(execute_function, section).tag('interval_task')
# Ejecutar el loop del planificador
while True:
	schedule.run_pending()
	time.sleep(1)
