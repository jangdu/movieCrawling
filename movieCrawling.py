# python을 이용한 크롤링 기초
# 크롤링 할 페이지 'https://movie.naver.com/movie/sdb/rank/rmovie.naver?sel=pnt&date=20210829'
# pip install bs4

# 크롤링 기본 세팅
import requests
from bs4 import BeautifulSoup

# python mongoDb 세팅
from pymongo import MongoClient
import certifi

ca = certifi.where()

client = MongoClient('mongodb+srv://sparta:test@cluster0.gm0wapr.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta


# 타겟 URL을 읽어서 HTML를 받아오고,
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://movie.naver.com/movie/sdb/rank/rmovie.naver?sel=pnt&date=20210829',headers=headers)

# HTML을 BeautifulSoup(bs4)이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
# soup이라는 변수에 "파싱 용이해진 html"이 담긴 상태가 됨
# 이제 코딩을 통해 필요한 부분을 추출하면 된다.
soup = BeautifulSoup(data.text, 'html.parser')

# select이용해서 tr들 불러오기
trs = soup.select('#old_content > table > tbody > tr')
#old_content > table > tbody > tr:nth-child(3) > td:nth-child(1)
#old_content > table > tbody > tr:nth-child(2) > td:nth-child(1) > img
#old_content > table > tbody > tr:nth-child(2) > td.point
#old_content > table > tbody
# movies의 반복문
for tr in trs:
  # movie안에 a가 있으면?
  a = tr.select_one('td.title > div > a')
  
  if a is not None:
    ac = tr.select_one('td:nth-child(1) > img')['alt']
    point = tr.select_one('td.point')
    print (ac, a.text, point.text)
    doc = {
      'title': a.text,
      'rank': ac,
      'star': point.text
    }
    db.movies.insert_one(doc)