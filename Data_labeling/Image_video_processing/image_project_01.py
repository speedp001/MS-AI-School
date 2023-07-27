from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from tqdm import tqdm

import time
import os
import urllib, requests
import cv2
import glob



#1. query 선언 / chromedriver 실행
#query = "mango"
#query = "pineapple"
service = Service("./data/chromedriver")
driver = webdriver.Chrome(service=service)

#로딩 대기를 위하여 driver 3초 대기
driver.implicitly_wait(3)
    
#query 검색창 추가
#query 검색창 추가
driver.get("https://www.google.co.kr/imghp?hl=ko")
keyword = driver.find_element_by_xpath("/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/textarea")
keyword.send_keys(query)
driver.implicitly_wait(3)

#검색 실행
driver.find_element_by_xpath("/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/button").click()
driver.implicitly_wait(3)
    
#스크롤 자동으로 내리기 / 더보기 버튼 클릭
print(f"{query}스크롤 내리는 중...")
#스크롤 동작을 위해 body정보를 elem에 담아준다
elem = driver.find_element_by_tag_name('body')

for i in range(60) :
    #스크롤 진행
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.1)
    
try :
    #더보기 버튼 클릭(class_name값으로 인식)
    driver.find_element_by_class_name('mye4qd').send_keys(Keys.ENTER)
    for i in range(60):
        #더보기 클릭 후 스크롤 진행
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.1)
except :
    pass

    try :
        #더보기 버튼 클릭(class_name값으로 인식)
        driver.find_element_by_class_name('mye4qd').send_keys(Keys.ENTER)
        for i in range(60):
            #더보기 클릭 후 스크롤 진행
            elem.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.1)
    except :
        pass
    
#검색된 이미지 저장 장소
links = []
#css_selector를 이용하여 이미지태그로 이미지 요소 찾기
images = driver.find_elements_by_css_selector('img.rg_i')
for image in images :
    #이미지 요소 안에 있는 src에는 url정보가 들어있다.
    #보통 src안에 있지만 이외에도 data-scr, data-iurl에도 들어있다.
    
    if image.get_attribute('src') != None :
        links.append(image.get_attribute('src'))
    elif image.get_attribute('data-scr') != None :
        links.append(image.get_attribute('data-scr'))
    elif image.get_attribute('data-iurl') != None :
        links.append(image.get_attribute('data-iurl'))
    
print("찾은 이미지 개수 : ", len(links))
time.sleep(1)

count = 0
for i in links :
    start = time.time()
    url = i
    os.makedirs(f"./data/fruit_data/{query}_img_download/", exist_ok=True)
    while True :
        try :
            urllib.request.urlretrieve(url, f"./data/fruit_data/{query}_img_download/{str(count)}_{query}.png")
            print(f"{str(count)} / {str(len(links))} / {query} / 다운로드 시간 : {str(time.time() - start)} 초")
            break
        except urllib.error.HTTPError as e :
            print(f"HTTPError 발생 {e} : 재시동 중...")
            time.sleep(5)
        except Exception as e :
            print(f"Error 발생 {e} : 재시동 중...")
            time.sleep(5)
            
        if time.time() - start > 60 :
            print(f"{query} 이미지 다운로드 실패")
            break
    count = count + 1

print(f"{query} 다운로드 완료")
driver.close()
