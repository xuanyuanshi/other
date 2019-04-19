import configparser
import requests
import xlrd
import xlsxwriter
import cx_Oracle


def request(url, header, body):
    rsp = requests.post(url, headers=header, json=body)
    return rsp


def getdata():
    rk = xlrd.open_workbook('../testcase/testcase.xlsx')
    st = rk.sheet_by_index(0)
    rows = st.nrows
    cols = st.ncols
    data = []
    for i in range(1, rows):
        data_rows = []
        for j in range(cols):
            d = st.cell(i, j).value
            if j == 0:
                if d == 'off':
                    break
            data_rows.append(d)
        if data_rows:
            data.append(data_rows)
    return data


def read_config(section, key):
    # 实例化ConfigParser对象
    config = configparser.ConfigParser()
    path = 'config/config.ini'
    # 读取config.ini文件
    config.read(path, encoding='UTF-8')
    return config.get(section, key)


def check(content, exception):
    # for k in exception:
    assert content == exception


def connect_oracle(sql):
    db = cx_Oracle.connect('db_blue_bull', 'db_blue_bull', '10.141.8.212/test212')
    cr = db.cursor()
    cr.execute(sql)
    rs = cr.fetchall()
    return rs


def get_loan_value(loan, name):
    value = loan.config.get("loan", name)
    return value


if __name__ == "__main__":
    data = getdata()
    print(data)
