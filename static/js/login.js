function show_login_modal() {
    tmp_html = `<div class="modal is-active">
                                <div class="modal-background" onclick="close_modal()"></div>
                                <div class="modal-content" style="width: 500px; height: 200px;">

                                        <div class="card-content" style="text-align: center">     
                                        <p style="font-size: 30px">로그인</p>                             
                                            <div class="content" style="margin-top: 40px">
                                                <button onclick="window.location.href='/oauth/kakao'" class='btn-social-login' style='background:#FFEB00'><i class="xi-3x xi-kakaotalk text-dark"></i></button>
                                                <button onclick="window.location.href='/login_google'" class='btn-social-login' style='background:#D93025'><i class="xi-3x xi-google"></i></button>
                                                <button class='btn-social-login' style='background:#4267B2'><i class="xi-3x xi-facebook"></i></button>
                                                <button class='btn-social-login' style='background:#55ACEE'><i class="xi-3x xi-twitter"></i></button>
                                                <button class='btn-social-login' style='background:#24292E'><i class="xi-3x xi-github"></i></button>
                                                <button onclick="window.location.href='/oauth/naver'" class='btn-social-login' style='background:#1FC700'><i class="xi-3x xi-naver"></i></button>                                                
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


