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
        data: {movie_title_give: movie_title}, //여기부분은 post할떄 사용
        success: function (response) {
            let reviews = response['result'];

            for (let i = 0; i < reviews.length; i++) {

                let title = reviews[i]['title']
                let username = reviews[i]['username']
                let like = reviews[i]['like']
                let time = reviews[i]['time']
                let review_comment = reviews[i]['review_comment']


                let temp_html =`<article class="media review-board posted-review">
                                    <figure class="media-left">
                                        <img class="posted-review-img" src="https://image.flaticon.com/icons/png/512/1179/1179069.png">
                                            </figure>
                                                <div class="media-content">
                                                <div class="content">
                                            <p>
                                                <strong>사용자 : ${username}</strong> <small>${time}</small> <small>평점</small>
                                                
                                                <button onclick="delete_review('${username}', '${time}' ,'${title}' )" type="button" class="delete-button">
                                                    <img src="data:image/png;base64,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">
                                                </button>
           
                                                <br>
                                                ${review_comment}
                                                <br>
                                                <small><button onclick="like_review('${username}', '${time}' ,'${title}' )" type="button" class="like-button">
                                                    <img src="https://about.fb.com/ko/wp-content/uploads/sites/16/2014/07/likebutton.png?w=1200">
                                                </button><a>Like ${like}</a>
                                            </p>
                                        </div>
                                    </div>
                                </article>`

                $('#posted-review-wrap').append(temp_html)
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
function Rating() {
};
Rating.prototype.rate = 0;
Rating.prototype.setRate = function (newrate) {

    this.rate = newrate;
    let items = document.querySelectorAll('.rate_radio')
    items.forEach(function (item, idx) {
        if (idx < newrate) {
            item.checked = true;
        } else {
            item.checked = false;
        }
    });
}
let rating = new Rating();

document.addEventListener('DOMContentLoaded', function () {
    //별점선택 이벤트 리스너
    document.querySelector('.rating').addEventListener('click', function (e) {
        let elem = e.target;
        if (elem.classList.contains('rate_radio')) {
            rating.setRate(parseInt(elem.value));
        }
    })
});

function logout(){
        $.removeCookie('mytoken');
        alert('로그아웃!')
        window.location.href='/login'
      }
