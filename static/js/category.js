function get_categorized_laws(category) {
    $('#law-card-box').empty()
    $.ajax({
        type: "GET",
        contentType: "application/x-www-form-urlencoded; charset=UTF-8",
        url: `/api/category?query=${category}`,
        success: function(res) {

            for (let i=0;i<res.length;i++) {

                let tmp_html = `<div class="column img1 toaster is-one-fifth" style="border-radius: 30px;">
                                    <p id="category-title" onclick="open_modal('${res[i].url}', '${res[i].id}', '${res[i].title}','${res[i].proposer_name}', '${res[i].proposer_names}')" class="category-title">${res[i].title}</p>
                                    <p id="category-proposer" class="category-subtitle"">대표발의자: ${res[i].proposer_name}</p>
                                    <p id="category-date" class="category-subtitle">${res[i].date}</p>
                                    <p><a href="${res[i].url}" style="font-size: 0.8em">상세정보</a></p>
                                </div>`
                $('#law-card-box').append(tmp_html)
            }
        }
    })
}