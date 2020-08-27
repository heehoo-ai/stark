from django.db import models

# Create your models here.
class Depart(models.Model):
    """
    Department table
    """
    title = models.CharField(verbose_name="部门名称", max_length=32)


class User(models.Model):
    """
    User table
    """
    name = models.CharField(max_length=32, verbose_name="姓名")
    age = models.CharField(max_length=32, verbose_name="年龄")
    email = models.EmailField(verbose_name="邮箱")
    depart = models.ForeignKey(to=Depart, verbose_name="部门", on_delete=models.DO_NOTHING)
