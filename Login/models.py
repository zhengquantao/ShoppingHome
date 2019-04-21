from django.db import models
# from Business.models import Binfo


# 用户表
class UserInfo(models.Model):
    num = models.AutoField(primary_key=True)
    name = models.CharField(max_length=16, unique=True, db_index=True)
    password = models.CharField(max_length=40)
    nickname = models.CharField(max_length=16)
    sex_choice = (('男', 'man'), ('女', 'women'))
    sex = models.CharField(max_length=10, choices=sex_choice)
    settime = models.DateTimeField(auto_now_add=True)
    addr = models.CharField(max_length=32, default='')
    email = models.CharField(max_length=32, default='')
    phone = models.CharField(max_length=11, default='')
    receiver = models.CharField(max_length=64, default='')
    code = models.CharField(max_length=6, default='')
    comment = models.ForeignKey(to="Comment", to_field='id', null=True)
    # car = models.ForeignKey(to="Car", to_field='id', null=True)


# 购物车
class Car(models.Model):
    # id = models.AutoField(primary_key=True)
    # date = models.DateTimeField(auto_now_add=True)
    # l_number = models.CharField(max_length=16, db_index=True, default='')
    # name = models.CharField(max_length=32, default='')
    # color = models.CharField(max_length=8, default='')
    # price = models.DecimalField(max_digits=8, decimal_places=2, default='')
    # img_url = models.CharField(max_length=200, default='')
    count = models.IntegerField(default='')  # 数量
    user = models.ForeignKey(to='UserInfo', to_field='name', null=True)
    class_item = models.ForeignKey(to='ClassList', to_field='l_number', null=True)


# 商品种类表
class AllClass(models.Model):
    number = models.CharField(max_length=16, db_index=True, default='')
    name = models.CharField(max_length=32, default='')
    classlist = models.ForeignKey(to="ClassList", to_field="l_number", null=True)


# 商品表
class ClassList(models.Model):
    l_number = models.CharField(max_length=16, db_index=True, unique=True, default='')
    name = models.CharField(max_length=32, default='')
    img_url = models.CharField(max_length=200, default='')
    color = models.CharField(max_length=8, default='')
    price = models.DecimalField(max_digits=8, decimal_places=2, default='')
    count = models.IntegerField(default='')
    see_nums = models.IntegerField(default='0')
    pay_nums = models.IntegerField(default='0')
    comment = models.ForeignKey(to='Comment', to_field='content', null=True)


# 统计访问量表
class VCount(models.Model):
    classlist = models.ForeignKey(to='ClassList', to_field='l_number', null=True)
    see_num = models.IntegerField(default='0')
    pay_num = models.IntegerField(default='0')


# 评论表
class Comment(models.Model):
    id = models.IntegerField(primary_key=True)
    content = models.CharField(max_length=126, unique=True, default='')


# 广告栏
class Ad(models.Model):
    id = models.CharField(max_length=16, default='', primary_key=True)
    name = models.CharField(max_length=16, default='')
    img_url = models.CharField(max_length=300, default='')
    classlist = models.OneToOneField(to='ClassList', to_field='l_number', null=True)


# 已支付订单
class Pay(models.Model):
    p_user = models.ForeignKey(to='UserInfo', to_field='name', null=True)
    c_item = models.ForeignKey(to='ClassList', to_field='l_number', null=True)
    count = models.IntegerField(default='')
    trade_no = models.CharField(max_length=16, null=True)
    su_choice = (('1', '已支付'), ('0', '未支付'))
    success = models.CharField(max_length=10, choices=su_choice, default=0)


# 物流表
class Logistics(models.Model):
    pass


# 商家订单表
class Border(models.Model):
    pay = models.ForeignKey(to='Pay', null=True)
    logistics = models.ForeignKey(to='Logistics', null=True)
    bdate = models.DateTimeField(auto_now_add=True)
    item_no = models.CharField(max_length=16, null=True, default='')


# 商家表
class Binfo(models.Model):
    name = models.CharField(max_length=16, unique=True)
    password = models.CharField(max_length=64)


# 聊天表
class Chat(models.Model):
    bid = models.ForeignKey(to='Binfo', null=True)
    uid = models.ForeignKey(to='UserInfo', null=True)
    content = models.CharField(max_length=200, null=True, default='')
    date = models.DateTimeField(auto_now_add=True)
    who_choice = (('1', '商家'), ('0', '用户'))  # 商家发的是1 ， 非商家是0
    who_send = models.CharField(max_length=10, choices=who_choice, default=0)
    su_choice = (('1', '已读'), ('0', '未读'))
    sign = models.CharField(max_length=10, choices=su_choice, default=0)


# 商品主评论表
class MComment(models.Model):
    id = models.AutoField(primary_key=True)
    cid = models.CharField(max_length=64, unique=True, null=True)
    uname = models.ForeignKey(to='UserInfo', to_field='name', null=True)
    number = models.ForeignKey(to='ClassList', to_field='l_number',  null=True)
    dComment = models.CharField(max_length=1000, null=True)
    date = models.DateTimeField(auto_now_add=True)


# 子评论表
class CComment(models.Model):
    cname = models.CharField(max_length=64, unique=True, null=True)
    cComment = models.CharField(max_length=1000, null=True, default='')
    date = models.DateTimeField(auto_now_add=True)


# 总表
class AComment(models.Model):
    uname = models.ForeignKey(to='MComment', null=True)
    cname = models.ForeignKey(to='CComment', to_field='cname', null=True)


# 优惠劵表
class Ticket(models.Model):
    tName = models.CharField(max_length=64, null=True, default='')
    tPrice = models.IntegerField(default='', null=True)
    tDescribe = models.CharField(max_length=128, null=True, default='')
    tDate = models.DateTimeField(null=True, default='')
    tCount = models.IntegerField(null=True, default='')
    user = models.ForeignKey(to='UserInfo', to_field='num', on_delete=models.SET_NULL, null=True)


# 秒杀商品
class SecKill(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    # count = models.IntegerField(null=True)
    startTime = models.DateTimeField(null=True)
    endTime = models.DateTimeField(null=True)
    goods = models.ForeignKey(to='ClassList', to_field='l_number')

