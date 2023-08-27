#pip install selenium==4.2.0

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

import time
import os
import urllib, requests



#크롤링 검색 함수
def goolge_crawling(query) :
    
    #chromedriver를 이용한 Service객체를 service에 담기
    service = Service("/Users/sang-yun/Desktop/Jupyter/Dataset_construction/06_data_collection/chromedriver")
    
    #service 객체로 webdriver 실행
    driver = webdriver.Chrome(service=service)
    
    # options = Options()
    # options.add_argument('--disable-popup-blocking')
    # driver = webdriver.Chrome(options=options)
    
    #로딩 대기를 위하여 driver 3초 대기
    driver.implicitly_wait(3)
    
    #query 검색창 추가
    driver.get("https://www.google.co.kr/imghp?h1=ko")
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
        time.sleep(0.3)

    try :
        #더보기 버튼 클릭(class_name값으로 인식)
        driver.find_element_by_class_name('mye4qd').send_keys(Keys.ENTER)
        for i in range(60):
            #더보기 클릭 후 스크롤 진행
            elem.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.3)
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
    return links[:]
    
    
    
#검색한 이미지 저장 함수
def img_download(links) :
    
    #이미지 다운로드
    count = 0
    for i in links :
        start = time.time()
        url = i
        os.makedirs(f"./Dataset_construction/data/{query}_img_download/", exist_ok=True)
        while True :
            try :
                urllib.request.urlretrieve(url, f"./Dataset_construction/data/{query}_img_download/{str(count)}_{query}.png")
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
    
    print("다운로드 완료")
    
    

#사용자 인터페이스
while True :
    
    search = int(input("검색을 진행하시겠습니까?(yes : 1, no : 2)"))

    if search == 1 :
        query = input("Input your search word : ")
        link = goolge_crawling(query)
        
        #이미지 다운로드
        download = int(input("해당 검색 이미지를 다운로드 하시겠습니까?(yes : 1, no : 2)"))
        if download == 1 :
            img_download(link)
            
        else :
            continue
            
    elif search==2 :
        print("크롤링을 종료합니다.")
        exit()
        
    else :
        print("1, 2번 중에 선택해주세요")
