from django.db import models

# Create your models here.
class Host(models.Model):
    """
    Host table
    """
    host = models.CharField(verbose_name="主机名", max_length=32)
    ip = models.GenericIPAddressField(verbose_name="IP")

    def __str__(self):
        return self.host


class Role(models.Model):
    """
    角色
    """
    title = models.CharField(verbose_name='角色名称', max_length=32)

    class Meta:
        verbose_name = "角色"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Project(models.Model):
    """
    项目表
    """
    title = models.CharField(verbose_name='项目名称', max_length=32)
    server = models.ForeignKey(to=Host, verbose_name="服务器", max_length=32, on_delete=models.DO_NOTHING)
    status_choices = (
        (1, '在建'),
        (2, "验收")
    )
    status = models.IntegerField(verbose_name="状态", choices=status_choices, default=1)
