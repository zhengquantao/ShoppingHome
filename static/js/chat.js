//提交数据
$('#send_message').click(function () {
    if ($('#input_message').val() != '') {
        if ($('#chat_user').text() != 'a') {
            $('.chat_message').append("<div class=\"row\" style=\"margin: 0\">\n" +
                "                    <div class=\"col-xs-1 pull-right\" style=\"padding:0;height:40px;\">\n" +
                "                        <img src=\"/static/images/person.jpg\" style=\"border-radius: 50%;width:100%;height:100%;\">\n" +
                "                    </div>\n" +
                "                    <div class=\"col-xs-10 pull-right\" style=\"padding:0; overflow:hidden;\">\n" +
                "                        <div style='text-align: center'>&nbsp;&nbsp;<span id='time'>11:31:27</span></div>\n" +
                "                        <div class=\"pull-right\" style=\"background-color: rgb(239, 243, 246);height:30px;line-height:30px;border-radius: 5px;\">\n" +
                $('#input_message').val() +
                "                        </div>\n" +
                "                    </div>\n" +
                "                </div>"
            )
        } else {
            $('.chat_message').append("<div class=\"row\" style=\"margin: 0\">\n" +
                "                    <div class=\"col-xs-1 pull-right\" style=\"padding:0;height:40px;\">\n" +
                "                        <img src=\"/static/images/logo.jpg\" style=\"border-radius: 50%;width:100%;height:100%;\">\n" +
                "                    </div>\n" +
                "                    <div class=\"col-xs-10 pull-right\" style=\"padding:0; overflow:hidden;\">\n" +
                "                        <div style='text-align: center'>&nbsp;&nbsp;<span id='time'>11:31:27</span></div>\n" +
                "                        <div class=\"pull-right\" style=\"background-color: rgb(239, 243, 246);height:30px;line-height:30px;border-radius: 5px;\">\n" +
                $('#input_message').val() +
                "                        </div>\n" +
                "                    </div>\n" +
                "                </div>"
            )
        };

        var time = new Date();
        //console.log(time.toLocaleTimeString())
        $('#time').text(time.toLocaleString());
        $.get('/chat/update/', {'message': $('#input_message').val(), 'user': $('#chat_user').text(), 'to': $('#to').text()}, function () {});
        $('#input_message').val("");
    }
});

//更新数据
setInterval(function(){
    $.get('/chat/change/', {'user': $('#chat_user').text(), 'to': $('#to').text()}, function(data){
        if(data){
            if(data.who_send == '1'){

                $('.chat_message').append("<div class=\"row\" style=\"margin: 0\">\n" +
                        "                    <div class=\"col-xs-1\" style=\"padding:0;height:40px;\">\n" +
                        "                        <img src=\"/static/images/logo.jpg\" style=\"border-radius: 50%;width:100%;height:100%;\">\n" +
                        "                    </div>\n" +
                        "                    <div class=\"col-xs-10 \" style=\"padding:0; overflow:hidden;\">\n" +
                        "                        <div style='text-align: center'>&nbsp;&nbsp;<span id='time'>" + data.date + "</span></div>\n" +
                        "                        <div class=\"pull-left\" style=\"background-color: rgb(239, 243, 246);height:30px;line-height:30px;border-radius: 5px;\">\n" +
                        data.content +
                        "                        </div>\n" +
                        "                    </div>\n" +
                        "                </div>"
                    );


                console.log("这个是客户端的")
            }

            if(data.who_send == '0' ){

                $('.chat_message').append("<div class=\"row\" style=\"margin: 0\">\n" +
                        "                    <div class=\"col-xs-1\" style=\"padding:0;height:40px;\">\n" +
                        "                        <img src=\"/static/images/person.jpg\" style=\"border-radius: 50%;width:100%;height:100%;\">\n" +
                        "                    </div>\n" +
                        "                    <div class=\"col-xs-10 \" style=\"padding:0; overflow:hidden;\">\n" +
                        "                        <div style='text-align: center'>&nbsp;&nbsp;<span id='time'>" + data.date + "</span></div>\n" +
                        "                        <div class=\"pull-left\" style=\"background-color: rgb(239, 243, 246);height:30px;line-height:30px;border-radius: 5px;\">\n" +
                        data.content +
                        "                        </div>\n" +
                        "                    </div>\n" +
                        "                </div>"
                    );

                console.log("这个是服务端的")
            }


        }
    })
}, 1000);