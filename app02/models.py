from django.db import models

# Create your models here.
class Host(models.Model):
    """
    Host table
    """
    host = models.CharField(verbose_name="主机名", max_length=32)
    ip = models.GenericIPAddressField(verbose_name="IP")