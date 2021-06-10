$(document).ready(function () {
    $('.card-columns').empty();
    showMovies();
});


function showMovies() {
    $.ajax({
        type: "GET",
        url: "/main/movies",
        data: {}, //여기부분은 post할떄 사용
        success: function (response) {
            let movies = response['result']
            for (let i = 0; i < movies.length; i++) {
                let image_url = movies[i]['img_url']

                let age = movies[i]['age'].substring(0,2)
                let age_html = ``;
                if (age == '청소') {
                  age = '청불'
                  age_html = `<div class="bg-text age18">
                                  <p>${age}</p>
                              </div>`
                } else if (age == '15') {
                  age_html = `<div class="bg-text age15">
                                  <p>${age}</p>
                              </div>`
                } else if (age == '12') {
                  age_html = `<div class="bg-text age12">
                                  <p>${age}</p>
                              </div>`
                } else {
                  age_html = `<div class="bg-text ageAll">
                                  <p>${age}</p>
                              </div>`
                };
                let title = movies[i]['title']
                let point = movies[i]['point']
                let release = movies[i]['release'].split('.')

                let temp_html = `<div class="card" onclick="window.location.href = '/reviews?title=${title}'">
                                    <div class="card-image">
                                        <figure class="image is-3by4">
                                            <img alt="Placeholder image" src="${image_url}">
                                        </figure>
                                    </div>
                                    ${age_html}
                                    <div class="card-content">
                                        <div class="media">
                                            <div class="media-content">
                                                <p class="title is-4">${title}</p>
                                            </div>
                                        </div>
                                        <div class="content">
                                            <div>평점 : ${point}</div>
                                            <div>${release[1]}.${release[2]} 개봉</div>
                                        </div>
                                    </div>
                                </div>`
                $('.card-columns').append(temp_html)

            }
        }
    })
}

function logout(){
        $.removeCookie('mytoken');
        alert('로그아웃!')
        window.location.href='/login'
}
