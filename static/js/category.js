
function get_categorized_laws(category) {
    $('#law-card-box').empty()
    $.ajax({
        type: "GET",
        contentType: "application/x-www-form-urlencoded; charset=UTF-8",
        url: `/api/category?query=${category}`,
        success: function(res) {

            for (let i=0;i<res.length;i++) {

                let tmp_html = `<div class="column img1 toaster is-one-quarter">
                                    <p>${res[i].title}</p>
                                    <p>대표발의자: ${res[i].proposer_name}</p>
                                    <p>${res[i].date}</p>
                                    <p><a href="${res[i].url}">상세정보</a></p>
                                </div>`
                $('#law-card-box').append(tmp_html)
            }
        }
    })
}