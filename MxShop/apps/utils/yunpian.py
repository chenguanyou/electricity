# coding=utf-8
import json
import requests


class YunPian_Sms(object):
    '''
    短信发送功能：
    api_key:
    url:
    parameter:
        apikey:
        mobile:
        text:
    '''

    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"

    def sendout_sms(self, mobile, code):
        parameter = {
            'apikey': self.api_key,
            'mobile': mobile,
            'text': "【書劍博客】您的验证码是%s。如非本人操作，请忽略本短信" % code
        }
        send_post = requests.post(self.single_send_url, data=parameter)
        # print("提示信息：" + send_post.json()["msg"])
        # print(send_post.json())
        return send_post.json()

if __name__ == "__main__":
    test_sms = YunPian_Sms("d198cf40b5c7bc81850cb5bbfe69659d")
    test_sms.sendout_sms("18611662860", "2018")
