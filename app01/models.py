from django.db import models

# Create your models here.
class Depart(models.Model):
    """
    Department table
    """
    title = models.CharField(verbose_name="部门名称", max_length=32)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """
    User table
    """
    name = models.CharField(max_length=32, verbose_name="姓名")
    gender_choices = (
        (1, '男'),
        (2, "女")
    )
    gender = models.IntegerField(verbose_name="性别", choices=gender_choices, default=1)
    age = models.CharField(max_length=32, verbose_name="年龄")
    email = models.EmailField(verbose_name="邮箱")
    depart = models.ForeignKey(to=Depart, verbose_name="部门", on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name
