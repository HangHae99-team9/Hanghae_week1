import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.team9TestOne

# 여기 테스트
# 발매일 코드 데이터베이스에 저장하는 코드 따로만들기
movie_list = list(db.movies.find({}, {'_id': False}))

big_list = []
for movie in movie_list:
    title = movie['title']
    url = movie['url']
    url = url.replace('basic', 'detail')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    # detail url을 통해서 영화배우들 리스트를 가져온다 !! 꼭 detail url 아니여도 가능 코드복사때문에 이렇게된것입니다.
    releases = soup.select('#content > div.article > div.wide_info_area > div.mv_info > p > span:nth-child(4) > a')
    # content > div.article > div.wide_info_area > div.mv_info > p > span:nth-child(4) 4번이 개봉일
    release_list = []
    for release in releases:
        release_list.append(release.text)

    big_list.append(release_list)

# 데이터베이스에저장보다는 UPDATE 왜냐면 이코드를 한번에 크롤링해서 처리를 못해서 UPDATE를 한것이다
movies = list(db.movies.find({}, {'_id': False}))

for idx, movie in enumerate(movies):
    title = movie['title']

    # 저장되기전 ['2021' , '.05.26'] 이코드 처리해서 넣기
    dispose = big_list[idx]

    year = dispose[0]
    month_day = dispose[1]

    year_month_day = year+month_day
    big_list[idx] = year_month_day

    db.movies.update_one({'title': title}, {'$set': {'release': big_list[idx]}})
