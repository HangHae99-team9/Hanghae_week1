$('.starRev span').click(function(){
  $(this).parent().children('span').removeClass('on');
  $(this).addClass('on').prevAll('span').addClass('on');
  return false;
});

function postReviews(){
            let reviews = $("#inputReview").val()
            $.ajax({
                type: "POST",
                url: "/reviews",
                data: {reviews_give: reviews},
                success: function (response) {
                    alert(response["msg"]);
                    window.location.href = "/reviews"
                }
            })
        }

        function addReviews(){
        $.ajax({
            type: "GET",
            url: "/Reviews",
            data: {},
            success: function (response) {
                let add_reviews = response["all_"]
            }
        })
        }