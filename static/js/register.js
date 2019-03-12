/**
* page : register.html
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
    if (user.val().length == 0 || user.val().length > 16) {
        u_error.text('名字格式不正确')
    } else {
        $.get('/login/register_exit/', {"user": user.val()}, function (data) {
            if (data.count == 1) {
                u_error.text('用户名已存在！');
                user_check = false
            } else {
                user_check = true
            }
        })
    }
});
user.hover(function () {
    u_error.empty()
});
pwd.blur(function () {
    if (pwd.val().length == 0 || pwd.val().length > 16) {
        p_error.text('密码格式不正确')
        pwd_check = false;
    } else {
        pwd_check = true;
    }
});
pwd.hover(function () {
    $('#p_error').empty()
});
rpwd.blur(function () {
    if (rpwd.val().length == 0 || rpwd.val().length > 16 || pwd.val() != rpwd.val()) {
        rp_error.text('两次密码不一样')
        rpwd_check = false;
    } else {
        rpwd_check = true;
    }
});
rpwd.hover(function () {
    rp_error.empty()
});
email.blur(function () {
    if (email.val().length == 0 || email.val().length > 16) {
        e_error.text('邮箱格式不正确');
        email_check = false;
    } else {
        email_check = true
    }
});
email.hover(function () {
    e_error.empty()
});


btn.on('click', function () {
    if (user_check == true && pwd_check == true && email_check == true && rpwd_check == true && check_agree[0].checked == true) {
        $.post('/login/register/', {
                'user': user.val(),
                'pwd': pwd.val(),
                'email': email.val(),
                "csrfmiddlewaretoken": $("[name='csrfmiddlewaretoken']").val()
            },
            function (data) {
                if (data.code) {
                    location.href = '/login/'
                }
            })
    }
});

/**
*   page : login.html
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
        $.post('/login/', {
                "user": login_user.val(),
                "pwd": login_pwd.val(),
                "check": login_choose[0].checked,
                "csrfmiddlewaretoken": $("[name='csrfmiddlewaretoken']").val()
            },
            function (data) {
                if (data.code == 1) {
                    location.href = '/?user='+data.user;
                    $.get('/', {'user':data.user})
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



/**
 * page : person.html
 * */

/*自定义弹框*/
function alert(e) {
    $(".body").append(
        "<div id='body'>" +
        "<div id='mark' style='opacity:0.5;position:fixed;z-index:1;left:0;top:0;height: 100%;width: 100%; background-color: #fff'>" + "</div>" +
        "<div class='alert'  style='z-index: 2; height:200px;width:400px;position:fixed;border-radius:2px;top:30%;left:35%;background-color: #bbb;'>" +
        "<div class='alert-mess' style='height:100px;width: 100%;text-align: center;line-height: 100px;font-size: 20px;color:white'>" + e + "</div>"
        + "<div class='alert-btn' style='height:100px;width:100%;'><button id='btn-sure' style='height:35px;width:80px;background-color: green;border: none; border-radius:5px;color:white;margin-top:45px;margin-left:50px;'>" +
        "确认" + "</button><button id='btn-clear' style='height:35px;width:80px;background-color: red; border: none;border-radius: 5px; color:white;margin-left:140px'>" + "取消" +
        "</button></div>" + "</div>" +
        "</div>");
        //点击模版关闭
    $('#mark').click(function () {
        $('#body').remove()
    });
    //点击取消
    $('#btn-clear').click(function () {
        $('#body').remove();
    });
    // 确认按钮没有加进来
}

$('#area-btn').on('click', function () {
    alert("确定要更改？");
    //点击确认发送
    $('#btn-sure').click(function () {
        console.log('before', $('#header').text().length);
        if ($('#receiver').val().length != 0 && $('#address').val().length != 0 && $('#zip_code').val().length != 0 && $('#phone').val().length != 0 && $('#header').text().length != 0) {
            console.log('send---')
            $.post('/person/update/', {
                'receiver': $('#receiver').val(),
                'address': $('#address').val(),
                'code': $('#zip_code').val(),
                'phone': $('#phone').val(),
                'user': $('#header').text(),
                "csrfmiddlewaretoken": $("[name='csrfmiddlewaretoken']").val()
            }, function (data) {
                if (data.code == 1) {
                    location.href = '/person/address/'
                }
            })
        }
    });
});


/***
 * page : index.html
 */

// $('.list_name').click(function () {
//     console.log($(this).siblings('.strong').text())
//     $.get('/list/', {'id': $(this).siblings('.strong').text(), 'user':$('#index__user').text()||null})
// })






/**
*   page: detail.html
* */

//放大镜

$('#mask').mouseover(function () {
    $('#float_box').show();
    $('#big_box').show();
});
$('#mask').mouseleave(function () {
    $('#float_box').hide();
    $('#big_box').hide();
});
$('#mask').mousemove(function (e) {
    var left = e.clientX - 132; //$('#mask').offset().left - $('#float_box').offset().left - $('#float_box').width()/2;
    var top = e.clientY - 38;//$('#mask').offset().top - $('#float_box').offset().top - $('#float_box').height()/2; //38;
    //console.log("========",$('#mask').offset().top);
    if (left < 0) {
        left = 0
    } else if (left > ($('#mask').width() - $('#float_box').width())) {
        left = $('#mask').width() - $('#float_box').width()
    }
    if (top > ($('#mask').height() - $('#float_box').height())) {
        top = ($('#mask').height() - $('#float_box').height())
    } else if (top < 0) {
        top = 0
    }

    var b_left = left / ($('#mask').width() - $('#float_box').width()) * ($('#big_box').width() - $('#big_img').width())
    var b_top = top / ($('#mask').height() - $('#float_box').height()) * ($('#big_box').height() - $('#big_img').height())
    // var b_left = -left/($('#mask').outerWidth()-$('#float_box').outerWidth())*3.3;
    //  var b_top = -top/($('#mask').outerHeight()-$('#float_box').outerHeight())*3.3;
    $('#float_box').css({"left": left, "top": top});

    $('#big_img').css({'left': b_left, "top": b_top})


})


/*计算价格*/
$('#getNumber').change(function () {
    $('#all_price').empty();
    var num = Number($('#price').text()) * $('#getNumber').val();
    $('#all_price').text(num)
});


$('#detail').click(function () {
    $('.detail-main').show();
    $('.comment-main').hide();
    $(this).css({'background-color': 'green'});
    $('#comment').css({'background-color': ''})
});
$('#comment').click(function () {
    $('.comment-main').show();
    $('.detail-main').hide();
    $('#detail').css({'background-color': ''});
    $(this).css({'background-color': 'green'})

});

// 点击购物车按钮
$('#add_car_btn').click(function () {
    if ($('#index__user').text() == '') {
        alert("你还没有登录哦！ 请登确认登录");
        //点击确认发送
        $('#btn-sure').click(function () {
            location.href = "/login/"
        })

    } else {
        $.get('/shoppingCar/', {'user': $('#index__user').text(), 'id': $('#l_number').text() }, function(data){console.log("GET");if (data.code == 1) {
                //$('#car_number').empty();
                $('#car_number').text(data.count)
            }
        })
    }
});


/**
 * page :car.html
 * */




