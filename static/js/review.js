$(document).ready(function () {

    let queryString = $(location).attr('search')
    let decodetitle = decodeURI(queryString)
    let title = decodetitle.substring(7)
    showMovie(title);

});

function showMovie(title) {
    $.ajax({
        type: "GET",
        url: "/reviews/detail",
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
            <a href="/movie/bi/mi/basic.nhn?code=187322">${title}</a>
        </dt>
        <div>
            <div class="info_txt1">
                <div class="tit_t1">개요</div>
                <div>
							<span class="link_txt">
									<span>${genre}</span>
									<span>범죄</span>
									<span>코미디</span>
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