from flask import Flask, render_template, jsonify, request, session, redirect, url_for

app = Flask(__name__)

from pymongo import MongoClient

# ,username="test", password="test" 이코드 일단안넣음
client = MongoClient('mongodb://localhost', 27017)
db = client.team9TestOne

# JWT 토큰을 만들 때 필요한 비밀문자열입니다. 아무거나 입력해도 괜찮습니다.
# 이 문자열은 서버만 알고있기 때문에, 내 서버에서만 토큰을 인코딩(=만들기)/디코딩(=풀기) 할 수 있습니다.
SECRET_KEY = 'SPARTA'

# JWT 패키지를 사용합니다. (설치해야할 패키지 이름: PyJWT)
import jwt

# 토큰에 만료시간을 줘야하기 때문에, datetime 모듈도 사용합니다.
import datetime

# 회원가입 시엔, 비밀번호를 암호화하여 DB에 저장해두는 게 좋습니다.
# 그렇지 않으면, 개발자(=나)가 회원들의 비밀번호를 볼 수 있으니까요.^^;
import hashlib

import requests

# 메소드 부분
def nowTime():
    now_time = datetime.datetime.now()
    now_time = str(now_time)
    return now_time[:16]


##  HTML을 주는 부분             ##
@app.route('/')
def home():
    msg = request.args.get("msg")
    r = requests.get(
        'http://kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json?key=f02f0047514de8f2bca5b5c23374ee21&targetDt=20210601')
    response = r.json()
    weeklys = response['boxOfficeResult']['weeklyBoxOfficeList']

    token_receive = request.cookies.get('mytoken')

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload['id']})
        return render_template('main.html', user_info=user_info, weeklys=weeklys, msg=msg)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


@app.route('/main/movies', methods=['GET'])
def main_movie_get():
    movie_list = list(db.movies.find({}, {'_id': False}))
    return jsonify({'result': movie_list})

# reviews 페이지
@app.route('/reviews')
def review_page():
    return render_template("reviews.html")

@app.route('/reviews/detail', methods=['GET'])
def review_get_detail():
   title_receive = request.args.get('title_give')
   movie = db.movies.find_one({'title': title_receive}, {'_id':False})

   return jsonify({'result': movie})



#################################
##  로그인을 위한 API            ##
#################################


# 회원가입및 로그인 API  경계선

# 회원가입에서 아이디 중복확인 서버
@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"username": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})

# 회원가입
@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "username": username_receive,                               # 아이디
        "password": password_hash,                                  # 비밀번호
        "profile_name": username_receive,                           # 프로필 이름 기본값은 아이디
        "profile_pic": "",                                          # 프로필 사진 파일 이름
        "profile_pic_real": "profile_pics/profile_placeholder.png", # 프로필 사진 기본 이미지
        "profile_info": ""                                          # 프로필 한 마디
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})

# 로그인
@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'username': username_receive, 'password': pw_hash})

    if result is not None:
        payload = {
         'id': username_receive,
         'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60 * 2)  # 로그인 24시간 유지 60 * 60 * 24
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

# @app.route('/post', methods=['POST'])
# def posting():
#     token_receive = request.cookies.get('mytoken')
#
#     try:
#         payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
#
#         user_info = db.users.find_one({"username": payload["id"]})
#         review_receive = `request`.form['review_give']
#         store = request.form["store"]
#         now = datetime.now()
#         time = now.strftime('%Y년 %m월 %d일 %H시 %M분')
#         if len(review_receive) < 5:
#             return jsonify({"msg" : "리뷰를 5자이상 달아주세요"})
#         doc = {
#             'review': review_receive,
#             'store': store,
#             'user': user_info,
#             'time': time
#         }
#         db.reviews.insert_one(doc)
#         return jsonify({'msg': '리뷰를 저장했습니다.'})
#
#     except jwt.ExpiredSignatureError:
#         return jsonify({'msg': '로그인 시간이 만료됐습니다.'})
#     except jwt.exceptions.DecodeError:
#         return jsonify({'msg': "로그인 해주세요"})
#



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
