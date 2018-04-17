import requests
import json
from Mxshop import settings
class YunPian():
    def __init__(self,api_key):
        self.api_key = api_key
        self.sing_send_url = 'https://sms.yunpian.com/v2/sms/single_send.json'
    def send_sms(self,code,mobile):
        parmas = {
            'apikey':self.api_key,
            'mobile':mobile,
            'code':code,
            'text':'haha,you code is {code}'.format(code=code)
        }
        response = requests.post(self.sing_send_url,data = parmas)
        re_dict = json.loads(response.text)
        # json.load(filename)从文件加载
        # json.loadds(string)从内存加载
        return re_dict

if __name__ == '__main__':
    #首先在云片网设置里添加服务器ip,查ip-->百度（本地ip）
    # print(settings.APIKEY)
    # exit()
    yun_pian = YunPian(settings.REGEX_MOBILE)
    yun_pian.send_sms('2017','18895326641')

