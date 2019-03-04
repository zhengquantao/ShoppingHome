from django.db import models


class UserInfo(models.Model):
    num = models.AutoField(primary_key=True)
    name = models.CharField(max_length=16)
    password = models.CharField(max_length=40)
    nickname = models.CharField(max_length=16)
    sex_choice = (('男', 'man'), ('女', 'women'))
    sex = models.CharField(max_length=10, choices=sex_choice)
    settime = models.DateTimeField(auto_now_add=True)
    addr = models.CharField(max_length=32, default='')
    email = models.CharField(max_length=32, default='')
    phone = models.CharField(max_length=11, default='')
    receiver = models.CharField(max_length=64, default='')

    # blog = models.ManyToManyField(to="Address", to_field="name", null=True)


# class Address(models.Model):
#     receiver = models.CharField(max_length=16)
#     address = models.CharField(max_length=64)
#     code = models.CharField(max_length=16)
#     phone = models.CharField(max_length=11)
