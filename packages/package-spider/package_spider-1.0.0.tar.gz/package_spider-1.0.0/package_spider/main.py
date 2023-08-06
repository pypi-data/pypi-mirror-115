#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   main.py
@Time    :   2021/08/05 22:03:50
@Author  :   Owen fanfl
@Version :   1.0
@Contact :   fanfuliang@yudaotec.com
@License :   (C)Copyright 2018-2019, yudao
@Desc    :   None
'''

import itertools

case_list = ['用户名', '密码']
value_list = ['正确', '不正确', '特殊符号', '超过最大长度']

def gen_case(item=case_list, value=value_list):
    '''输出笛卡尔用例集合'''
    for i in itertools.product(item, value):
        print('输入'.join(i))

def test_print():
    print("欢迎搜索关注公众号: 「测试开发技术」!")
    gen_case()
       
        

if __name__ == '__main__':
    test_print()
    # gen_case()