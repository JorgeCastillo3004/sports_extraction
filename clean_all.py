import psycopg2
from datetime import date, timedelta
from datetime import datetime
import argparse
from common_functions import load_json
import os

# if os.path.isfile("check_points/last_saved_news.json"):
# 	os.remove("check_points/last_saved_news.json")

if os.path.isfile("check_points/sports_id.json"):
	os.remove("check_points/sports_id.json")

if os.path.isfile("check_points/leagues_info.json"):
	os.remove("check_points/leagues_info.json")

if os.path.isfile('check_points/global_check_point.json'):
	os.remove('check_points/global_check_point.json')

files = os.listdir('check_points/leagues_season/')

print("Files and folder removed: ")
# Iterate over each file and remove it
for file_name in files:
    file_path = os.path.join('check_points/leagues_season/', file_name)
    if os.path.isfile(file_path):  # Check if it's a file and not a directory
        os.remove(file_path)
        print(f"Removed {file_path}")

files = os.listdir('check_points/news/')

# Iterate over each file and remove it
for file_name in files:
    file_path = os.path.join('check_points/news/', file_name)
    if os.path.isfile(file_path):  # Check if it's a file and not a directory
        os.remove(file_path)
        print(f"Removed {file_path}")


def getdb():
	return psycopg2.connect(
			host="localhost",
			user="wohhu",
			password="caracas123",
	dbname='sports_db',
	)

con = getdb()


print("Delete all from score_entity ")
query = "DELETE FROM score_entity;"
cur = con.cursor()
cur.execute(query)
con.commit()


print("Delete all from match_detail ")
query = "DELETE FROM match_detail;"
cur = con.cursor()
cur.execute(query)
con.commit()

print("Delete all from match ")
query = "DELETE FROM match;"
cur = con.cursor()
cur.execute(query)
con.commit()

print("Delete all from stadium ")
query = "DELETE FROM stadium;"
cur = con.cursor()
cur.execute(query)
con.commit()

print("Delete all from league_team ")
query = "DELETE FROM league_team;"
cur = con.cursor()
cur.execute(query)
con.commit()

print("Delete all from team_players_entity")
query = "DELETE FROM team_players_entity;"
cur = con.cursor()
cur.execute(query)
con.commit()

print("Delete all from season ")
query = "DELETE FROM season;"
cur = con.cursor()
cur.execute(query)
con.commit()


print("Delete all from league ")
query = "DELETE FROM league;"
cur = con.cursor()
cur.execute(query)
con.commit()


print("Delete all from team ")
query = "DELETE FROM team;"
cur = con.cursor()
cur.execute(query)
con.commit()

print("Delete all from sport ")
query = "DELETE FROM sport;"
cur = con.cursor()
cur.execute(query)
con.commit()

print("Delete all from news ")
query = "DELETE FROM news;"
cur = con.cursor()
cur.execute(query)
con.commit()

cur.close()