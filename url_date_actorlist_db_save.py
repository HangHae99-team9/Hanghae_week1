import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.team9TestOne


# 모든 영화 url을 가져온다 -> 그다음 url을 detail url로 변경한다
# actorlist 저장 코드
movie_list = list(db.movies.find({}, {'_id': False}))
for movie in movie_list:
    title = movie['title']
    url = movie['url']
    url = url.replace('basic', 'detail')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    # detail url을 통해서 영화배우들 리스트를 가져온다
    actor_list = soup.select('#content > div.article > div.section_group.section_group_frst > div.obj_section.noline > div > div.lst_people_area.height100 > ul > li')

    ac_second_list = []
    for actor in actor_list:
        ac = actor.select_one(' div.p_info > a').text
        ac_second_list.append(ac)

    db.movies.update_one({'title': title}, {'$set': {'actor_list': ac_second_list}})