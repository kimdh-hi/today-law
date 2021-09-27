let offset = 1; // 페이징 시작위치
let total_count; // api호출시 반한받는 아이템의 수

// 더보기로 인한 법안목록 추가인지 체크하기 위함
// false인 경우 리스트를 지우고 새로 html을 생성
// true인 경우 기존 리스트를 유지하고 뒤에 새로 html을 append
let more = false;

let g_condition // 현재 검색조건이 법안이름인지 의원이름인지 구분 (all, title, name)
let g_title // 현재 검색되고 있는 법안이름
let g_name // 현재 검색되고 있는 의원이름
let g_readmore_button_show = true // 더보기 버튼을 보여줄 것인지 판단

$(document).ready(function () {
    g_condition = "all"
    g_title = ""
    g_name = ""
    // 법안목록 받아오기
    get_law_list()
    // 즐겨찾기
    bookmark_show()

    //탭 메뉴 전환 ( 전체보기 / 즐겨찾기 )
    $(".tab_title li").click(function () {
        let idx = $(this).index();
        //console.log(idx)
        $(".tab_title li").removeClass("is-active");
        $(".tab_title li").eq(idx).addClass("is-active");
        $(".card-container > .card-list").hide();
        $(".card-container > .card-list").eq(idx).show();
    })
    $('#ranking-box').vTicker();
})

//모달 열기 (법안 상세내용)
function open_modal(url, id, title) {
    $.ajax({
        type: "POST",
        url: "/api/laws/details",
        data: {url_give: url, id_give: id, title_give: title},
        success: function (response) {
            like_show()
            let id = response['id']
            let title = response['title'].split('(')[0]
            let proposer = response['proposer']
            let content = response['content']
            let date = response['date']
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
                                <div class="modal-background" onclick="close_modal()"></div>
                                <div class="modal-content">

                                        <div class="card-content" style="text-align: center">
                                            <div class="media">
                                                <div class="media-content">
                                                    <p class="title is-5">${title}</p>
                                                    <time style="font-size: 1em" datetime="2016-1-1">${date}</time>
                                                    <p class="subtitle is-6">${proposer}</p>
                                                    <div>
                                                        <button id="btn-save" class="btn btn-outline-sparta btn-lg" onclick="bookmark('${id}')">
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
                                                ${content2}
                                                <br>
                                                <hr>
                                                <br>
                                                <span id="subtitle_2" style="text-align: left; font-size: 1.5em; font-weight: bold" >${subtitle2}</span>
                                                <br>
                                                ${content3}
                                                <br>

                                            </div>
                                            <footer class="card-footer" id="card-footer">
                                            
                                            </footer>

                                        </div>

                                </div>
                                <button class="modal-close is-large" aria-label="close" onclick="close_modal()"></button>
                            </div>`
            $('body').append(temp_html)
        }
    })
}

//모달 닫기
function close_modal() {
    $(".modal").removeClass("is-active");
    get_ranking()
}

//법안 전체목록 가져오기
function get_law_list() {
    if (!more) $('#laws-box').empty()
    $.ajax({
        type: "GET",
        url: `/api/laws?offset=${offset}`,
        success: function (res) {
            total_count = res[0].total_count
            add_law_list(res)
            get_ranking()
        }
    })
}

//법안이름으로 조회
function get_law_list_by_title(title) {
    g_title = title
    g_condition = "title"
    if (!more) $('#laws-box').empty()
    $.ajax({
        type: "GET",
        url: `/api/laws?offset=${offset}&query=${title}&condition=법안명`,
        success: function (res) {
            total_count = res[0].total_count
            if (!more) g_readmore_button_show = total_count > 10 ? true : false
            add_law_list(res)
        }
    })
}

//발의자 이름으로 조회
function get_law_list_by_proposer_name(name) {
    g_name = name
    g_condition = "name"
    if (!more) $('#laws-box').empty()
    $.ajax({
        type: "GET",
        url: `/api/laws?offset=${offset}&proposer=${name}&condition=제안자`,
        success: function (res) {
            total_count = res[0].total_count
            if (!more) g_readmore_button_show = total_count > 10 ? true : false
            add_law_list(res)
        }
    })
}

//법안목록 html 추가
function add_law_list(res) {
    for (let i = 1; i < res.length; i++) {
        console.log(res[i].proposer_name)
        let tmp_html = `<div class="card">
                            <div class="card-content">
                                <div class="media">
                                    <div class="media-content">
                                        <a>
                                            <p class="title is-5" style="color: black" id="title" onclick="open_modal('${res[i].url}', '${res[i].id}', '${res[i].title}')">${res[i].title}</p>
                                        </a>        
                                        <br/>                                            
                                        <p>대표 제안자: ${res[i].proposer_name}</p>
                                        <p>${res[i].proposer_names}</p>
                                    </div>
                                </div>
                                <div class="content" id="content">
                                    <time id="date" datetime="2016-1-1">${res[i].date}</time>
                                </div>
                            </div>`
        $('#laws-box').append(tmp_html)
        add_readMore_button()
    }
}

// 조회
function search() {
    more = false
    offset = 1

    let condition = $('#select-condition option:selected').val()
    let query = $('#search-list').val()

    if (condition == 'title') {
        get_law_list_by_title(query)
    } else {
        get_law_list_by_proposer_name(query)
    }
}

// open_modal(url, id, title)
function get_ranking() {
    $('#ranking-list').empty()
    $.ajax({
        type: "GET",
        url: "/api/rank",
        success: function(res) {
            for (let i=0;i<res.length;i++) {
                let tmp_html = `<li onclick="open_modal('${res[i]['url']}', '${res[i]['id']}', '${res[i]['title']}')">${res[i]['rank']}위  ${res[i]['title']}</li>`
                $('#ranking-list').append(tmp_html)
            }
        }
    })
}

// 좋아요
function like_show() {
    $.ajax({
            type: 'GET',
            url: '/api/like',
            data: {},
            success: function (response) {
                let like_list = response['like_list']

                let id, like, hate

                for (let i = 0; i < like_list.length; i++) {
                    id = like_list[i]['id']
                    like = like_list[i]['like']
                    hate = like_list[i]['hate']
                }


                let temp_html = `<a href="#" onClick="likeLaw('${id}')" class="card-footer-item has-text-info">
                                                    좋아요 ${like}명 <i class="fa fa-thumbs-up" aria-hidden="true"></i>
                                                </a>
                                                <a href="#" onClick="hateLaw('${id}')" class="card-footer-item has-text-danger">
                                                    싫어요 ${hate}명 <i class="fa fa-thumbs-down" aria-hidden="true"></i>
                                                </a>`
                $('#card-footer').append(temp_html)
            }

        }
    )
}

// 좋아요 기능
function likeLaw(id) {
    $.ajax({
        type: 'POST',
        url: '/api/like',
        data: {id_give: id},
        success: function (response) {
            alert(response['msg']);
            window.location.reload()
        }
    })
}

//싫어요 기능
function hateLaw(id) {
    $.ajax({
        type: 'POST',
        url: '/api/hate',
        data: {id_give: id},
        success: function (response) {
            alert(response['msg']);
            window.location.reload()
        }
    });
}

// 더보기 버튼 추가
function add_readMore_button() {
    $('#read-more-box').remove()

    if (total_count > 10 && g_readmore_button_show) {
        $('#laws-box')
            .append(
                '<div id="read-more-box" style="width: 100px; margin: 50px auto 50px auto;"><i onclick="readMore()" class="fas fa-chevron-circle-down fa-5x"></i></div>'
            )
    }
}

// 더보기 기능
function readMore() {
    more = true; // 기존 리스트를 유지

    //  offset의 끝에 도달한 경우
    if ((offset+1)*10 >= total_count) {
        g_readmore_button_show = false
    }
    offset+=1

    // 현재 검색조건이 의원이름인 경우 더보기 처리
    if (g_condition == "name")
        get_law_list_by_proposer_name(g_name)
    // 현재 검색조건이 법안이름인 경우 더보기 처리
    else if (g_condition == "title") {
        get_law_list_by_title(g_title)
    }
    // 현재 검색조건이 없는 경우 더보기 처리
    else
        get_law_list()
}

// 법안 즐겨찾기 보여주기
function bookmark_show() {
    $.ajax({
            type: 'GET',
            url: '/api/bookmark',
            data: {},
            success: function (response) {
                let bookmark_list = response['bookmark_list']

                for (let i = 0; i < bookmark_list.length; i++) {
                    let id = bookmark_list[i]['id']
                    let url = bookmark_list[i]['url']
                    let title = bookmark_list[i]['title']
                    let proposer = bookmark_list[i]['proposer']
                    let date = bookmark_list[i]['date']

                    let temp_html = `<div class="card">
                                        <div class="card-content">
                                            <div class="media">
                                                <div class="media-content">
                                                    <a>
                                                        <p class="title is-4" style="color: black" id="title" onclick="open_modal('${url}', '${id}', '${title}')">${title}</p>
                                                    </a>
                                                    <p class="subtitle is-6" style="color: black" >${proposer}</p>
                                                </div>
                                            </div>
                                            <div class="content">
                                                <time datetime="2016-1-1">${date}</time>
                                            </div>
                                        </div>
                                    </div>`
                    $('#bookmark').append(temp_html)

                }


            }

        }
    )
}

// 법안 즐겨찾기 기능
function bookmark(id) {
    $.ajax({
        type: "POST",
        url: `/api/bookmark`,
        data: {id_give: id},
        success: function (response) {
            alert(response["msg"])
        }
    });
}

// 법안 즐겨찾기 삭제 기능
function delete_bookmark(id) {
    $.ajax({
        type: "POST",
        url: `/api/delete_bookmark`,
        data: {id_give: id},
        success: function (response) {
            alert(response["msg"])
            window.location.reload()
        }
    });
}

