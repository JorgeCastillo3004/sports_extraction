

# from selenium import webdriver
# from selenium.webdriver.firefox.service import Service as FirefoxService
# from webdriver_manager.firefox import GeckoDriverManager


# # Initialize FirefoxOptions
# options = webdriver.FirefoxOptions()

# # Disable features related to automation
# options.set_preference("dom.webdriver.enabled", False)
# options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# # Disable automation switches
# options.set_preference("browser.tabs.remote.autostart", False)
# options.set_preference("browser.tabs.remote.autostart.1", False)
# options.set_preference("browser.tabs.remote.autostart.2", False)
# options.set_preference("browser.tabs.remote.force-enable", False)

# # Headless mode if database_enable is True
# options.headless = True

# # Other arguments
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')
# options.add_argument('--disable-gpu')

# # Initialize Firefox driver with the configured options
# driver = webdriver.Firefox(options=options)
# driver = webdriver.Firefox(options=options, service=FirefoxService(GeckoDriverManager().install()))
# # # Navigate to a website

# # # driver = webdriver.Firefox()

# # # Navigate to a website
# # driver.get("https://www.flashscore.com/golf/pga-tour/wgc-dell-technologies-match-play/standings/#/GzSXhozK/table")


# # print("Done navigator open")

# from selenium import webdriver
# from selenium.webdriver.firefox.service import Service as FirefoxService
# from webdriver_manager.firefox import GeckoDriverManager

# driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
# driver.get('https://www.bstackdemo.com/')

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
