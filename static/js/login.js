function show_login_modal() {
    tmp_html = `<div class="modal is-active">
                                <div class="modal-background" onclick="close_modal()"></div>
                                <div class="modal-content" style="width: 500px; height: 360px; margin: auto;">

                                        <div class="card-content" style="text-align: center">     
                                        <p style="font-size: 30px">로그인</p>                             
                                            <div class="content" style="margin-top: 40px">
                                                <ul class="social_button">
                                                    <li>
                                                        <button class="img_kakao" onclick="window.location.href='/oauth/kakao'"></button>
                                                    </li>
                                                    <li>
                                                        <button class="img_google" onclick="window.location.href='/oauth/google'"></button>
                                                    </li>
                                                    <li>
                                                        <button class="img_naver" onclick="window.location.href='/oauth/naver'"></button>
                                                    </li>
                                                </ul>                                                
                                            </div>

                                        </div>

                                </div>
                                <button class="modal-close is-large" aria-label="close" onclick="close_modal()"></button>
                            </div>`
    $('body').append(tmp_html)
}

function close_modal() {
    $(".modal").removeClass("is-active");
    $(".modal").empty();
}


function logout() {

    $.removeCookie("mytoken");
    alert('로그아웃')
    window.location.href = '/'
}


