from stark.service.v1 import site
from app01 import models

class DepartHandler(object):

    def list_view(self, request):


site.register(models.Depart)
site.register(models.User)