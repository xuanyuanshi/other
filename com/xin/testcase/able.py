import xlrd
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
            if j == 1:
                if d == 'off':
                    break
            data_rows.append(d)
        if data_rows:
            data.append(data_rows)
    return data
data = getdata()
print(data)
