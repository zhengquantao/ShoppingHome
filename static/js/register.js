var user = $('#user');
var pwd = $('#pwd');
var rpwd = $('#rpwd');
var email = $('#email');
var u_error = $('#u_error');
var p_error = $('#p_error');
var rp_error = $('#rp_error');
var e_error = $('#e_error');
user.blur(function () {
    console.log('blur')
    if(user.val().length <= 0 || user.val().length>16){
          u_error.text('名字格式不正确')
    }
});
user.hover(function () {
    u_error.empty()
});
pwd.blur(function () {
    if (pwd.val().length <= 0 || pwd.val().length > 16) {
        p_error.text('密码格式不正确')
    }
});
rpwd.blur(function () {
    if (rpwd.val().length <= 0 || rpwd.val().length > 16) {
        rp_error.text('两次密码不一样')
    }
});
email.blur(function () {
    if (email.val().length <= 0 || email.val().length > 16) {
        e_error.text('邮箱格式不正确')
    }
});
