
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

def execute_section(execution_schedule, day_execution, execute_ready):
	# global day_execution, execute_ready
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
		# print("Case daily")
		_, time_str = execution_schedule.split("|")		
		time_execution = datetime.strptime(time_str, '%H:%M:%S').time()
		if datetime.now().time() >= time_execution:
			enable_execution = True
			execute_ready = True
			day_execution = datetime.now().day

	if 'minute' in execution_schedule and not execute_ready:
		# print("Case daily")
		_, time_str = execution_schedule.split("|")		
		time_execution = datetime.strptime(time_str, '%H:%M:%S')
		if datetime.now().time() >= time_execution.time():
			enable_execution = True
			execute_ready = True
			time_execution = time_execution + timedelta(minutes=1)
			# day_execution = datetime.now().day
	
	if datetime.now().day != day_execution:		
		execute_ready = False
		day_execution = -1
	return enable_execution, day_execution, execute_ready

driver = 1
def extract_news(driver):
	print("Extracting news: ")

def create_leagues(driver):
	print("Create create_leagues: ")

def create_teams(driver):
	print("Create_teams: ")

def create_player(driver):
	print("Create_teams: ")
# with open('input.json', 'r') as file:
# 	section_schedule = json.load(file)

section_schedule =	{
		"EXTRACT_NEWS": "daily|4:50:00",
	    "CREATE_LEAGUES": "weekly|monday|4:22:30",
	    "TEAMS_CREATION": "montly|15|4:25:15",
	    "GET_RESULTS": "daily|4:27:15",
	    "GET_FIXTURES": "seconds|30",
	    "GET_PLAYERS": "minute|4:48:15"
	}


count = 0
day_execution_s1 = -1
execute_ready_s1 = False
day_execution_s2 = -1
execute_ready_s2 = False
while True:	
	print(datetime.now().time())
	execution_schedule = section_schedule['EXTRACT_NEWS']
	enable_execution_s1, day_execution_s1, execute_ready_s1 = execute_section(execution_schedule, day_execution_s1, execute_ready_s1)
	if enable_execution_s1:
		extract_news(driver)

	execution_schedule_s2 = section_schedule['CREATE_LEAGUES']
	enable_execution_s2, day_execution_s2, execute_ready_s2 = execute_section(execution_schedule_s2, day_execution_s2, execute_ready_s2)
	if enable_execution:
		extract_news(driver)
	# print(stop)
	time.sleep(1)
	count += 1
