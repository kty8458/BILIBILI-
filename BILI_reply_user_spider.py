from selenium.webdriver import Chrome
from time import sleep
from selenium.webdriver.chrome.options import Options
from matplotlib import pyplot as plt
import xlwt
#无头设置，不显示浏览器
opt = Options()
opt.add_argument("--headless")
opt.add_argument("--disable-gup")

web = Chrome(options=opt)
web.get("https://t.bilibili.com/528672278995406531?tab=2")

#滚动到底部
for i in range(10):
    web.execute_script("window.scrollTo(0,document.body.scrollHeight)") 
    print('working',i)
    sleep(0.5)

#定位user节点，爬取uid（a）和等级（i）
user_list = {}
user = web.find_elements_by_class_name('user')
count = 0
for item in user:
    uid = item.find_element_by_tag_name('a')
    level = item.find_element_by_tag_name('i')
    user_list[uid.get_attribute('data-usercard-mid')] = level.get_attribute('class')
    count += 1
Total_number = len(user_list)

#将所有uid根据等级分组
lv1 = []
lv2 = []
lv3 = []
lv4 = []
lv5 = []
lv6 = []
for user in user_list:
    if user_list[user] == "level l1":
        lv1.append(user)
    elif user_list[user] == "level l2":
        lv2.append(user)
    elif user_list[user] == "level l3":
        lv3.append(user)
    elif user_list[user] == "level l4":
        lv4.append(user)
    elif user_list[user] == "level l5":
        lv5.append(user)
    elif user_list[user] == "level l6":
        lv6.append(user)
all_user = [lv1,lv2,lv3,lv4,lv5,lv6]

workbook = xlwt.Workbook()
row = 0
worksheet = workbook.add_sheet('test')
worksheet.write(0,0,'UID')

for i in range(len(all_user)):
    for j in range(len(all_user[i])):
        worksheet.write(row+1,0,all_user[i][j])
        row += 1
workbook.save('test.xls')

plt.rcParams['font.sans-serif']=['SimHei'] #解决中文乱码
plt.figure(figsize=(6,9))#调节图形大小
labels = [u'lv1',u'lv2',u'lv3',u'lv4',u'lv5',u'lv6']
sizes = [len(lv1),len(lv2),len(lv3),len(lv4),len(lv5),len(lv6)]
colors = ['red','yellowgreen','lightskyblue','yellow','blue','orange','green']
explode = (0.1,0.05,0,0,0,0)#将某一块分割出来，值越大分割出的间隙越大
patches,text1,text2 = plt.pie(sizes,
                      explode=explode,
                      labels=labels,
                      colors=colors,
                      autopct = '%3.2f%%', #数值保留固定小数位
                      labeldistance = 1.2,#图例距圆心半径倍距离
                      shadow = False, #无阴影设置
                      startangle =90, #逆时针起始角度设置
                      pctdistance = 0.6) #数值距圆心半径倍数距离
#patches饼图的返回值，texts1饼图外label的文本，texts2饼图内部的文本
# x，y轴刻度设置一致，保证饼图为圆形
plt.axis('equal')
plt.title("用户等级分布，样本人数：%s"%(Total_number))
plt.legend()
plt.show()
web.close()

# print(user_list)
# print(count)