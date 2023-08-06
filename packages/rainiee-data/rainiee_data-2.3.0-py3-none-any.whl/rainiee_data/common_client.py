from functools import partial

class CommonClient(object):

    def __init__(self, data_pro):
        self.data_pro = data_pro

    def query(self,api_name,**kwargs):
        return self.data_pro.get_rainiee_client().query(api_name, 'POST', req_param = kwargs)

    def __getattr__(self, name):
        return partial(self.query, api_name=name)