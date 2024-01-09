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


import schedule
import time
import datetime

def job_func():
    print("Ejecutando la tarea programada...")

def schedule_weekly(day_of_week, hour, minute):
    # Diccionario para mapear nombres de días a números
    days = {
        'monday': 0,
        'twesday': 1,
        'miércoles': 2,
        'jueves': 3,
        'viernes': 4,
        'sábado': 5,
        'domingo': 6
    }

    # Mapear el nombre del día ingresado al número correspondiente
    day_number = days.get(day_of_week.lower())

    if day_number is None:
        print("Error: Nombre de día no válido.")
        return

    # Crear la programación usando la biblioteca schedule
    schedule.every().day.at(f"{hour}:{minute}").do(job_func).day.at(f"{hour}:{minute}").do(job_func).wednesday.at(f"{hour}:{minute}").do(job_func)

    while True:
        # Verificar si el día actual coincide con el día programado
        if datetime.datetime.now().weekday() == day_number:
            schedule.run_pending()
        time.sleep(1)

# Ejemplo de uso
schedule_weekly('lunes', '10', '30')










def main_extract_news(driver):
	print("Extract news")
	
def create_leagues(driver):
    print("Milestone 2")

def teams_creation(driver):
    print("Milestone 3")

def results_fixtures_extraction(driver, name_section = 'results'):
    print("Milestone 4")
	
def results_fixtures_extraction(driver, name_section = 'fixtures'):
    print("Milestone 5")

def players(driver):
    print("Milestone 2")

# Cargar el archivo JSON
with open('input.json', 'r') as file:
	data = json.load(file)
# driver = 15
# driver = launch_navigator('https://www.flashscore.com', database_enable)
# login(driver, email_= "jignacio@jweglobal.com", password_ = "Caracas5050@\n")	
# Procesar las secciones y programar la ejecución


def set_time_execution(function_name, frequency_time):	
	frequency, time_config = frequency_time.split('|')
	hour, minute, second = map(int, time_config.split(':'))
	if frequency == "weekly":
		schedule.every(7).days.at(f"{hour:02d}:{minute:02d}:{second:02d}").do(function_name, section)
	elif frequency == "daily":
		schedule.every(1).days.at(f"{hour:02d}:{minute:02d}:{second:02d}").do(function_name, section)
	elif frequency == "monthly":
		# Aproximación: usar días múltiplos del intervalo como una aproximación al mes
		schedule.every(30).days.at(f"{hour:02d}:{minute:02d}:{second:02d}").do(function_name, section)
	elif frequency == "minutes":
		schedule.every().day.at(f"{hour:02d}:{minute:02d}:{second:02d}").do(function_name, section)
		schedule.every(1).minutes.do(execute_function, section).tag('interval_task')
		
	elif frequency == "seconds":
		schedule.every().day.at(f"{hour:02d}:{minute:02d}:{second:02d}").do(function_name, section)
		schedule.every(15).seconds.do(execute_function, section).tag('interval_task')

	# elif frequency == "seconds":
	# 	schedule.every().day.at(f"{hour:02d}:{minute:02d}:{second:02d}").do(function_name, section)
	# 	schedule.every(15).seconds.do(execute_function, section).tag('interval_task')
	# elif frequency == "minutes":
	#     schedule.every().day.at(f"{hour:02d}:{minute:02d}:{second:02d}").do(results_fixtures_extraction(driver, name_section = 'results'), section)
	#     schedule.every(1).minutes.do(execute_function, section).tag('interval_task')
		
	# elif frequency == "seconds":
	#     schedule.every().day.at(f"{hour:02d}:{minute:02d}:{second:02d}").do(results_fixtures_extraction(driver, name_section = 'fixtures'), section)
	#     schedule.every(15).seconds.do(execute_function, section).tag('interval_task')
# Ejecutar el loop del planificador

for section, time_config in data.items():
	if section == 'EXTRAC_NEWS':		
		function_name = main_extract_news(driver)
	if section == 'CREATE_LEAGUES':
		function_name = create_leagues(driver)
	if section == 'CREATE_TEAMS':
		function_name = teams_creation(driver)
	if section == 'GET_RESULTS':
		function_name = results_fixtures_extraction(driver, name_section = 'results')
	if section == 'GET_FIXTURES':
		function_name = results_fixtures_extraction(driver, name_section = 'fixtures')
	if section == 'GET_PLAYERS':
		function_name = players(driver)
	set_time_execution(function_name, time_config)
	# frequency, execution_time = config.split('|')
	
	# print(section, config)

if __name__ == "__main__": 	
	while True:
		schedule.run_pending()
		time.sleep(1)

	if database_enable:
		con.close()
	driver.quit()


