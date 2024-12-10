from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

# url = f"map.naver.com/p/search/{keyword}"
# driver = webdriver.Chrome(options=options)

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")   # 화면 크게
options.add_experimental_option("detach", True) # 자동종료 방지
driver = webdriver.Chrome(options=options)

URL = "https://map.naver.com/p/"
driver.get(url=URL)


# iframe focus
# def switch_left():
#     driver.switch_to.parent_frame()
#     iframe = driver.find_element(By.XPATH,'//*[@id="searchIframe"]')
#     driver.switch_to.frame(iframe)

# wait = WebDriverWait(driver, 10)
# wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchIframe"]')))
# switch_left()

def switch_right():
    ############## iframe으로 오른쪽 포커스 맞추기 ##############
    driver.switch_to.parent_frame()
    iframe = driver.find_element(By.XPATH,'//*[@id="entryIframe"]')
    driver.switch_to.frame(iframe)