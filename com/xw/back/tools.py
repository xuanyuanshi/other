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
    sql = 'select apply_id,batch_no "放款申请流水号",total_period "总期数",total_capital "总本金",total_interest "总利息",total_bank_interest "银行利息",paid_period "已还期号",current_period "当前期",paid_capital "已还本金",paid_interest "已还利息",paid_bank_interest "已还银行利息",paid_penalty_interest "已还罚息",paid_bank_penalty_interest "已还银行罚息",pending_capital "待还本金",pending_interest "待还利息",pending_bank_interest "代还银行利息",pending_penalty_interest "待还总罚息",pending_bank_penalty_interest "代还银行罚息",statement_day "还款日",loan_date "放款日期",settle_status "1为已结清2逾期3还款中4初始状态",settle_time,updated_at,request_pay_status "1为未申请支付,2正在申请支付,3支付完毕",created_at "创建时间",compensatory_status "0未代偿1为已代偿",compensatory_amount "代偿金额",last_pay_time "最近还款时间",request_pay_type "当前划扣类型 request_pay_type 0-没有划扣 1-正在自动 2-正在手动" from bs_xw_bank_order_pay where apply_id=25382681405;'
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



