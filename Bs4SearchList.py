from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
# expected_conditions (EC): Selenium에서 제공하는 여러 가지 조건을 정의한 모듈
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import sys
import time

options = Options()
# 차단 방지 user-agent 설정
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
# 화면 크게
options.add_argument("--start-maximized")
 # 자동종료 방지
options.add_experimental_option("detach", True)

# run webdriver
driver = webdriver.Chrome(options=options)
# 전주역 테스트 좌표
keyword = "돈카츠"
cx = "127.161762930"
cy = "35.849829071"
# 데이터 입력 받기
# index 0: file path
# keyword = sys.argv[1:]
# cx = sys.argc[2:]
# cy = sys.argc[3:]
# print("params :", keyword, cx, cy)
URL = f"https://pcmap.place.naver.com/restaurant/list?query={keyword}&x={cx}&y={cy}"
print("URL :", URL)
# URL = f"https://map.naver.com/restaurant/list?query={keyword}&x=126.97828200000112&y=37.56846119999963&clientX=126.97825&clientY=37.566551"
#https://pcmap.place.naver.com/restaurant/list?query=%EB%8F%88%EC%B9%B4%EC%B8%A0&x=127.161762930&y=35.849829071



driver.get(url = URL)

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

# 검색 결과 창을 html로 추출
results_html = driver.page_source
soup = BeautifulSoup(results_html, 'html.parser')

result_items = soup.find_all('li', class_='rTjJo')

for index, item in enumerate(result_items, start=1):
        # 가게명
        restaurant_name = item.find('span', class_="TYaxT")
     
        # 영업 여부
        try :
            isOpen = item.find('span', class_="MqNOY").get_text()
        except :
            isOpen = "null"
        
        # 별점 
        try :
            rating_value = item.find('span', class_="orXYY").get_text().replace("별점","").strip()
        except :
            rating_value = "null"
             
        # 리뷰
        reviews_ele = item.find('div', class_="MVx6e")
        for item in reviews_ele:
            if len(item['class']) == 1:
                print(item.get_text().replace("리뷰","").strip())
                reviews_value = item.get_text().replace("리뷰","").strip()
        
        print(index, ".", restaurant_name.get_text(), "\n 영업여부 :", isOpen, "\n 별점 :", rating_value, "\n 리뷰 수 : "+reviews_value)

# 드라이버 종료
driver.quit()