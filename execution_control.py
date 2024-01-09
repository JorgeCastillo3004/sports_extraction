
import time
from datetime import date, timedelta
from datetime import datetime

section_schedule =	{
		"main_extract_news": "weekly|tuesday|2:15:00",
	    "create_leagues": "weekly|monday|4:22:30",
	    "teams_creation": "montly|4:25:15",
	    "results_fixtures_extraction": "daily|4:27:15",
	    "GET_FIXTURES": "seconds|30",	    
	    "GET_PLAYERS": "minute|4:32:15"
	}


days = {
    'monday': 0,
    'tuesday': 1,
    'wednesday': 2,
    'thursday': 3,
    'friday': 4,
    'saturday': 5,
    'sunday': 6
}

def extract_news():
	print("Extracting news: ")
# with open('input.json', 'r') as file:
# 	section_schedule = json.load(file)
count = 0
day_execution = -1
execute_ready = False
while True and count < 100:
	print(count, end = '-')
	
	execution_schedule = section_schedule['main_extract_news']
	if 'montly' in execution_schedule and not execute_ready:
		print("Case montly: ")
		interval, day_exe, time_str = execution_schedule.split("|")
		if datetime.now().day == days[day_exe]:
			time_execution = datetime.strptime(time_str, '%H:%M:%S')
			print(time_execution)
			execute_ready = True

	if 'weekly' in execution_schedule and not execute_ready:

		interval, day_exe, time_str = execution_schedule.split("|")
		time_execution = datetime.strptime(time_str, '%H:%M:%S')
		print("Case weekly: ", day_exe, days[day_exe])
		print(time_execution)
		if datetime.now().day == days[day_exe] and datetime.now() > time_execution:		
			print("Execute function: ")
			extract_news()
			execute_ready = True
			day_execution = datetime.now().day
	if datetime.now().day != day_execution:
		execute_ready = False
		day_execution = -1

	time.sleep(1)
	count += 1
