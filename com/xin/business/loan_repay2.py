# /bin/usr/python
# coding:utf-8
import xlrd
import json
import pytest
import allure
import os
from com.xin.tools.tools import request,getdata,check
# 借款-还款
data = getdata()


@pytest.mark.parametrize('id,_,testcase,method,url,uri,header,body,exception', data)
def test_loan_repay(id, _, testcase, method, url, uri, header, body, exception):
    allure.attach('测试用例', testcase)
    url = url + uri
    body = json.loads(body)
    header = json.loads(header)
    rsp = request(url, body, header)
    content = rsp.json()["loan_status"]
    d = 'S'
    # exception = json.loads(exception)
    # print('exception is %s'%exception)
    check(content, d)


if __name__ == "__main__":
    os.system("pytest loan_repay2.py --alluredir allure-report")
    os.system("allure serve allure-report")


