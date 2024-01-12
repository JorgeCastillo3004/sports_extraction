import concurrent.futures
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
from main1 import *
from main2 import *

database_enable = CONFIG['DATA_BASE']
if database_enable:
	con = getdb()

if __name__ == "__main__":	
	with concurrent.futures.ThreadPoolExecutor() as executor:
		# Submit the functions for execution
		future1 = executor.submit(main_others)
		future2 = executor.submit(main_live)

		# Wait for both functions to complete
		concurrent.futures.wait([future1, future2])

		# Check if any exceptions occurred during execution
		for future in [future1, future2]:
			if future.exception():
				print(f"Exception occurred: {future.exception()}")