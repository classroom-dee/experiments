from selenium import webdriver
from selenium.webdriver.firefox.service import Service

service = Service("./geckodriver.exe")
driver = webdriver.Firefox(service=service)
driver.get("https://images.google.com")
driver.quit()
