from selenium import webdriver
from selenium.webdriver.common.by import By

# 1. open web brower (chrome/fire fox/Edge)
driver = webdriver.Chrome(executable_path="D:\OneDrive\TonyTools\selenium\chromedriver.exe")

# 2. Open Url https://opensource-demo.orangehrmlive.com/web/index.php/auth/login
driver.get("https://opensource-demo.orangehrmlive.com/")

# 3. Enter username (Admin)
bah = driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div/div[1]/div/div[2]/div[2]/form/div[1]/div/div[2]/input')
bah.send_keys("Admin")

# 4. Enter password  (admin123)
driver.find_element(By.XPATH, '/html/body/div/div[1]/div/div[1]/div/div[2]/div[2]/form/div[2]/div/div[2]/input').send_keys("admin123")
# #
# # 5. click on login
driver.find_element(By.XPATH, '/html/body/div/div[1]/div/div[1]/div/div[2]/div[2]/form/div[2]/div/div[2]/input').click()

# # 6. Capture title of the home page. (Actual title)
# act_title = driver.title
# exp_title = 'OrangeHRM'
#
# # 7. Verify title of the page: OrangeHRM (Expected)
# if act_title == exp_title:
#     print('Login Test passed')
# else:
#     print('Login Test failed')
#
# # 8. close browser
# driver.close()