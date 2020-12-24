import time
import pyperclip
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import re
import sqlite3
import datetime

hangul = re.compile("[^ a-z A-Z 가-힣]+")

driver = webdriver.Chrome('./chromedriver')
driver.implicitly_wait(3)

board_url = 'https://cafe.naver.com/hyualife/'
#ArticleList.nhn?search.clubid=26209757
#board_url1 = '&search.menuid=227&search.page='
#board_url2 = '&articleid='

driver.get('https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com')
tmp = input("로그인을 한 뒤, 엔터키를 눌러주세요")

start_page = 8566#8566 #처음
end_page = 9392 #최태주씨
all_text = []
for page_number in range(start_page,end_page+1):
    try :
        driver.get(board_url+str(page_number))
        driver.switch_to.frame("cafe_main")
        soup = BeautifulSoup(driver.page_source,"html.parser")
        text = str(soup.text)
        where = text.find("학과/학부를 알려주세요!!")
        where2 = text.find("같은 고향 친구를")
    except:
        continue
    if(where != -1):
        where += 14
        findtext = text[where:where2]
        where = findtext.find("학과")
        if(where == -1) : where = findtext.find("학부")
        if(where == -1) : where = where2-2
        #all_text += findtext[0:where+2] + "\n"
        all_text.append(hangul.sub("",findtext[0:where+2]).strip() +' ' + str(page_number) + "\n")

all_text.sort()
f = open("text.txt","w")
for t in all_text :
    f.write(t)
f.close()