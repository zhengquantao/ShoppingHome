from django.db import models


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

# 已支付订单
class Pay(models.Model):
    id = models.IntegerField(primary_key=True)
    date = models.DateTimeField(auto_now_add=True)
    l_number = models.CharField(max_length=16, db_index=True, default='')
    name = models.CharField(max_length=32, default='')
    color = models.CharField(max_length=8, default='')
    price = models.DecimalField(max_digits=8, decimal_places=2, default='')
    count = models.IntegerField(default='')
    su_choice = (('1', '1'), ('0', '0'))
    success = models.CharField(max_length=10, choices=su_choice)


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
    comment = models.ForeignKey(to='Comment', to_field='content', null=True)


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