from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

serv_obj=Service('D:\OneDrive\TonyTools\selenium\drivers\chromedriver.exe')
driver=webdriver.Chrome(service=serv_obj)

driver.get('https://www.youtube.com/')
driver.maximize_window()

# driver.find_element(By.XPATH,'/html/body/ytd-app/div[1]/div/ytd-masthead/div[3]/div[2]/ytd-searchbox/form/div[1]/div[1]/input').send_keys('rickroll')
# driver.find_element(By.ID, 'search-icon-legacy').click()
#
# driver.find_element(By.XPATH, "//input[contains(@id, 'search')]").send_keys('T-shirts')
# driver.find_element(By.XPATH, "//button[starts-with(@name, 'submit_')]").click()

driver.find_element(By.XPATH, "//input[@placeholder='Search Best Buy']").send_keys('Sony')
