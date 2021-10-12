const EB_URL='http://pythonapp-env.eba-pxmvppwj.ap-northeast-2.elasticbeanstalk.com'

function wish_list() {
    $.ajax({
        type: "GET",
        url: `${EB_URL}/wish`,
        data: {},
        success: function (response) {
            let wishes = response['wish_list']
            console.log(wishes)

            for (let i = 0; i < wishes.length; i++) {
                let title = wishes[i]['title']
                let category = wishes[i]['category']
                let time = wishes[i]['time']
                let agree = wishes[i]['agree']

                console.log(title, category, agree)

                let temp_html = `<tr>
                                    <th scope="row">${category}</th>
                                    <td>${title}</td>
                                    <td>${time}</td>
                                    <td>${agree}명</td>
                                </tr>`

                $('#wish_tr').append(temp_html)

            }
        }
    })
}

function post_wish() {
    let title = $('#wish_title').val()
    let category = $('#category').val()
    let contents = $('#contents').val()

    console.log(title, category, contents)

    $.ajax({
        type: "POST",
        url: `${EB_URL}/wish`,
        data: {title_give: title, category_give: category, contents_give: contents},
        success: function (response) {
            alert(response['msg'])
            window.location.reload()
        }
    })
}