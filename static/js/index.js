$(document).ready(function () {

    // 법안목록 받아오기
    get_law_list()

    //탭 메뉴 전환 ( 전체보기 / 즐겨찾기 )
    $(".tab_title li").click(function () {
        let idx = $(this).index();
        //console.log(idx)
        $(".tab_title li").removeClass("is-active");
        $(".tab_title li").eq(idx).addClass("is-active");
        $(".card-container > .card-list").hide();
        $(".card-container > .card-list").eq(idx).show();
        console.log($(".card-container > .card-list").index())
    })
    $('#ranking-box').vTicker();
})

//모달 열기 (id를 인자로 받는 함수??)
function open_modal(url, id, title) {
    $.ajax({
        type: "POST",
        url: "/api/laws/details",
        data: {url_give: url, id_give: id, title_give: title},
        success: function (response) {
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
            }
            else if(content.includes("제안이유")){
                content2 = content.split('제안이유')[1].split('주요내용')[0]
                content3 = content.split('주요내용')[1]
                subtitle = '제안이유'
                subtitle2 ='주요내용'
            }
            else
            {
                content2=content
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

                                        </div>

                                </div>
                                <button class="modal-close is-large" aria-label="close" onclick="close_modal()"></button>
                            </div>`
            $('body').append(temp_html)
        }
    })
    //$(".modal").addClass("is-active");

}

//모달 닫기
function close_modal() {
    $(".modal").removeClass("is-active");
    get_ranking()
}

//법안 전체목록 가져오기
function get_law_list() {
    $('#laws-box').empty()
    $.ajax({
        type: "GET",
        url: "/api/laws?offset=1",
        success: function (res) {
            add_law_list(res)
            get_ranking()
        }
    })
}

//법안이름으로 조회
function get_law_list_by_title(title) {
    $('#laws-box').empty()
    $.ajax({
        type: "GET",
        url: `/api/laws?offset=1&query=${title}&condition=법안명`,
        success: function (res) {
            add_law_list(res)
        }
    })
}

//발의자 이름으로 조회
function get_law_list_by_proposer_name(name) {
    $('#laws-box').empty()
    $.ajax({
        type: "GET",
        url: `/api/laws?offset=1&proposer=${name}&condition=제안자`,
        success: function (res) {
            add_law_list(res)
        }
    })
}

//법안목록 html 추가
function add_law_list(res) {
    for (let i = 0; i < res.length; i++) {
        let tmp_html = `<div class="card">
                            <div class="card-content">
                                <div class="media">
                                    <div class="media-content">
                                        <a>
                                            <p class="title is-5" style="color: black" id="title" onclick="open_modal('${res[i].url}', '${res[i].id}', '${res[i].title}')">${res[i].title}</p>
                                        </a>
                                        <p class="subtitle is-6">${res[i].proposer_name}</p>
                                        <p>${res[i].proposer_names}</p>
                                    </div>
                                </div>
                                <div class="content" id="content">
                                    <time id="date" datetime="2016-1-1">${res[i].date}</time>
                                </div>
                            </div>`
        $('#laws-box').append(tmp_html)
    }
}

// 조회
function search() {
    let condition = $('#select-condition option:selected').val()
    let query = $('#search-list').val()

    if (condition == 'title') {
        get_law_list_by_title(query)
    } else {
        get_law_list_by_proposer_name(query)
    }
}

function get_ranking() {
    console.log('getranking')
    $('#ranking-list').empty()
    $.ajax({
        type: "GET",
        url: "/api/rank",
        success: function(res) {
            console.log(res)
            for (let i=0;i<res.length;i++) {
                let tmp_html = `<li>${res[i]['rank']}위  ${res[i]['title']}</li>`
                $('#ranking-list').append(tmp_html)
            }
        }
    })
}