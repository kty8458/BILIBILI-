from selenium.webdriver import Chrome
from time import sleep
from selenium.webdriver.chrome.options import Options
from matplotlib import pyplot as plt
import xlrd
import pprint
import xlwt

def get_uids():
    data = xlrd.open_workbook('test.xls')
    table = data.sheets()[0]
    uids = table.col_values(0)
    del uids[0]
    return uids

def get_data(uids):
    user_list = []
    for uid in uids:
        opt = Options()
        opt.add_argument("--headless")
        opt.add_argument("--disable-gup")
        web = Chrome(options = opt)
        url_root=('https://space.bilibili.com/')
        url = url_root+uid
        web.get(url)
        sleep(1)
        try:
            gz = web.find_element_by_id('n-gz').text
        except:
            gz = "None"
        try:        
            fs = web.find_element_by_id('n-fs').text
        except:
            fs = 'None'
        try:
            vip = web.find_element_by_xpath('//*[@id="app"]/div[1]/div[1]/div[2]/div[2]/div/div[2]/div[1]/a[2]').text
            if vip =='':
                vip = '普通'
        except:
            vip = 'None'
        user = {}
        user["uid"] = uid
        user["关注数"] = gz
        user["粉丝数"] = fs
        user["会员类型"] = vip
        user_list.append(user)
        web.close()
        # pprint.pprint(user_list)
    return user_list

def save_data(user_list):
    workbook=xlwt.Workbook('test.xls')
    worksheet=workbook.add_sheet('test')
    worksheet.write(0,0,'UID')
    worksheet.write(0,1,'粉丝数')
    worksheet.write(0,2,'关注数')
    worksheet.write(0,3,'会员类型')
    
    for i in range(len(user_list)):
        value = list(user_list[i].values())
        for j in range(4):
            worksheet.write(i+1,j,value[j])
    workbook.save('test.xls')

uids = get_uids()
user_list = get_data(uids)
save_data(user_list)
