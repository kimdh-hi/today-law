
function get_categorized_laws(category) {
    $('#law-card-box').empty()
    $.ajax({
        type: "GET",
        contentType: "application/x-www-form-urlencoded; charset=UTF-8",
        url: `/api/category?category=${category}`,
        success: function(res) {

            for (let i=0;i<res.length;i++) {

                let tmp_html = `<div class="column img1 toaster is-one-quarter">
                                    <p>${res[i].title}</p>
                                </div>`
                $('#law-card-box').append(tmp_html)
            }
        }
    })
}