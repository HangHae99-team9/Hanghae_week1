$(document).ready(function () {

    let queryString = $(location).attr('search')
    let decodetitle = decodeURI(queryString)
    let title = decodetitle.substring(7)
    showMovie(title);
    review_show(title);

});

// 리뷰맨위 poster보여주기
function showMovie(title) {
    $.ajax({
        type: "GET",
        url: "/reviews/poster",
        data: {title_give: title}, //여기부분은 post할떄 사용
        success: function (response) {
            let img_url = response['result']['img_url']
            let age = response['result']['age']
            let title = response['result']['title']
            let genre = response['result']['genre']
            let time = response['result']['time']
            let release = response['result']['release']
            let director = response['result']['director']
            let actor = response['result']['actor_list'][0]


            let temp_html = `<div class="image_wrap">
        <img class="reviews_movie_image"
                src="${img_url}"
                alt="영화이미지">
    </div>
    <div class="movie-information-wrap">
        <dt class="tit">
            <span class="ico_rating_12">${age}</span>
            <a class="poster-title" href="/movie/bi/mi/basic.nhn?code=187322">${title}</a>
        </dt>
        <div>
            <div class="info_txt1">
                <div class="tit_t1">개요</div>
                <div>
							<span class="link_txt">
									<span>${genre}</span>
							</span>
                    <span class="split">|</span>
                    ${time}
                    <span class="split">|</span>
                    ${release}
                </div>
                <dt class="movie_director">감독 <span>| ${director}</span></dt>

                <dt class="move_actor">출연 <span>| ${actor} </span></dt>

            </div>
        </div>
    </div>`

            $('#movie-information').append(temp_html);

        }
    })
}

// 리뷰 저장하기
function review_save() {
    let review_comment = $('.textarea').val();
    let movie_title = $('.poster-title').text();

    $.ajax({
        type: "POST",
        url: "/reviews/save",
        data: {review_comment_give: review_comment, movie_title_give: movie_title}, //여기부분은 post할떄 사용
        success: function (response) {
            console.log(response);
            window.location.reload();
        }
    })
}
// 모든 리뷰 다 가져오기
function review_show(title) {

    let movie_title = title;

    $.ajax({
        type: "GET",
        url: "/reviews/show",
        data: {movie_title_give: movie_title},
        success: function (response) {
            let reviews = response['result'];

            for (let i = 0; i < reviews.length; i++) {

                let title = reviews[i]['title']
                let username = reviews[i]['username']
                let like = reviews[i]['like']
                let time = reviews[i]['time']
                let review_comment = reviews[i]['review_comment']


                let temp_html = `<figure class="media-left">
                                    <p class="image is-64x64">
                                        <img src="">
                                    </p>
                                </figure>
                                <div class="media-content">
                                    <div class="content">
                                        <p>
                                            <strong>사용자${username}</strong> <small>날짜${time}</small> <small>평점</small>
                                            <button onclick="delete_review('${username}', '${time}' ,'${title}', '${review_comment}' )" type="button" class="delete is-medium delete-button"></button>
                                            <button onclick="like_review('${username}', '${time}' ,'${title}', '${review_comment}' )" type="button" class="delete is-medium delete-button"></button>
       
                                            <br>
                                            ${review_comment}
                                            <br>
                                            <small><a>Like ${like}</a> · <a>Reply</a> · 3 hrs</small>
                                        </p>
                                    </div>
                                </div>`

                $('#article_wrap').append(temp_html)
            }
        }
    })
}

// 리뷰 삭제
function delete_review(username, time, title, comment) {
    console.log('삭제',username, time, title, comment)

    $.ajax({
        type: "POST",
        url: "/reviews/delete",
        data: {username_give: username, title_give: title, time_give: time, comment_give: comment}, //여기부분은 post할떄 사용
        success: function (response) {
            console.log(response)
            alert(response['msg'])
            window.location.reload();
        }
    })
}
// 리뷰 좋아요
function like_review(username, time, title, comment){
    console.log('좋아요',username, time, title, comment)

    $.ajax({
        type: "POST",
        url: "/reviews/like",
        data: {username_give: username, title_give: title, time_give: time, comment_give: comment}, //여기부분은 post할떄 사용
        success: function (response) {
            console.log(response)
            alert(response['msg'])
            window.location.reload();
        }
    })
}

function logout(){
        $.removeCookie('mytoken');
        alert('로그아웃!')
        window.location.href='/login'
      }