from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

serv_obj=Service('D:\OneDrive\TonyTools\selenium\drivers\chromedriver.exe')
driver=webdriver.Chrome(service=serv_obj)

driver.get('https://www.bestbuy.ca/en-ca')
driver.maximize_window()

driver.find_element(By.NAME, 'search').send_keys('sony')
# driver.find_element(By.XPATH, '//*[@id="root"]/div/div[3]/header/div/div/div[2]/div/div/div[2]/div/div/form/div/div/button[2]/svg').click()
driver.find_element(By.XPATH, "//input[@placeholder='Search Best Buy']").send_keys('Sony')
driver.find_element(By.XPATH, "//div[@class='autocompleteContent_jYkqN']//li[1]//a[1]").click()

# how to write xpath manully
 