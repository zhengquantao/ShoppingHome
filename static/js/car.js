
/**
 *   page : shoppingCar.html
 */

//点击减号
$('.reduce_btn').click(function(){

    if(parseInt($(this).next('.num_input').val())==0){
        console.log(this)
        $(this).next('.num_input').val(0)
    }else{
        var reduce = parseInt($(this).next('.num_input').val())-1;
        $(this).next('.num_input').val(reduce);
        //小计变化
         $(this).parent().next('.items_price').text(parseInt($(this).next('.num_input').val()) * parseInt($(this).parent().prev('.item_price').text()));
           al()
    }
});

//点击加号
$('.add_num_btn').click(function(){
    var add = parseInt($(this).prev('.num_input').val())+1;
    $(this).prev('.num_input').val(add);
    //小计变化
    $(this).parent().next('.items_price').text(parseInt($(this).prev('.num_input').val()) * parseInt($(this).parent().prev('.item_price').text()));
      al()
});

//手动输入
$('.num_input').blur(function () {
    //小计变化
    $(this).parent().next('.items_price').text(parseInt($(this).val()) * parseInt($(this).parent().prev('.item_price').text()));
});

//获取checkbox框的状态
console.log("=======", $('.checkbox').is(':checked'));

var $items_price = $('td').siblings('.items_price');//小计

//加载时的总价
function al(){
    var all_price = 0;
    for (var i=0; i<$items_price.length; i++){
        if($('.checkbox').eq(i).is(':checked')==true){
            all_price += parseInt($items_price.eq(i).text());
        }
    }
    $('#all_price').text(all_price);
}
al();

//点击价格时价格的变动
$('.checkbox').change(function(){
    var all_price = 0;
    for (var i=0; i<$items_price.length; i++){
        if($('.checkbox').eq(i).is(':checked')==true){
        all_price += parseInt($items_price.eq(i).text());
        }
    }
    $('#all_price').text(all_price);
})


//点击删除按钮
$('.car_delete_btn').click(function(){
    console.log('ok')
    $(this).parent().parent().remove();

})



//点击购买框  触发的事件
$('#car_button').click(function () {
    console.log('5555')
});

