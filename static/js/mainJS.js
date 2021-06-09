$(document).ready(function () {

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
                let title = movies[i]['title']
                let point = movies[i]['point']

                let temp_html = `<div class="card" onclick="window.location.href = '/reviews?title=${title}'">
                                    <div class="card-image">
                                        <figure class="image is-3by4">
                                            <img alt="Placeholder image" src="${image_url}">
                                        </figure>
                                    </div>
                                    <div class="card-content">
                                        <div class="media">
                                            <div class="media-content">
                                                <p class="title is-4">${title}</p>
                                            </div>
                                        </div>
                                        <div class="content">
                                            ${point}
                                        </div>
                                    </div>
                                </div>`
                $('.card-columns').append(temp_html)

            }
        }
    })
}