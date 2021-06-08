import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.team9

# DB에 저장할 영화인들의 출처 url을 가져옵니다.
# 진짜 완료
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


# 출처 url로부터 영화인들의 사진, 이름, 최근작 정보를 가져오고 mystar 콜렉션에 저장합니다.
def insert_star(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    title = soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > h3.h_movie > a').text
    img_url = soup.select_one('#content > div.article > div.wide_info_area > div.poster > a > img')['src']
    point = soup.select_one('#content > div.article > div.wide_info_area > div.mv_info > div.main_score > div.score >  #actualPointPersentWide > div > span > span').text
    # age  =    # 연령대
    # director =
    # genre =
    # releaseDay  # 개봉일

    doc = {
        'title': title,
        'img_url': img_url,
        'point': point,
        'url': url,
        'like': 0
    }

    db.movies.insert_one(doc)
    print('완료!', title)


# 기존 mystar 콜렉션을 삭제하고, 출처 url들을 가져온 후, 크롤링하여 DB에 저장합니다.
def insert_all():
    # db.movies.drop()  # mystar 콜렉션을 모두 지워줍니다.
    urls = get_urls()
    for url in urls:
        insert_star(url)


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
    movies = list(db.movies.find({},{'_id':False}))
    for idx,movie in enumerate(movies):
        title = movie['title']
        # print(title, point_list[idx])
        db.movies.update_one({'title': title}, {'$set': {'point': point_list[idx]}})


def actor_save():
    # 이것만 따로 크롤링 코드
    # 모든 영화 url을 가져온다 -> 그다음 url을 detail url로 변경한다
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
        actor_list = soup.select(
            '#content > div.article > div.section_group.section_group_frst > div.obj_section.noline > div > div.lst_people_area.height100 > ul > li')

        ac_second_list = []
        for actor in actor_list:
            ac = actor.select_one(' div.p_info > a').text
            ac_second_list.append(ac)

        db.movies.update_one({'title': title}, {'$set': {'actor_list': ac_second_list}})


insert_all()
update_point()
actor_save()