
let is_authenticated = false // 인증된 사용자=true , 인증되지 않은 사용자=false


function modal() {
    $('#edit-preferences-modal').addClass('is-active');

}

function close_modal() {
    $('#edit-preferences-modal').removeClass('is-active');
}

function agree_receive() {
    $.ajax({
        type: "POST",
        url: `/mypage/agree`,
        success: function (res) {
            alert(res['result'])
            location.reload()
        }
    })
}

function edit_profile() {
    let name = $('#profile-name').val()
    let bio = $('#profile-bio').val()
    $.ajax({
        type: "POST",
        url: `/mypage/profile`,
        data: {name_give: name, bio_give: bio},
        success: function (res) {
            if (res['result'] == 'success') {
                alert(res['result'])
                location.reload()
            } else {
                alert('이미 존재하는 닉네임입니다.')
            }
        }
    })
}

$(document).ready(function () {
    show_recently()
    // 현재 요청이 인증되었는지 확인 (매 요청마다 확인하는 것인지 맞는지 잘 모르겠음)
    $.ajax({
        type: "GET",
        url: `/login-check`,
        success: function (res) {
            if (res['result'] == 'success') {
                $('#login_button').addClass("is-hidden")
                $('#logout_button').removeClass("is-hidden")
                $('#bookmark-tab').removeClass("is-hidden")
                $('#btn-post-box').removeClass("is-hidden")
                $('#login_warning').addClass("is-hidden")

                let profile_html = `<div class='modal' id='edit-preferences-modal'>
                                        <div class='modal-background'></div>
                                        <div class='modal-card'>
                                            <header class='modal-card-head'>
                                                <p class='modal-card-title'>프로필 수정</p>
                                                <button onclick="close_modal()" class='delete'></button>
                                            </header>
                                            <section class='modal-card-body'>
                                                <label class='label'>닉네임</label>
                                                <p class='control has-icon has-icon-right'>
                                                    <input id="profile-name" class='input' placeholder='Text input' type='text' value='${res['name']}'>
                                                </p>
                                                <label class='label'>이메일</label>
                                                <p class='control has-icon has-icon-right'>
                                                    <input class='input' placeholder='Email input' type='text' value='${res['email']}' readonly>
<!--                                                    <i class='fa fa-warning'></i>-->
<!--                                                    <span class='help is-danger'>This email is invalid</span>-->
                                                </p>
                            
                                                <label class='label'>자기소개</label>
                                                <p class='control'>
                                                    <textarea id="profile-bio" class='textarea' placeholder='자기 소개를 작성해보세요!'>${res['bio']}</textarea>
                                                </p>
                            
                                            </section>
                                            <footer class='modal-card-foot'>
                                                <a onclick="edit_profile()" class='button is-primary modal-save'>Save changes</a>
                                                <a onclick="close_modal()" class='button modal-cancel'>Cancel</a>
                                            </footer>
                                        </div>
                                    </div>
                                    <div class='section profile-heading'>
                                        <div class='columns is-mobile is-multiline'>
                                            <div class='column is-2'>
                                                <span class='header-icon user-profile-image'>
                                                    <img alt='' src='${res['profile_image']}'>
                                                </span>
                                            </div>
                                            <div class='column is-4-tablet is-10-mobile name'>
                                                <p>
                                                    <span class='title is-bold'> ${res['name']} </span>
                                                    <br>
                                                    <a onclick="modal()" class='button is-primary is-outlined' id='edit-preferences' style='margin: 5px 0'>
                                                        프로필 수정
                                                    </a>
                                                        ${res['receive_mail'] ? `<a onclick="agree_receive()" class='button is-danger is-outlined' id='edit-preferences' style='margin: 5px 0'>
                                                        알림끄기
                                                    </a>` : `<a onclick="agree_receive()" class='button is-primary is-outlined' id='edit-preferences' style='margin: 5px 0'>
                                                        알림받기
                                                    </a>`}
                                                    
                                                    
                                                    <br>
                                                </p>
                                                <p class='tagline'>
                                                    ${res['bio']}         
                                                </p>
                                            </div>
                            
                                        </div>
                                    </div>`
                $('#profile-container').append(profile_html)

                let temp_html = `<div onclick="dpmenu()" class = "dropdown" >
                                    <div class = "dropdown-trigger" >
                                        <button style="padding-left: 0" class = "button" aria-haspopup = "true" aria-controls = "dropdown-menu3" >
                                        <img alt="profile_image" src="${res['profile_image']}">
                                            <span > ${res['name']} </span>
                                            </span>
                                        </button>
                                    </div>
                                    <div class="dropdown-menu" id="dropdown-menu3" role="menu">
                                        <div class="dropdown-content">
                                            <a id="mypage_button" onclick="mypage()" class="dropdown-item">
                                                마이페이지
                                            </a>
                                            <hr class="dropdown-divider">
                                                <a onclick="logout()" class="dropdown-item">
                                                    로그아웃
                                                </a>
                                        </div>
                                    </div>
                                </div>
                                `
                $('#navbar').append(temp_html)


                is_authenticated = true
            } else {
                if ($(location).attr('pathname') == '/mypage') {
                    location.pathname = '/'
                }
                $('#login_button').removeClass("is-hidden")
                $('#logout_button').addClass("is-hidden")
                $('#bookmark-tab').addClass("is-hidden")
                $('#btn-post-box').addClass("is-hidden")
                $('#login_warning').removeClass("is-hidden")
                is_authenticated = false
            }
        }
    })

    //마이페이지 메뉴 전환
    $(".page-list li").click(function () {
        let idx = $("li").index(this);
        $(".page-list li").removeClass("is-active");
        $(".page-list li").eq(idx).addClass("is-active");
        if ($(this).text().includes('작성한 청원')) {
            $.ajax({
                type: "GET",
                url: `/mypage/wishlist`,
                success: function (res) {
                    $("#mypage-contents").empty();
                    $("#mypage-contents").append(`<div class="wishlist">
                                      <table class="table is-responsive">
                                        <thead>
                                          <tr>
                                            <th>카테고리</th>
                                            <th>제목</th>
                                            <th>작성일</th>
                                          </tr>
                                        </thead>
                                        <tbody id="wishList-body">

                                        </tbody>
                                      </table>
                                    </div>`)
                    for (let i=0;i<res.length;i++) {
                        console.log(res[i])
                        let category = res[i]['category_give']
                        let title = res[i]['title_give']
                        let time = res[i]['time_give']
                        let contents = res[i]['contents_give']
                        let agree = res[i]['agree_give']
                        temp_html = `<tr>
                                        <td>${category}</td>
                                        <td onClick="open_modal_wish('${title}','${category}','${time}','${agree}', '${contents}')">
                                            <a>${title}</a></td>
                                        <td>${time}</td>
                                    </tr>`
                        $('#wishList-body').append(temp_html)
                    }
                }

            })
        } else if ($(this).text().includes('좋아요')) {
            $.ajax({
                type: "GET",
                url: `/mypage/likes`,
                success: function (res) {
                    $("#mypage-contents").empty();
                    like_laws = res['like_laws']
                    let temp_html = `<div class='columns is-mobile' style="flex-wrap: wrap">`
                    for (let i = 0; i < like_laws.length; i++) {

                        let id = like_laws[i]['like_law_id']
                        let title = like_laws[i]['title']
                        let content = like_laws[i]['content']
                        let proposer_name = like_laws[i]['proposer_name']
                        let proposer_names = like_laws[i]['proposer_names']
                        let url = like_laws[i]['url']

                        temp_html += `<div class='column is-3-tablet is-6-mobile'>
                                        <div class='card'>
                                            <p class="card-header-title">${title}</p>
                                            <div class='card-content'>
                                                <div class='content'>
                                                    <p>${content}</p>
                                                </div>
                                                </div>
                                            <footer class='card-footer'>
                                                <a onclick="open_modal('${url}', '${id}', '${title}', '${proposer_name}', '${proposer_names}')" class='card-footer-item'>보기</a>
                                            </footer>
                                        </div>
                                        <br>
                                        </div>`
                    }
                    $("#mypage-contents").append(temp_html + `</div>`)
                }
            })
        } else if ($(this).text().includes('최근')) {
            show_recently()
        }

    })

})

function show_recently() {
    $.ajax({
        type: "GET",
        url: `/mypage/recently_view`,
        success: function (res) {
            $("#mypage-contents").empty();
            let temp_html = `<div class='columns is-mobile' style="flex-wrap: wrap">`
            for (let i = res['recently_list']['recently_view'].length - 1; i >= 0; i--) {
                let title = res['recently_list']['recently_view'][i]['title']
                let content = res['recently_list']['recently_view'][i]['content'].slice(0, 87) + '...'
                let urls = res['recently_list']['recently_view'][i]['url']
                let id = res['recently_list']['recently_view'][i]['recently_view_id']
                let proposer_name = res['recently_list']['recently_view'][i]['proposer_name']
                let proposer_names = res['recently_list']['recently_view'][i]['proposer_names']

                temp_html += `<div class='column is-3-tablet is-6-mobile'>
                                    <div class='card'>
                                        <p class="card-header-title">${title}</p>
                                        <div class='card-content'>
                                            <div class='content'>
                                                <p>${content}</p>
                                            </div>
                                        </div>
                                        <footer class='card-footer'>
                                            <a onclick="open_modal('${urls}', '${id}', '${title}', '${proposer_name}', '${proposer_names}')" class='card-footer-item'>보기</a>
                                        </footer>
                                    </div>
                
                                    <br>
                                </div>`
            }
            $('#mypage-contents').append(temp_html + `</div>`)
        }
    })
}

function dpmenu() {
    if ($(".dropdown").hasClass("is-active")) {
        $(".dropdown").removeClass("is-active")
    } else {
        $(".dropdown").addClass("is-active")
    }
}

function close_modal() {
    $(".modal").removeClass("is-active");
}

function close_modal2() {
    $(".modal").removeClass("is-active");
    //모달을 비워주지 않으면 두번째 창부터 좋아요 버튼이 생기지 않음
    $(".modal").empty();
}

function open_modal(url, id, title, proposer_name, proposer_names) {
    $.ajax({
        type: "POST",
        url: '/api/laws/details',
        data: {
            url_give: url,
            id_give: id,
            title_give: title,
            proposer_name_give: proposer_name,
            proposer_names_give: proposer_names
        },
        success: function (response) {
            let id = response['id']
            let title = response['title'].split('(')[0]
            let proposer_name = response['proposer_name']
            let proposer_names = response['proposer_names']
            let content = response['content']
            let date = response['date']
            let like = response['like']
            let hate = response['hate']
            let subtitle = ''
            let subtitle2 = ''
            let content2 = ''
            let content3 = ''
            if (content.includes("제안이유 및 주요내용")) {
                subtitle = '제안이유 및 주요내용'
                content2 = content.split('주요내용')[1]
            } else if (content.includes("제안이유")) {
                content2 = content.split('제안이유')[1].split('주요내용')[0]
                content3 = content.split('주요내용')[1]
                subtitle = '제안이유'
                subtitle2 = '주요내용'
            } else {
                content2 = content
            }


            let temp_html = `<div class="modal is-active">
                                <div class="modal-background" onclick="close_modal2()"></div>
                                <div class="modal-content">

                                        <div class="card-content" style="text-align: center">
                                            <div class="media">
                                                <div class="media-content">
                                                    <p class="title is-5">${title}</p>
                                                    <time style="font-size: 1em" datetime="2016-1-1">${date}</time>
                                                    <p class="subtitle is-6" style="margin: auto; color: black;">대표발의자: ${proposer_name} 의원</p>
                                                    <p>공동발의자: ${proposer_names}</p>
                                                    <div id="bookmark-box">
                                                        <button id="btn-save" class="btn btn-outline-sparta btn-lg" 
                                                            onclick="bookmark('${id}', '${title}', '${proposer_name}', '${proposer_names}', '${url}', '${date}')">
                                                                <i class="fa fa-bookmark-o" aria-hidden="true"></i>
                                                        </button>
                                                        <button id="btn-delete" class="btn btn-sparta btn-lg" onclick="delete_bookmark('${id}')">
                                                                 <i class="fa fa-trash-o" aria-hidden="true"></i>
                                                        </button>
                                                    </div>
                                                </div>
                                            </div>
                                            <hr>
                                            <div class="content">
                                                <span id="subtitle_1" style="text-align: left; font-size: 1.5em; font-weight: bold" >${subtitle}</span>
                                                <br>
                                                <textarea readonly style="margin-top: 2em;  resize: none; height: 25em" class="textarea" placeholder="Info textarea">${content2}</textarea>
                                                <br>
                                                ${subtitle2 ? `<hr>
                                                <br>
                                                <span id="subtitle_2" style="text-align: left; font-size: 1.5em; font-weight: bold" >${subtitle2}</span>
                                                <br>
                                                <textarea readonly style="margin-top: 2em;  resize: none; height: 25em" class="textarea" placeholder="Info textarea">${content3}</textarea>
                                                <br>` : ``}


                                            </div>
                                            
                                            <footer class="card-footer" id="card-footer">
                                                
                                            </footer>

                                        </div>
                                </div>
                                <button class="modal-close is-large" aria-label="close" onclick="close_modal2()"></button>
                            </div>`
            $('body').append(temp_html)

            add_like_hate_button(id, like, hate, title, content2, proposer_name, proposer_names, url)


            // 인증된 사용자에게만 즐겨찾기, 좋아요/싫어요 버튼을 보이도록 처리
            if (is_authenticated == false) {
                $('#bookmark-box').addClass("is-hidden")
                $('#card-footer').addClass("is-hidden")
            } else {
                $('#bookmark-box').removeClass("is-hidden")
                $('#card-footer').removeClass("is-hidden")
            }
        }
    })
}

function likeLaw(id, title, content, proposer_name, proposer_names, url) {
    $.ajax({
        type: 'POST',
        url: `/api/like`,
        data: {
            id_give: id,
            title_give: title,
            content_give: content,
            proposer_name_give: proposer_name,
            proposer_names_give: proposer_names,
            url_give: url
        },
        success: function (response) {
            add_like_hate_button(
                response.id, response.like, response.hate, response.title, response.proposer_name, response.proposer_names, response.url
            )
            window.location.reload();
        }
    })
}

//싫어요 기능
function hateLaw(id, title, content, proposer_name, proposer_names, url) {
    let data = {
            id_give: id,
            title_give: title,
            content_give: content,
            proposer_name_give: proposer_name,
            proposer_names_give: proposer_names,
            url_give: url
    }

    $.ajax({
        type: 'POST',
        url: `/api/hate`,
        data: data,
        success: function (response) {
            add_like_hate_button(
                response.id, response.like, response.hate, response.title, response.proposer_name, response.proposer_names, response.url
            )
            window.location.reload();
        }
    });
}

// 좋아요 싫어요 버튼 추가
function add_like_hate_button(id, like, hate, title, content, proposer_name, proposer_names, url) {
    $('#card-footer').empty()

    content = content.replaceAll("\"","").replaceAll("\'","").replaceAll(".","").replaceAll("\n","")
    content = $.trim(content);

    let tmp_html = `<a href="#" onClick="likeLaw('${id}', '${title}', '${content}', '${proposer_name}', '${proposer_names}', '${url}')" class="card-footer-item has-text-info">
                        좋아요 ${like}명 <i class="fa fa-thumbs-up" aria-hidden="true"></i>
                    </a>
                    <a href="#" onClick="hateLaw('${id}', '${title}', '${content}', '${proposer_name}', '${proposer_names}', '${url}')" class="card-footer-item has-text-danger">
                        싫어요 ${hate}명 <i class="fa fa-thumbs-down" aria-hidden="true"></i>
                    </a>`
    $('#card-footer').append(tmp_html)
}

function bookmark(id, title, proposer_name, proposer_names, url, date) {
    let data = {
        "id_give": id,
        "title": title,
        "proposer_name": proposer_name,
        "proposer_names": proposer_names,
        "url": url,
        "date": date
    }

    $.ajax({
        type: "POST",
        url: `/api/bookmark`,
        data: data,
        success: function (response) {
            alert(response["msg"])
            bookmark_show()
        }
    });
}

// 법안 즐겨찾기 삭제 기능
function delete_bookmark(id) {
    $.ajax({
        type: "DELETE",
        url: `/api/bookmark`,
        data: {id_give: id},
        success: function (response) {
            alert(response["msg"])
            bookmark_show()
        }
    });
}