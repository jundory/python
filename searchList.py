from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC    #expected_conditions (EC): Selenium에서 제공하는 여러 가지 조건을 정의한 모듈

import time
import json

options = Options()
# 차단 방지 user-agent 설정
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
# 화면 크게
options.add_argument("--start-maximized")
 # 자동종료 방지
options.add_experimental_option("detach", True)

# run webdriver
driver = webdriver.Chrome(options=options)
keyword = "돈카츠"
# URL = f"https://map.naver.com/p/search/{keyword}"
# URL = f"https://pcmap.place.naver.com/place/list?query={keyword}&x=126.97828200000112&y=37.56846119999963&clientX=126.97825&clientY=37.566551"
URL = f"https://map.naver.com/restaurant/list?query={keyword}&x=126.97828200000112&y=37.56846119999963&clientX=126.97825&clientY=37.566551"


driver.get(url = URL)


# iframe focus
def switch_left():
    driver.switch_to.parent_frame()
    iframe = driver.find_element(By.XPATH,'//*[@id="searchIframe"]')
    driver.switch_to.frame(iframe)

wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchIframe"]')))
switch_left()


scroll_container = driver.find_element(By.CSS_SELECTOR, ".Ryr1F")
# execute_script = js 실행.
last_height = driver.execute_script("return arguments[0].scrollHeight", scroll_container)

# 스크롤
while True:
        # 요소 내에서 아래로 3000px 스크롤
        driver.execute_script("arguments[0].scrollTop += 3000;", scroll_container)
        # 페이지 로드를 기다림
        time.sleep(0.5)  # 동적 콘텐츠 로드 시간에 따라 조절
        # 스크롤 높이 계산
        new_height = driver.execute_script("return arguments[0].scrollHeight", scroll_container)
        # 스크롤이 더 이상 늘어나지 않으면 루프 종료
        if new_height == last_height:
            break
        last_height = new_height

# //* = 경로에 관계없이 문서 속의 엘러먼트를 선택  (@ = all)
elemets = driver.find_elements(By.XPATH,'//*[@id="_pcmap_list_scroll_container"]//li')[2:] # 슬라이싱
for index, item in enumerate(elemets, start=1) : 
        # 가게명 .//a = 현재 노드의 a 엘러먼트 자손들을 선택
        restaurant_name = item.find_element(By.CLASS_NAME,'CHC5F').find_element(By.XPATH, ".//a/div/div/span").text
        detail_info_ele = item.find_element(By.CLASS_NAME,'CHC5F').find_element(By.CLASS_NAME, "Dr_06").find_element(By.CLASS_NAME, "MVx6e") 
        
        # 영업 여부
        try :
            isOpen = detail_info_ele.find_element(By.CSS_SELECTOR, '.MqNOY').text
        except :
            isOpen = "없음"
        # 별점 
        try :
            rating = detail_info_ele.find_element(By.CSS_SELECTOR, '.orXYY').text.replace("별점","").strip()
        except :
            rating = "없음"
        # 리부 
        try :
            reviews = detail_info_ele.find_element(By.CSS_SELECTOR, '.orXYY').text.replace("별점","").strip()
        except :
            reviews = "없음"
        print(index, ". ", restaurant_name, "\n 영업 정보 : ", isOpen, "\n 별점 : ", rating)
print("총 식당 수 : ", len(elemets), "개")

# 드라이버 종료
driver.quit()