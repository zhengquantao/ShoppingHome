/**
 * page:business/login.html
 * */

var login_user = $('#login_user');
var login_pwd = $('#login_pwd');
var login_btn = $('#login_btn');
var login_pwd_error = $('#login_pwd_error');
var login_user_error = $('#login_user_error');
var login_choose = $('#login_choose');

login_btn.click(function () {
    console.log('......', login_choose.is(":checked"));
    console.log('-----', login_choose[0].checked);
    if (login_user.val().length == 0 || login_pwd.val().length == 0) {
        login_user_error.text('用户名不能为空');
        login_pwd_error.text('密码不能为空');
    } else {
        $.post('/business/login/', {
                "user": login_user.val(),
                "pwd": login_pwd.val(),
                "check": login_choose[0].checked,
                "csrfmiddlewaretoken": $("[name='csrfmiddlewaretoken']").val()
            },
            function (data) {
                if (data.code == 1) {
                    location.href = data.path;
                    //$.get('/', {'user':data.user})
                } else {
                    login_user_error.text('用户名或者密码错误');
                    login_pwd_error.text('用户名或者密码错误');
                }
            })
    }
});
login_pwd.hover(function () {
    login_pwd_error.empty()
});
login_user.hover(function () {
    login_user_error.empty()
});

/***
 * page: business/message.html
 */
//聊天窗口
function openwin(sendto) {
window.open("http://127.0.0.1:8000/chat/?to="+sendto,"newwin","height=450,width=500,resizable=no,toolbar=no,top=100, left=150,scrollbars=no,menubar=no,location=no");
}

$('.click_name').click(function(){
    $(this).parent().siblings('div').remove();
    window.open("http://127.0.0.1:8000/chat/?to="+$(this).text(),"newwin","height=450,width=500,resizable=no,toolbar=no,top=100, left=150,scrollbars=no,menubar=no,location=no");
})

// $('#send_message').click(function(){
//     if($('#input_message').val() != '') {
//         if ($('#chat_user').text() != 'a') {
//             $('.chat_message').append("<div class=\"row\" style=\"margin: 0\">\n" +
//                 "                    <div class=\"col-xs-1 pull-right\" style=\"padding:0;height:40px;\">\n" +
//                 "                        <img src=\"/static/images/person.jpg\" style=\"border-radius: 50%;width:100%;height:100%;\">\n" +
//                 "                    </div>\n" +
//                 "                    <div class=\"col-xs-10 pull-right\" style=\"padding:0; overflow:hidden;\">\n" +
//                 "                        <div style='text-align: center'>&nbsp;&nbsp;<span id='time'>11:31:27</span></div>\n" +
//                 "                        <div class=\"pull-right\" style=\"background-color: rgb(239, 243, 246);height:30px;line-height:30px;border-radius: 5px;\">\n" +
//                 $('#input_message').val() +
//                 "                        </div>\n" +
//                 "                    </div>\n" +
//                 "                </div>"
//             )
//         } else {
//             $('.chat_message').append("<div class=\"row\" style=\"margin: 0\">\n" +
//                 "                    <div class=\"col-xs-1 pull-right\" style=\"padding:0;height:40px;\">\n" +
//                 "                        <img src=\"/static/images/logo.jpg\" style=\"border-radius: 50%;width:100%;height:100%;\">\n" +
//                 "                    </div>\n" +
//                 "                    <div class=\"col-xs-10 pull-right\" style=\"padding:0; overflow:hidden;\">\n" +
//                 "                        <div style='text-align: center'>&nbsp;&nbsp;<span id='time'>11:31:27</span></div>\n" +
//                 "                        <div class=\"pull-right\" style=\"background-color: rgb(239, 243, 246);height:30px;line-height:30px;border-radius: 5px;\">\n" +
//                 $('#input_message').val() +
//                 "                        </div>\n" +
//                 "                    </div>\n" +
//                 "                </div>"
//             );
//
//             var time = new Date()
//             //console.log(time.toLocaleTimeString())
//             $('#time').text(time.toLocaleString());
//             $.get('/chat/update/', {'message': $('#input_message').val(), 'user': $('#chat_user').text()}, function () {
//
//             });
//             $('#input_message').val("");
//         }
//     }})