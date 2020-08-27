class StarkSite(object):
    def __init__(self):
        self._registry = []
        self.app_name = 'stark'
        self.namespace = 'stark'

    def register(self, model_class, handler_class):
        """

        :param model_class:是models中数据库相关类
        :param handler_class:处理请求的视图函数所在的类
        :return:
        """
        self._registry.append({'model_class': model_class, 'handler': handler_class(model_class)})
        """
        [
            {'model_class':models.Depart},
            {'model_class':models.User},
            {'model_class':models.Host},
        ]
        """


site = StarkSite()