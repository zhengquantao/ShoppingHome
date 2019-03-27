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