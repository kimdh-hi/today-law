$(document).ready(function (){
    get_yesterday_info('')
})

function yesterday_toggle(){
    $('#yesterday-status').toggleClass('is-active')
}

function get_yesterday_info(status) {
    $('#law-card-box').empty()
    console.log(status)

    $.ajax({
        type: "GET",
        url: `/api/yesterday?status=${status}`,
        success: function(res) {
            $('#law-card-box').empty()

            if (res.length == 0) {
                let tmp_html = `<div style="text-align: center">
                                    <h3>조회된 결과가 없습니다.</h3>
                                </div>`
                $('#law-card-box').append(tmp_html)
            } else {

                for (let i = 0; i < res.length; i++) {
                    if (res[i].committee == '') {
                        comittee = '-'
                    } else {
                        comittee = res[i].committee
                    }
                    let tmp_html = `<div class="column img1 toaster is-two-fifths " style="border-radius: 30px;">
                                        <div style="text-align: center; color: steelblue">
                                            <p>
                                                <span style="font-size: 0.7em;">처리상태: </span> ${res[i].status}
                                                <span style="font-size: 0.6em; color: black">${res[i].detail_status}</span></p>
                                        </div>
                                        <p id="category-title"
                                           onClick="open_modal('${res[i].url}', '${res[i].law_id}', '${res[i].title}','', '${res[i].proposer_names}')" class="category-title">${res[i].title}</p>
                                
                                        <p style="font-size: 0.8em">발의자: ${res[i].proposer_names}</p>
                                        <p style="font-size: 0.8em">소관위원회: ${comittee}</p>
                                        <div style="text-align: center;"><p><a href='${res[i].url}' style="font-size: 0.8em">상세정보</a></p></div>
                                </div>`
                    $('#law-card-box').append(tmp_html)
                }
            }
        }
    })
}


// <div className="columns is-multiline is-centered" id="law-card-box">
//     <div className="column img1 toaster is-two-fifths " style="border-radius: 30px;">
//         <div style="text-align: center; color: steelblue">
//             <p>
//                 <span style="font-size: 0.7em;">처리상태: </span>
//                 <span style="font-size: 0.6em; color: black">{{law.detail_status}}</span></p>
//         </div>
//         <p id="category-title"
//            onClick="open_modal({{ law.url }}, {{ law.law_id }}, {{ law.title }},'', {{ law.proposer_names }})"
//            className="category-title">{{law.title}}</p>
//
//         <p style="font-size: 0.8em">발의자: {{law.proposer_names}}</p>
//         <p style="font-size: 0.8em">소관위원회: {{law.committee}}</p>
//         <div style="text-align: center;"><p><a href="{{ law.url }}" style="font-size: 0.8em">상세정보</a>
//         </p>
//         </div>
//     </div>
// </div>