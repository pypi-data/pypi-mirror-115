#coding=utf-8
#auther=DD
#date=2021.8.4 21:40

import requests

#DD严格意义上的第一个类诞生了
#天气查询类
class Future():
    def __init__(self, city):
        '''

        :param city: 要查询的城市名(str)
        '''
        self.response = requests.get(
            url='https://apis.juhe.cn/simpleWeather/query',
            params={
                'city': city,
                "key": "79f5c61eac3185e23ef675b454036e10"
            }
        ).json()
        self.a  = 1
        self.aim_list = []
        self.result = self.response['result']
        self.future = self.result.get('future')
        for self.i in self.future:
            self.i.pop('wid')
            for self.k in self.i:
                self.aim = self.i[self.k]
                self.aim_list.append(self.aim)
        for self.i in self.aim_list:
            if self.a == 4:
                print('\n' + '--------------' + '\n')
                self.a = 1
            else:
                print(self.i)
                self.a += 1

#一下为天气查询类的使用借鉴
#
# print('！！！欢迎使用DD天气查询程序！！！')
# while True:
#     a = input('是否要查询天气（是或否）>>>')
#     if a == '是':
#         city = input('请输入要查询的城市>>>')
#         print('以下为{}近几天的天气预报:'.format(city))
#         print('')
#         f = Future(city=city)
#     elif a == '否':
#         print('！！！感谢使用！！！')
#         print('--DD程序--')
#         break
#     else:
#         print('----请输入正确指令----')
#         continue