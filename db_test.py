import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.team9Test


# 이것만 따로 크롤링 코드
# 모든 영화 url을 가져온다 -> 그다음 url을 detail url로 변경한다
# 네티즌평점으로 하는코드
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

    # time, age랑 director는 추가된거임 현재까지 이상없음
    time = soup.select_one('#content > div.article > div.wide_info_area > div.mv_info > p > span:nth-child(3)').text
    age = soup.select_one('#content > div.article > div.wide_info_area > div.mv_info > p > span:nth-child(5) > a').text
    director = soup.select_one('#content > div.article > div.wide_info_area > div.mv_info > div.info_spec2 > dl.step1 > dd > a').text

    # genre = db_genre_dispose()
    # releaseDay = db_releaseDay_dispose()
    #

    # content > div.article > div.wide_info_area > div.mv_info > p > span:nth-child(1) 장르는 메서드로 처리
    # content > div.article > div.wide_info_area > div.mv_info > p > span:nth-child(4) 개봉날짜 메서드로 처리
    # content > div.article > div.wide_info_area > div.mv_info > p > span:nth-child(3) 영화길이 ex)2시간짜리 영화
    # content > div.article > div.wide_info_area > div.mv_info > p > span:nth-child(5) 관람연령 12세 관람가

    # doc = {
    #     'title': title,
    #     'img_url': img_url,
    #     'point': point,
    #     'url': url,
    #     'like': 0
    # }
    #
    # db.movies.insert_one(doc)
    # print('완료!', title)


# 기존 mystar 콜렉션을 삭제하고, 출처 url들을 가져온 후, 크롤링하여 DB에 저장합니다.
def insert_all():
    # db.movies.drop()  # mystar 콜렉션을 모두 지워줍니다.
    urls = get_urls()
    for url in urls:
        insert_star(url)


# https://movie.naver.com/movie/bi/mi/detail.nhn?code=187322
# https://movie.naver.com/movie/bi/mi/basic.nhn?code=187322


