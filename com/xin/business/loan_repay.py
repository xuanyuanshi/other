import json
from com.xin.tools.tools import read_config, request

'''全部业务均在mock环境进行，放款时间自己设置

'''


# 借款并还款
def loan_repay():
    global header
    header = json.loads(read_config('header', 'header'))

    # 获取借款接口请求参数url和data，并修改data使之符合用例要求
    url_loan = read_config('url', 'apply_loan')
    data_loan = json.loads(read_config('data', 'loan'))
    data_loan["account_id"] = read_config('account_id', 'account_id1')
    data_loan["bank_card_number"] = read_config('bank_card_number', 'bank_card_number1')
    data_loan["principal"] = read_config('principal', 'principal1')
    data_loan["loan_term"] = read_config('loan_term', 'loan_term1')
    data_loan["lendInfo"]["lendTime"] = read_config('lendTime', 'lendTime1')

    # 借款并获取借款结果
    rsp_loan = json.loads(request(url_loan, data_loan, header).text)
    principal = int(data_loan["principal"])
    loan_term = int(data_loan["loan_term"])
    loan_id = rsp_loan["loan_id"]
    loan_status = rsp_loan["loan_status"]

    # 如果借款成功，根据是否逾期进行逾期还款和账户还款
    print(rsp_loan)
    if loan_status == 'S':
        print("借款成功，loan_id:%s,金额%d，%d期！" % (loan_id, principal, loan_term))

        # 逾期试算
        trial_method = read_config('trial_method', 'overdue')
        url_trial_repay_loan = read_config('url', 'trial_repay_loan')
        data_trial_repay_loan = json.loads(read_config('data', 'trial_repay_loan'))
        data_trial_repay_loan["loan_id"] = loan_id
        data_trial_repay_loan["trial_method"] = trial_method
        rsp_trial = json.loads(request(url_trial_repay_loan, data_trial_repay_loan, header).text)
        print(rsp_trial)
        total_unpaid = int(rsp_trial["total_unpaid"])

        # 如果total_unpaid>0则逾期
        if total_unpaid > 0:
            repay_type = read_config('repay_type', 'overdue')

            # 逾期还款，参数初始化
            url_repay_loan = read_config('url', 'repay_loan')
            data_repay_loan = json.loads(read_config('data', 'repay_loan'))
            data_repay_loan["repay_type"] = repay_type
            data_repay_loan["repay_amount"] = total_unpaid

            # 单笔还款
            rsp_repay_loan = json.loads(request(url_repay_loan, data_repay_loan, header).text)
            pay_status = rsp_repay_loan["repayInfo"]["payStatus"]
            loan_id = rsp_repay_loan["loan_id"]
            pay = rsp_repay_loan["repayInfo"]["pay"]
            if pay_status == 'S':
                print("借款单%s逾期还款成功%d元！" % (loan_id, pay))
            else:
                print("逾期还款失败！")
                print(rsp_repay_loan)

        # 账户还款
        else:
            # 参数初始化
            url_repay = read_config('url', 'repay')
            data_repay = json.loads(read_config('data', 'repay'))
            account_id = data_repay["account_id"] = read_config('account_id', 'account_id1')
            data_repay["bank_card_number"] = read_config('bank_card_number', 'bank_card_number1')

            # 账户还款
            rsp_repay = json.loads(request(url_repay, data_repay, header).text)
            pay_status = rsp_repay["pay_status"]
            pay_amount = rsp_repay["pay_amount"]
            print(rsp_repay)
            if pay_status == 'S':
                print("%s账户还款成功,还款%d元" % (account_id, pay_amount))
            else:
                print("%s账户未还款，原因是“%s”" % (account_id, rsp_repay["retMsg"]))
    else:
        print("借款失败！")
        print(rsp_loan)


# 还款
def only_repay():
    global header
    header = json.loads(read_config('header', 'header'))
    # 逾期试算，参数初始化
    url_trial_repay_loan = read_config('url', 'trial_repay_loan')
    data_trial_repay_loan = json.loads(read_config('data', 'trial_repay_loan'))
    data_trial_repay_loan["loan_id"] = read_config('loan_id', 'loan_id1')
    data_trial_repay_loan["trial_method"] = read_config('trial_method', 'overdue')

    # 试算
    rsp_trial_repay_loan = json.loads(request(
        url_trial_repay_loan, data_trial_repay_loan, header).text)
    total_unpaid = rsp_trial_repay_loan["total_unpaid"]

    # 如果逾期，进行单笔还款
    if total_unpaid > 0:

        # 参数初始化
        url_repay_loan = read_config('url', 'repay_loan')
        data_repay_loan = json.loads(read_config('data', 'repay_loan'))
        data_repay_loan["loan_id"] = data_trial_repay_loan["loan_id"]
        data_repay_loan["bank_card_number"] = read_config('bank_card_number', 'bank_card_number1')
        data_repay_loan["repay_type"] = read_config('repay_type', 'overdue')
        data_repay_loan["repay_amount"] = total_unpaid

        # 单笔还款
        rsp_repay_loan = json.loads(request(url_repay_loan, data_repay_loan, header).text)
        pay_status = rsp_repay_loan["repayInfo"]["payStatus"]
        loan_id = rsp_repay_loan["loan_id"]
        pay = rsp_repay_loan["repayInfo"]["pay"]
        if pay_status == 'S':
            print("借款单%s逾期还款成功%d元！" % (loan_id, pay))
        else:
            print("逾期还款失败！")
            print(rsp_repay_loan)
    else:
        # 账户还款，参数初始化
        url_repay = read_config('url', 'repay')
        data_repay = json.loads(read_config('data', 'repay'))
        account_id = data_repay["account_id"] = read_config('account_id', 'account_id1')
        data_repay["bank_card_number"] = read_config('bank_card_number', 'bank_card_number1')

        # 账户还款
        rsp_repay = json.loads(request(url_repay, data_repay, header).text)
        pay_status = rsp_repay["pay_status"]
        pay_amount = rsp_repay["pay_amount"]
        if pay_status == 'S':
            print("%s账户还款成功,还款%d元"%(account_id, pay_amount))
        else:
            print("%s账户未还款，原因是“%s”" % (account_id, rsp_repay["retMsg"]))


if __name__ == "__main__":
    loan_repay()

