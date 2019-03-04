/* page : register.html
 *  */
var user = $('#user');
var pwd = $('#pwd');
var rpwd = $('#rpwd');
var email = $('#email');
var u_error = $('#u_error');
var p_error = $('#p_error');
var rp_error = $('#rp_error');
var e_error = $('#e_error');
var check_agree = $('#check_agree');
var btn = $('#btn');
var user_check = false;
var pwd_check = false;
var rpwd_check = false;
var email_check = false;

user.blur(function () {
    if(user.val().length == 0 || user.val().length>16){
        u_error.text('名字格式不正确')
    }else{
        $.get('/login/register_exit/', {"user":user.val()}, function(data){
            console.log(data);
            if(data.count==1){
                u_error.text('用户名已存在！');
                user_check =  false
            }else{
                user_check =  true
            }
        })
    }
});
user.hover(function () {
    u_error.empty()
});
pwd.blur(function () {
    if (pwd.val().length == 0 || pwd.val().length > 16 ) {
        p_error.text('密码格式不正确')
        pwd_check =  false;
    }else{
        pwd_check =  true;
    }
});
pwd.hover(function () {
    $('#p_error').empty()
});
rpwd.blur(function () {
    if (rpwd.val().length == 0 || rpwd.val().length > 16  || pwd.val() != rpwd.val()) {
        rp_error.text('两次密码不一样')
       rpwd_check =  false;
    }else{
        rpwd_check =  true;
    }
});
rpwd.hover(function () {
    rp_error.empty()
});
email.blur(function () {
    if (email.val().length == 0 || email.val().length > 16) {
        e_error.text('邮箱格式不正确');
        email_check = false;
    }else{
        email_check = true
    }
});
email.hover(function () {
    e_error.empty()
});


btn.on('click', function(){
    if(user_check==true && pwd_check==true && email_check==true && rpwd_check == true && check_agree[0].checked == true){
        $.post('/login/register/', {'user':user.val(), 'pwd':pwd.val(), 'email':email.val(),"csrfmiddlewaretoken": $("[name='csrfmiddlewaretoken']").val()},
        function(data){
            if(data.code){
                location.href = '/login/'
            }
        })
    }
});

/* page : login.html
*
* */

var login_user = $('#login_user');
var login_pwd = $('#login_pwd');
var login_btn = $('#login_btn');
var login_pwd_error = $('#login_pwd_error');
var login_user_error = $('#login_user_error');
var login_choose = $('#login_choose');

login_btn.click(function(){
    console.log('......',login_choose.is(":checked"));
    console.log('-----', login_choose[0].checked);
    if(login_user.val().length == 0 || login_pwd.val().length == 0){
        login_user_error.text('用户名不能为空');
        login_pwd_error.text('密码不能为空');
    }else{
        $.post('/login/', {"user":login_user.val(), "pwd": login_pwd.val(), "check": login_choose[0].checked,"csrfmiddlewaretoken": $("[name='csrfmiddlewaretoken']").val()},
            function (data) {
                if(data.code==1){
                    location.href = "/person/";
                }else{
                    login_user_error.text('用户名或者密码错误');
                    login_pwd_error.text('用户名或者密码错误');
                }
            })
    }
});
login_pwd.hover(function(){
    login_pwd_error.empty()
});
login_user.hover(function(){
    login_user_error.empty()
});