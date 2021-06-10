from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import requests


from pymongo import MongoClient

client = MongoClient('mongodb://test:test@52.78.44.138', 27017)
db = client.team9TestOne


# 영화정보페이지로 가는 url
def get_urls():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get('https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=cur&date=20210606', headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    trs = soup.select('#old_content > table > tbody > tr')
    urls = []

    for tr in trs:
        a = tr.select_one('td.title > div.tit5 > a')
        if a is not None:
            base_url = 'https://movie.naver.com/'
            url = base_url + a['href']
            urls.append(url)
    return urls

# 하나하나 읽어와서 하는곳
def insert_movie(url):
    driver = webdriver.Chrome('./chromedriver')  # 드라이버를 실행합니다.

    # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    # data = requests.get(url, headers=headers)

    driver.get(url)  # 드라이버에 해당 url의 웹페이지를 띄웁니다.
    sleep(5)  # 페이지가 로딩되는 동안 5초 간 기다립니다.

    req = driver.page_source  # html 정보를 가져옵니다.
    driver.quit()  # 정보를 가져왔으므로 드라이버는 꺼줍니다.

    # soup = BeautifulSoup(data.text, 'html.parser')
    summary = BeautifulSoup(req, 'html.parser')  # 가져온 정보를 beautifulsoup으로 파싱해줍니다.

    title = summary.select_one('#content > div.article > div.mv_info_area > div.mv_info > h3.h_movie > a').text
    summarys = summary.select_one("#content > div.article > div.section_group.section_group_frst > div:nth-child(1) > div > div.story_area > p").text

    # db.summarytest.insert_one({'title': title,'summary': summarys})
    db.movies.update_one({'title': title}, {'$set': {'summary': summarys}})
    print(title,'완료.')

def insert_all():
    # db.movies.drop()  # mystar 콜렉션을 모두 지워줍니다.
    urls = get_urls()
    for url in urls:
        insert_movie(url)

insert_all()
# a = list(db.summarytest.find({'title':'크루엘라'},{'_id':False}))
# print(a[0]['summary'])
