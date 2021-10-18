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
    console.log(name, bio)
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

                console.log(res)


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
                    console.log('not logged in')
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
        console.log(idx)
        $(".page-list li").removeClass("is-active");
        console.log($(".page_list li").eq(idx))
        $(".page-list li").eq(idx).addClass("is-active");
        if ($(this).text().includes('작성한 청원')) {
            $.ajax({
                type: "GET",
                url: `/mypage/wishlist`,
                success: function (res) {
                    $("#mypage-contents").empty();
                    console.log(res['title'])
                    let category = res['category_give']
                    let title = res['title_give']
                    let time = res['time_give']
                    let contents = res['contents_give']
                    let agree = res['agree_give']
                    temp_html = `<div class="wishlist">
                                  <table class="table is-responsive">
                                    <thead>
                                      <tr>
                                        <th>카테고리</th>
                                        <th>제목</th>
                                        <th>작성일</th>
                                      </tr>
                                    </thead>
                                    <tbody>
                                      <tr>
                                        <td>${category}</td>
                                        <td onclick="open_modal_wish('${title}','${category}','${time}','${agree}', '${contents}')"><a>${title}</a></td>
                                        <td>${time}</td>
                                      </tr>
                                    </tbody>
                                  </table>
                                </div>`
                    $('#mypage-contents').append(temp_html)

                }
            })
        }
        else if ($(this).text().includes('좋아요')) {
            $.ajax({
                type: "GET",
                url: `/mypage/wishlist`,
                success: function (res) {
                    $("#mypage-contents").empty();
                    console.log(res['title'])
                    let category = res['category_give']
                    let title = res['title_give']
                    let time = res['time_give']
                    let contents = res['contents_give']
                    let agree = res['agree_give']
                    temp_html = `<div class="wishlist">
                                  <table class="table is-responsive">
                                    <thead>
                                      <tr>
                                        <th>법안이름</th>
                                        <th>대표발의자</th>
                                        <th>발의일</th>
                                      </tr>
                                    </thead>
                                    <tbody>
                                      <tr>
                                        <td></td>
                                        <td></td>
                                        <td></td>
                                      </tr>
                                    </tbody>
                                  </table>
                                </div>`
                    $('#mypage-contents').append(temp_html)

                }
            })
        }

    })

})

function dpmenu() {
    if ($(".dropdown").hasClass("is-active")) {
        $(".dropdown").removeClass("is-active")
    } else {
        $(".dropdown").addClass("is-active")
    }
}

function close_modal() {
    $(".modal").removeClass("is-active");
    //모달을 비워주지 않으면 두번째 창부터 좋아요 버튼이 생기지 않음
    $(".modal").empty();
}