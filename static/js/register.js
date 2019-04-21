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
    if (/^[\w]{7,10}@[\w]+[.][\w]{2,4}$/.test(email.val())) {
        email_check = true
    } else {
        e_error.text('邮箱格式不正确');
        email_check = false;
    }
});
email.hover(function () {
    e_error.empty();
    $('#cm_error').empty();
});
//点击注册按钮
btn.on('click', function () {
    if (user_check == true && pwd_check == true && email_check == true && rpwd_check == true && check_agree[0].checked == true && $('#check_message').val() != '') {
        //密码加盐
        var salt="1a2b3c4d";
        var str_r =  ""+salt.charAt(0)+salt.charAt(2)+pwd.val()+salt.charAt(5)+salt.charAt(4);
        var password_r = md5(str_r);
        $.post('/login/register/', {
                'user': user.val(),
                'pwd': password_r,
                'email': email.val(),
                'check_message': $('#check_message').val(),
                "csrfmiddlewaretoken": $("[name='csrfmiddlewaretoken']").val()
            },
            function (data) {
                if (data.code) {
                    location.href = data.path
                } else {
                    $('#cm_error').text('验证码有误')
                }
            })
    }
});
//定时器
// function sleep(second){
//     var now = new Date();
//     var last = now.getTime() + second;
//     while(true){
//         now = new Date();
//         if(now.getTime() > last){
//             return
//         }
//     }
// }

/**ES7语法*/
const sleep = (timeout) => new Promise((resolve) => {
    setTimeout(resolve, timeout);
});

//点击验证码

$('.check_message_btn').click(function () {

    if (email_check == true) {
        /**ES7语法*/
        (async () => {
            for (var i = 60; i > 0; i--) {
                await sleep(1000);
                $('.check_message_btn').text("剩余时间" + i);
                $('.check_message_btn').attr('disabled', true);

                if (i == 1) {
                    $('.check_message_btn').text("获取验证码");
                    $('.check_message_btn').attr('disabled', false);
                }
            }
        })();

        $.get('/login/email/', {"check_message": email.val()}, function (data) {
            if (data.status) {
                pass
            } else {
                $('#cm_error').text('邮箱有误')
            }
        });
        //for(let i=10; i>0;i--) {
        //       (function(j){ //闭包
        //
        //          setTimeout(function () {
        //         //sleep(1000)
        //              console.log(j)
        //         $('.check_message_btn').text("剩余时间" + j)
        //              if(i==1){
        //             $('.check_message_btn').text("获取验证码")
        //                  return
        //              }
        //     }, 0);
        //      })(i)
        //
        // }

    }
})


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
    //加盐
    var salt="1a2b3c4d";
    var str =  ""+salt.charAt(0)+salt.charAt(2)+login_pwd.val()+salt.charAt(5)+salt.charAt(4);
    var password = md5(str);

    if (login_user.val().length == 0 || login_pwd.val().length == 0) {
        login_user_error.text('用户名不能为空');
        login_pwd_error.text('密码不能为空');
    } else {
        $.post('/login/', {
                "user": login_user.val(),
                "pwd": password,
                "check_code": $('#check_code').val(),
                "check": login_choose[0].checked,
                "csrfmiddlewaretoken": $("[name='csrfmiddlewaretoken']").val()
            },
            function (data) {
                if (data.code == 1) {
                    location.href = data.path;
                    //$.get('/', {'user':data.user})
                }
                else if (data.code == 2) {
                    $('#login_check_code_error').text("验证码错误")
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
$('#check_code').hover(function () {
    $('#login_check_code_error').empty()
});

//点击验证码图片
$('#check_img').click(function () {
    $.get('/login/check_img/', function (data) {
        // data.path_img += '?';
        $('#check_img')[0].src += '?';
        //$('#check_img').attr('src', data.path_img)
        // console.log(data.path_img)
    })
})


/***
 * page: person.html
 */
$('.old_pwd').focusin(function () {
    $('.pwd_error').empty()
})
$('.new_pwd').focusin(function () {
    $('.rpwd_error').empty()
})
$('.pwd_btn').click(function () {
    if ($('.old_pwd').val() == "") {
        $('.pwd_error').text('密码不能为空')
    }
    if ($('.new_pwd').val() == "") {
        $('.rpwd_error').text('密码不能为空')
    }
    if ($('.old_pwd').val() != "" && $('.new_pwd').val() != "") {
        $.post('/person/', {
                "pwd": $('.old_pwd').val(),
                "rpwd": $('.new_pwd').val(),
                "csrfmiddlewaretoken": $("[name='csrfmiddlewaretoken']").val()
            },
            function (data) {
                if (data.status == 1) {
                    alert(data.msg)
                    $('#btn-sure').click(function () {
                        $('#body').remove()
                    })
                } else {
                    alert(data.msg)
                    $('#btn-sure').click(function () {
                        $('#body').remove()
                    })
                }
            })
    }
});


/**
 * page : address.html
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


/**
 *   page: detail.html
 */

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
    var left = e.clientX - $('#mask').offset().left - $('#float_box').width() / 2;  //132; - $('#float_box').offset().left
    var top = e.clientY - $('#mask').offset().top - $('#float_box').height() / 2; //38; - $('#float_box').offset().top
    //console.log('left', left, 'top', top)
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
    //$('#alls_price').empty();
    var num = (Number($('#price').text()) * $('#getNumber').val()).toFixed(2);
    $('#alls_price').text(num)
});


$('#detail').click(function () {
    $('.detail-main').show();
    $('.comment-main').hide();
    $(this).css({'background-color': '#5cb85c'});
    $('#comment').css({'background-color': ''})
});
$('#comment').click(function () {
    $('.comment-main').show();
    $('.detail-main').hide();
    $('#detail').css({'background-color': ''});
    $(this).css({'background-color': '#5cb85c'})

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
        $.get('/shoppingCar/', {
            'user': $('#index__user').text(),
            'id': $('#l_number').text(),
            'count': $('#getNumber').val()
        }, function (data) {
            console.log("GET");
            if (data.code == 1) {
                //$('#car_number').empty();
                $('#car_number').text(data.count)
            }
        })
    }
});
//点击购买按钮
$('#buy_btn').click(function () {
    var item_lists = $('.item_name').text() + ',' + $('#l_number').text() + ',' + $('#getNumber').val() + ',' + $('#price').text();
    location.href = '/pay/?price=' + $('#alls_price').text() + '&item=' + item_lists;
});


//评论
$('.face').hover(function(){
    $('#i1').css({'display': 'block'})
    $('.icon_face').click(function(){
        let icon = $(this).text()
        $('#comment_content').append(icon)
    })
},function(){
    $('#i1').css({'display': 'none'});
});

//子评论
$('.c_face').hover(function(){
    $('#ci1').css({'display': 'block'})
    $('.cicon_face').click(function(){
        let icon = $(this).text()
        $('.textareas').append(icon)
    })
},function(){
    $('#ci1').css({'display': 'none'});
});



$('#commit_comment').click(function () {
    if($('#index__user').text() == ""){
        location.href = '/login/'
    }else {
        if ($('#comment_content').val() != '') {
            $.get('/detail/comment/', {
                //'user': $('#index__user').text(),
                'comment': $('#comment_content').val(),
                'cid': $('#l_number').text(),
            }, function (data) {
                $('.comment-main').append(
                " <div class=\"col-xs-12\" style=\"border:1px solid green; border-radius:5px;background-color:#ccc;\">\n" +
                "                        <div style=\"font-size: 15px;height:30px;line-height: 30px;\">" + $('#index__user').text() + "</div>\n" +
                "                        <div style=\"margin-left:30px;\">\n" +
                "                            <div style=\"background-color:white;border-radius: 2px;\">\n" +
                $('#comment_content').val() +
                "                            </div>\n" +
                "                            <div class=\"pull-right\"><span id=\"uid\" class=\"hidden\">"+ data.uid +"</span><a class=\"question\" style='cursor: pointer'>回复</a></div>\n" +
                "                        </div>\n" +
                "                    </div>"
            );
                //清空输入框
                $('#comment_content').empty();
            })

        }
    }
});
//点击回复
$('.question').click(function(){
    if($('#index__user').text() == ""){
        location.href = '/login/'
    }else{
    $(this).parents().siblings('.input-commit').css({'display': 'block'})
    }
});
//点击关闭的地方
$('.close-btn').click(function(){
    $(this).parents('.input-commit').css({'display': 'none'});
});
//点击确认
$('.sure-btn').click(function(){
    if($(this).siblings('.textareas').val() != "") {
        $.get('/detail/Ccomment/', {
            'comment': $(this).siblings('.textareas').val(),
            'uid': $(this).parents().siblings('.pull-right').children('#uid').text()
        }, function(data){

        });
        $(this).parents().parents().parents('.children_comment').append("     <div class=\"col-xs-12 children_comment\" style=\"border:1px solid green;margin-bottom: 10px; border-radius:5px;background-color:#ddd;\">\n" +
            "                        <div class=\"question_name\" style=\"font-size: 15px;height:30px;line-height: 30px;\">"+$('#index__user').text()+"</div>\n" +
            "                        <div style=\"margin-left:30px;\">\n" +
            "                            <div style=\"background-color:white;border-radius: 2px;\">\n" +
                                            $(this).siblings('.textareas').val() +
            "                            </div>\n" +
            "                        </div>\n" +
            "                    </div>\n");
    }
    //清空输入框
    $(this).siblings('.textareas').empty();
});



/**
 *   page : shoppingCar.html
 */

//获取checkbox框的状态
console.log("=======", $('.checkbox').is(':checked'));

var $items_price = $('td').siblings('.items_price');//小计
var $item_allname = $('td').siblings('.item_small_img').children('.item_name'); //名字
var $item_allprice = $('td').siblings('.item_price'); //单价
var $item_allnum = $('td').siblings('.num_item_input').children('.num_input'); //数量
var $item_l_num = $('td').siblings().children('.car_delete_btn').children('.item_l_number');  //商品编号

//点击减号
$('.reduce_btn').click(function () {

    if (parseInt($(this).next('.num_input').val()) == 0) {
        console.log(this)
        $(this).next('.num_input').val(0)
    } else {
        var reduce = parseInt($(this).next('.num_input').val()) - 1;
        $(this).next('.num_input').val(reduce);//框的变化
        //小计变化
        $(this).parent().next('.items_price').text((parseInt($(this).next('.num_input').val()) * parseFloat($(this).parent().prev('.item_price').text())).toFixed(2));
        al()
    }
});

//点击加号
$('.add_num_btn').click(function () {
    var add = parseInt($(this).prev('.num_input').val()) + 1;
    $(this).prev('.num_input').val(add);
    //小计变化
    $(this).parent().next('.items_price').text((parseInt($(this).prev('.num_input').val()) * parseFloat($(this).parent().prev('.item_price').text())).toFixed(2));
    al()
});

//手动输入
$('.num_input').blur(function () {
    //小计变化
    $(this).parent().next('.items_price').text((parseInt($(this).val()) * parseFloat($(this).parent().prev('.item_price').text())).toFixed(2));
    al()
});

//加载时的总价
//全局的数据
var item_lists;

function al() {
    var all_price = 0;
    var item_list = new Array();//局部的数据
    for (var i = 0; i < $items_price.length; i++) {
        if ($('.checkbox').eq(i).is(':checked') == true) {
            item_list[i] = new Array()
            all_price += parseFloat($items_price.eq(i).text());
            item_list[i].push([$item_allname.eq(i).text(), $item_l_num.eq(i).text(), $item_allnum.eq(i).val(), $item_allprice.eq(i).text()])
        } else {
            continue
        }
    }
    $('#all_price').text(all_price.toFixed(2));
    item_lists = item_list;
}

al();


//点击选择框时价格的变动
$('.checkbox').change(function () {
    // var all_price = 0;
    // for (var i=0; i<$items_price.length; i++){
    //     if($('.checkbox').eq(i).is(':checked')==true){
    //     all_price += parseInt($items_price.eq(i).text());
    //     }
    // }
    // $('#all_price').text(all_price);
    al()
})


//点击删除按钮
$('.car_delete_btn').click(function () {
    $(this).parent().parent().remove();
    al();
    $.get('/shoppingCar/car_update/', {'id': $(this).next('span').text()}, function (data) {
        if (data.code == 1) {
            $('#car_number').text(data.count)
        }
    })
})


//点击购买框  触发的事件
$('#car_button').click(function () {
    for (var i = 0; i < item_lists.length; i++) {
        if (item_lists[i] == null) {  //如果数组里数据为空，把那个为空的数据删除掉
            item_lists.splice(i, 1)
        }
    }
    location.href = '/pay/?price=' + $('#all_price').text() + '&item=' + item_lists;
});


/***
 * page: chat.html
 */
//聊天窗口
function openwin() {
    window.open("http://127.0.0.1:8000/chat/", "newwin", "height=450,width=500,resizable=no,toolbar=no,top=100, left=150,scrollbars=no,menubar=no,location=no");
}


/***
 * page: coupon.html
 */
$('.ticket').click(function(){
    if($('#index__user').text() == ""){
        location.href="/login/"
    }else{
        $.get('/ticket/update/', {'id': $(this).children().children('.ticket_id').text()}, function(date){
            alert(date.msg);
            //关闭模版
            $('#btn-sure').click(function(){
                 $('#body').remove();
            })
        })
    }
});

/***
 *  page:pay.html
 */

let $nums = $('#A-price').text()
$('.radios').click(function(){
    if($(this).is(':checked') == true){
        var num = Number($nums)-Number($(this).siblings('.one-price').text());
        $('#A-price').text(num);
        $('#pay_ali').attr('href', '/pay/pay_ali/?price='+num+'&item='+$('#item_message').text()+'&name='+$(this).siblings('.one-name').text())
        $('#pay_wx').attr('href', '/pay/pay_wx/?price='+num+'&item='+$('#item_message').text()+'&name='+$(this).siblings('.one-name').text())
        $('#pay_yl').attr('href', '/pay/pay_yl/?price='+num+'&item='+$('#item_message').text()+'&name='+$(this).siblings('.one-name').text())
    }
});


/***
 * page:seckill.html
 */

// function countDown(maxtime, n){
//     var timer = setInterval(function(){
//         if(maxtime!=0){
//             maxtime--;
//             $kill_items.eq(n).text("剩余时间"+maxtime)
//         }else{
//             clearInterval(timer)
//             $kill_items.eq(n).text("开始秒杀");
//             $kill_items.eq(n).removeClass('kill_items')
//         }
//     },1000)
// }


var startTime = $('.startTime');
var endTime = $('.endTime').text();
var $kill_items = $('.kill_items');
var nowTime = (new Date).getTime()/1000;
//console.log(startTime.length,"===========");
for(var i=0; i<startTime.length;i++){
    var residueTime = parseInt(startTime.eq(i).text()-nowTime);
    //console.log(residueTime, '===========');
    /**ES7语法*/
    (async (residueTime, i) => {
        for (var j=residueTime; j > 0; j--) {
            //console.log(residueTime, '+++++++++++');
            //console.log(i, '====');
            await sleep(1000);
            residueTime--;
            $kill_items.eq(i).text("剩余时间"+residueTime);
        }
        $kill_items.eq(i).text("开始秒杀");
        $kill_items.eq(i).removeClass('kill_items', 'disable');
        $kill_items.eq(i).addClass('start-kill-item')
    })(residueTime, i);
    // countDown(residueTime, i);
};
$('.start-kill-item').click(function(){
    alert("正在排队中。。。。");
    $('#btn-sure').click(function () {
        $('#body').remove();
    });
    // 判断用户是否为空
    if($('#index__user').text() == ""){
        location.href="/login/"
    }else {
        //不为空发送数据
        $.post('/seckill/sendkill/', {
                "id": $(this).siblings('.goods_items__l_number').text(),
                "trend_path": $(this).siblings('.trend_path_s').text(),
                "csrfmiddlewaretoken": $("[name='csrfmiddlewaretoken']").val()
            }, function (data) {
                if (data.path) {
                    alert(data.msg);
                    setTimeout(function () {
                        location.href = data.path;
                    }, 3000);
                } else {
                    alert(data.msg);
                    //location.href = '/seckill/'
                }
            }
        );
    }
});


/***
 * page: goodkill.html
 */
//计时器
(async (pay_time) =>{
    for(var time=pay_time; time>0;time--){
        await sleep(1000);
        time--;
        $('.pay_time').text(time);
        if(time == 0){
            alert("秒杀失败了！！！！！");
            await sleep(3000);
            location.href= '/'
        }
    }

})($('.pay_time').text());

//秒杀支付
$('#kill-pay').click(function(){
    var item_lists = $('.kill_item_name').text() + ',' + $('.kill_item_l_number').text() + ',' + 1 + ',' + $('.kill_price').text();
    location.href = '/pay/?price=' + $('.kill_price').text() + '&item=' + item_lists;
});
