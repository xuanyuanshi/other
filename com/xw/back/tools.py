# coding=gbk
import requests, json, xlrd
import MySQLdb


def request(url, header, body):
    rsp = requests.post(url, headers=header, data=body)
    return rsp


# rsp = request(url, header, data)

def getpara():
    rk = xlrd.open_workbook('testcase_api.xlsx')
    st = rk.sheet_by_index(0)
    rows = st.nrows
    cols = st.ncols
    data = []

    for i in range(1, rows):
        data_rows = []
        for j in range(cols):
            cell = st.cell(i, j).value
            if j == 0:
                if cell == 'off':
                    break
            data_rows.append(cell)
        if data_rows:
            data.append(data_rows)
    return data


def getdata():
    conn = MySQLdb.connect(
        host='10.141.8.33',
        port=3306,
        user='banksns',
        passwd='RdNdVoLWpMwuXEq1',
        db='banksns',
        charset='utf8'
    )
    cur = conn.cursor()
    sql = 'select apply_id,batch_no "�ſ�������ˮ��",total_period "������",total_capital "�ܱ���",total_interest "����Ϣ",total_bank_interest "������Ϣ",paid_period "�ѻ��ں�",current_period "��ǰ��",paid_capital "�ѻ�����",paid_interest "�ѻ���Ϣ",paid_bank_interest "�ѻ�������Ϣ",paid_penalty_interest "�ѻ���Ϣ",paid_bank_penalty_interest "�ѻ����з�Ϣ",pending_capital "��������",pending_interest "������Ϣ",pending_bank_interest "����������Ϣ",pending_penalty_interest "�����ܷ�Ϣ",pending_bank_penalty_interest "�������з�Ϣ",statement_day "������",loan_date "�ſ�����",settle_status "1Ϊ�ѽ���2����3������4��ʼ״̬",settle_time,updated_at,request_pay_status "1Ϊδ����֧��,2��������֧��,3֧�����",created_at "����ʱ��",compensatory_status "0δ����1Ϊ�Ѵ���",compensatory_amount "�������",last_pay_time "�������ʱ��",request_pay_type "��ǰ�������� request_pay_type 0-û�л��� 1-�����Զ� 2-�����ֶ�" from bs_xw_bank_order_pay where apply_id=25382681405;'
    # sql = 'select apply_id,batch_no,total_period,total_capital,total_interest,total_bank_interest,paid_period,current_period,paid_capital,paid_interest,paid_bank_interest,paid_penalty_interest,paid_bank_penalty_interest,pending_capital,pending_interest,pending_bank_interest,pending_penalty_interest,pending_bank_penalty_interest,statement_day,loan_date,settle_status,settle_time,updated_at,request_pay_status,created_at,compensatory_status,compensatory_amount,last_pay_time,request_pay_type from bs_xw_bank_order_pay where apply_id=25382681405;'

    cur.execute(sql)
    res = cur.fetchall()
    cur.close()
    conn.close()
    return res


if __name__ == '__main__':
    res = getdata()
    res_ = []
    for i in range(len(res[0])):
        res_.append(res[0][i])
    print(res_)



