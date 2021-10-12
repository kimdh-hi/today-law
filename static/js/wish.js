
function wish_list() {
    $.ajax({
        type: "GET",
        url: `http://pythonapp-env.eba-pxmvppwj.ap-northeast-2.elasticbeanstalk.com/wish`,
        data: {},
        success: function (response) {
            let wishes = response['wish_list']
            for (let i = 0; i < wishes.length; i++) {
                let title = wishes[i]['title']
                let category = wishes[i]['category']
                let time = wishes[i]['time']
                let agree = wishes[i]['agree']

                let temp_html = `<tr>
                                    <th scope="row">${category}</th>
                                    <td onclick="open_modal_wish('${title}','${category}','${time}','${agree}', '${contents}')">${title}</td>
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
    let contents = $('#contents').val().replace(/\n/g, '<br>')

    console.log(title, category, contents)

    $.ajax({
        type: "POST",
        url: `http://pythonapp-env.eba-pxmvppwj.ap-northeast-2.elasticbeanstalk.com/wish`,
        data: {title_give: title, category_give: category, contents_give: contents},
        success: function (response) {
            alert(response['msg'])
            window.location.reload()
        }
    })
}

function open_modal_wish(title, category, time, agree, contents) {

    $.ajax({
        type: "POST",
        url: "http://pythonapp-env.eba-pxmvppwj.ap-northeast-2.elasticbeanstalk.com/wish/details",
        data: {
            title_give: title,
            category_give: category,
            time_give: time,
            agree_give: agree,
            contents_give: contents
        },
        success: function () {
            content = contents.replaceAll("<br>", "\r\n")
            let temp_html = `<div class="modal is-active">
                                <div class="modal-background" onclick="close_modal()"></div>
                                <div class="modal-content">
                                        <div class="card-content" style="text-align: center">
                                            <div class="media">
                                                <div class="media-content">
                                                    <p class="title is-5">${title}</p>
                                                    <p>참여인원 : ${agree}명</p>
                                                    <div class="petitionsView_info">
                                                        <ul class="petitionsView_info_list">
                                                            <li><p>카테고리</p> ${category}</li>
                                                            <li><p>청원시작</p> ${time} </li>
                                                        </ul>
                                                    </div>
                                                    
                                                </div>
                                            </div>
                                            <hr>
                                            <div class="content">
                                                <span id="subtitle_1" style="text-align: left; font-size: 1.5em; font-weight: bold" >청원내용</span>
                                                <br>
                                                <textarea  readonly style="margin-top: 2em;  resize: none; height: 25em" class="textarea" placeholder="Info textarea">${content}</textarea>                                       
                                            </div>
                                            <footer class="footer_wish">
                                                <span id="subtitle_1" style="text-align: left; font-size: 1.5em; font-weight: bold" >청원동의 ${agree}명</span>
                                                <br>
                                                <div style="margin-top: 2em">
                                                    <textarea id="contents" class="form-control" rows="1" placeholder="동의합니다" style="float:left; width: 91%;"></textarea>
                                                    <button onclick="post_comment('${title}')" type="button" class="btn btn-primary" style="float:left;">동의</button>
                                                </div>
                                            </footer>
                                        </div>

                                </div>
                                <button class="modal-close is-large" aria-label="close" onclick="close_modal()"></button>
                            </div>`
            $('body').append(temp_html)
        }
    })
}

function post_comment(title) {
    $.ajax({
        type: "POST",
        url: "http://pythonapp-env.eba-pxmvppwj.ap-northeast-2.elasticbeanstalk.com/wish/comment",
        data: {
            title_give: title
        },
        success: function (response) {
            alert(response['msg'])
            window.location.reload()
        }
    })
}

