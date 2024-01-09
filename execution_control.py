
import time
from datetime import date, timedelta
from datetime import datetime

days = {
    'monday': 0,
    'tuesday': 1,
    'wednesday': 2,
    'thursday': 3,
    'friday': 4,
    'saturday': 5,
    'sunday': 6
}

def execute_section(execution_schedule):
	global day_execution, execute_ready
	enable_execution = False	
	if 'montly' in execution_schedule and not execute_ready:		
		interval, day_exe, time_str = execution_schedule.split("|")
		if datetime.now().day == days[day_exe]:
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
		print("Case daily")
		_, time_str = execution_schedule.split("|")		
		time_execution = datetime.strptime(time_str, '%H:%M:%S').time()
		if datetime.now().time() >= time_execution:
			enable_execution = True
			execute_ready = True
			day_execution = datetime.now().day
	
	if datetime.now().day != day_execution:		
		execute_ready = False
		day_execution = -1
	return enable_execution

driver = 1
def extract_news(driver):
	print("Extracting news: ")

def create_leagues(driver):
	print("Create create_leagues: ")

def create_teams(driver):
	print("Create_teams: ")
# with open('input.json', 'r') as file:
# 	section_schedule = json.load(file)

section_schedule =	{
		"main_extract_news": "daily|4:10:00",
	    "create_leagues": "weekly|monday|4:22:30",
	    "teams_creation": "montly|15|4:25:15",
	    "results_fixtures_extraction": "daily|4:27:15",
	    "GET_FIXTURES": "seconds|30",	    
	    "GET_PLAYERS": "minute|4:32:15"
	}


count = 0
day_execution = -1
execute_ready = False
while True:
	print(count, end = '-')
	execution_schedule = section_schedule['main_extract_news']
	enable_execution = execute_section(execution_schedule)
	if enable_execution:
		extract_news(driver)
	# print(stop)
	time.sleep(1)
	count += 1
