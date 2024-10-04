from django.db import models

# Create your models here.
class NewContact(models.Model):
    department = models.CharField(verbose_name="部门", max_length=16)
    name = models.CharField(verbose_name="姓名", max_length=16)
    student_id = models.CharField(verbose_name="学号", max_length=16)
    phone = models.CharField(verbose_name="手机", max_length=12)
    major = models.CharField(verbose_name="专业", max_length=12)
    dorm = models.CharField(verbose_name="寝室号", max_length=16, null=True, blank=True)
    birthday = models.DateTimeField(verbose_name="出生日期", null=True, blank=True)
    home = models.CharField(verbose_name="家乡", max_length=10, null=True, blank=True)
    qq = models.CharField(verbose_name="QQ", max_length=16, null=True, blank=True)
    wechat = models.CharField(verbose_name="微信", max_length=30, null=True, blank=True)
    email = models.CharField(verbose_name="邮箱", max_length=30, null=True, blank=True)
    hobby = models.CharField(verbose_name="爱好（除天文）", max_length=50, null=True, blank=True)
    skill = models.CharField(verbose_name="技能点", max_length=50, null=True, blank=True)
    comment = models.CharField(verbose_name="备注", max_length=50, null=True, blank=True)

class AllContact(models.Model):
    department = models.CharField(verbose_name="部门", max_length=16)
    name = models.CharField(verbose_name="姓名", max_length=16)
    student_id = models.CharField(verbose_name="学号", max_length=16)
    phone = models.CharField(verbose_name="手机", max_length=12)
    major = models.CharField(verbose_name="专业", max_length=12)
    birthday = models.DateTimeField(verbose_name="出生日期", null=True, blank=True)
    home = models.CharField(verbose_name="家乡", max_length=10, null=True, blank=True)
    qq = models.CharField(verbose_name="QQ", max_length=16, null=True, blank=True)
    wechat = models.CharField(verbose_name="微信", max_length=30, null=True, blank=True)
    email = models.CharField(verbose_name="邮箱", max_length=30, null=True, blank=True)

class User(models.Model):
    user_name = models.CharField(verbose_name="用户名", max_length=20)
    password = models.CharField(verbose_name="密码", max_length=32)
    admin_choices = ((1, "普通用户"), (2, "管理员"))
    admin = models.SmallIntegerField(verbose_name="权限", choices=admin_choices, default=0)

class Masterpiece(models.Model):
    author = models.CharField(verbose_name="作者", max_length=20)
    description = models.TextField(verbose_name="简介")
    url = models.CharField(verbose_name="文件名", max_length=40)

class Tutorial(models.Model):
    title = models.CharField(verbose_name="标题", max_length=20)
    author = models.CharField(verbose_name="作者", max_length=10)
    img_url = models.CharField(verbose_name="封面图片路径", max_length=40)
    url = models.CharField(verbose_name="根目录", max_length=40)