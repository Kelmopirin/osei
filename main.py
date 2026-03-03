import time  
from selenium import webdriver
from selenium.webdriver.common.by import By
driver = webdriver.Chrome()
driver.get("https://online.osei.hu/uj-idopont-foglalasa")
email,password=open("credentials.txt").readlines()
driver.find_element(By.NAME, "email").send_keys(email)
driver.find_element(By.NAME, "password").send_keys(password)
driver.find_element(By.ID, "btn-sesion").click()
time.sleep(2)
try:
    driver.find_elements(By.CLASS_NAME, "btn-secondary")[1].click()
except:
    print("No secondary button found.")
driver.get("https://online.osei.hu/uj-idopont-foglalasa")
driver.find_element(By.ID, "rendelo116476").click()
driver.find_element(By.ID, "306048").click()
time.sleep(2)
driver.quit()