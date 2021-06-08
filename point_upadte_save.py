import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.team9TestOne

# 네티즌 포인트로 업데이트할려고 만든코드
def update_point():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get('https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=cur&date=20210606', headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    trs = soup.select('#old_content > table > tbody > tr')

    point_list = []
    for tr in trs:
        a = tr.select_one('td.title > div > a')
        if a is not None:
            point = tr.select_one('td.point').text
            point_list.append(point)

    # 포인트값만 이제 가져와서 하면된다.
    movies = list(db.movies.find({}, {'_id': False}))
    for idx, movie in enumerate(movies):
        title = movie['title']
        db.movies.update_one({'title': title}, {'$set': {'point': point_list[idx]}})

update_point()