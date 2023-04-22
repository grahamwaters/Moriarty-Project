# use selenium to open the browser
import os
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()

driver = webdriver.Chrome(options=chrome_options)
print("driver is: ", driver)
print("driver type is: ", type(driver))
print(f'Activated driver: {driver.name} {driver.capabilities["browserVersion"]}')
driver.get("http://localhost:8080/") # open the browser
