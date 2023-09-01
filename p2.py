import requests
from lxml import etree
import random
import time
from selenium import webdriver
import base64
import base64
import re
import xml.etree.ElementTree as et
from fontTools.ttLib import TTFont
from fontTools.ttLib import TTFont
import xlwt
#字体反扒
# def fanpa1(content,html):
#     fontdata = re.findall("charset=utf-8;base64,(.*?)'\) format",html,re.S)[0]
#     fontent = base64.b64decode(fontdata)
#     f = open("t5.woff", 'wb')
#     f.write(fontent)
#     f.close()
#     fonts = TTFont('t5.woff')
#     fonts.saveXML('test8.xml')
#     root = et.parse('test8.xml').getroot()
#     con = root.find('cmap').find('cmap_format_4').findall('map')
#     for i in con:
#         names = i.attrib['name']
#         code = i.attrib['code'].replace('0x', '&#x') + ';'
#         c1 = re.findall(r'\d+', names)
#         c2 = str(int(c1[0]) - 1)
#         content = content.replace(code, c2)
#     return content
def fanpa1(content, html):
    fontdata = re.findall(r'base64,(.*?)\'\) format', html, re.S)
    if fontdata:
        fontent = base64.b64decode(fontdata[0])
        f = open("t5.woff", 'wb')
        f.write(fontent)
        f.close()
        # ... 其他处理字体的部分
        return content
    else:
        return content

#分析页面
def lxmldata(data):
    datas =etree.HTML(data)
    list1 = []
    date=datas.xpath("//div[@class='list-content']//div[@class='zu-itemmod']")
    for i,dates in enumerate (date):
        dict = {}
        #价格
        price1 = re.findall('<p><strong><b class="strongbox">(.*?)</b></strong> 元/月</p>', data, re.S)
        price = re.findall('<p><strong><b class="strongbox">(.*?)</b></strong> 元/月</p>', data, re.S)[i]
        #面积
        size = re.findall('<b class="strongbox" style="font-weight: normal;">(.*?)</b>', data, re.S)[2:len(price1)*3:3][i]
        #房屋结构
        fangjian1 = re.findall('<b class="strongbox" style="font-weight: normal;">(.*?)</b>', data, re.S)[0:len(price1)*3:3][i]
        fangjian2 = re.findall('<b class="strongbox" style="font-weight: normal;">(.*?)</b>', data, re.S)[1:len(price1)*3:3][i]
        #详细标题
        title=dates.xpath(".//div[@class='zu-info']//b/text()")
        #名称
        map = dates.xpath(".//address[@class='details-item']/a/text()")
        #具体位置
        local = dates.xpath(".//address[@class='details-item']/text()")
        local = [x.strip() for x in local]
        #装修情况
        zhuangxiu = dates.xpath(".//p[@class='details-item bot-tag']//span[@class='cls-1']/text()")+dates.xpath(".//p[@class='details-item bot-tag']/span[@class='cls-2']/text()")+dates.xpath(".//p[@class='details-item bot-tag']/span[@class='cls-3']/text()")
        dict['价格']=str(fanpa1(price,data))+'元/月'
        dict['面积']=str(fanpa1(size,data))+'平方米'
        dict["详细标题"]=title[0]
        dict['名称']=map[0]
        dict["具体位置"]=local[1]
        dict['房间结构']=fanpa1(fangjian1,data)+'室'+fanpa1(fangjian2,data)+'厅'
        if len(zhuangxiu)==3:
            dict["装修情况"]=zhuangxiu[0]+','+zhuangxiu[1]+','+zhuangxiu[2]
        elif len(zhuangxiu)==2:
            dict["装修情况"]=zhuangxiu[0]+','+zhuangxiu[1]
        else:
            dict["装修情况"] = zhuangxiu[0]
        list1.append(dict)
    return list1
def save(list):
    filename = r"C:\Users\Admin\Desktop\p.xls"
    book = xlwt.Workbook()
    sheet1=book.add_sheet("sheet1")
    header = ['价格','面积','详细标题','名称','具体位置','装修情况']
    for i in range(len(header)):
        sheet1.write(0,i,header[i])
    j = 1
    for i in list:
        sheet1.write(j,0,i['价格'])
        sheet1.write(j,1,i['面积'])
        sheet1.write(j,2,i['详细标题'])
        sheet1.write(j,3,i['名称'])
        sheet1.write(j,4,i['具体位置'])

        sheet1.write(j,5,i['装修情况'])
        j = j+1
    book.save(filename)
    print("写入成功")

if __name__ == '__main__':
    headers = {
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        "cookie":"aQQ_ajkguid=C1CC68B8-4D19-287F-3644-2D367108DEC0; id58=e87rkF/LkOJmpXJnEm4JAg==; 58tj_uuid=a6d935e2-5506-4369-9370-d4081b424818; ctid=49; _ga=GA1.2.1998955085.1607386984; _gid=GA1.2.1925540573.1607386984; new_uv=2; als=0; cmctid=2053; wmda_new_uuid=1; wmda_uuid=aa760fc62c405eecb84c273b7206beed; wmda_visited_projects=%3B6289197098934; xxzl_cid=090b7011f13f44c8b3d9271ce16587b3; xzuid=ad62da25-6302-4e3e-992e-eea22f2d9d02; lps=https%3A%2F%2Fhai.zu.anjuke.com%2Ffangyuan%2Fp2%2F%3Ffrom_price%3D0%26to_price%3D2500an%7Chttps%3A%2F%2Fcallback.58.com%2F; wmda_session_id_6289197098934=1607426591062-bdd0135e-4c1f-a60c; xzfzqtoken=lbhfULbvUI2tmDmR%2By8o2XgL%2FoD%2Fi8pTDHftNbKQZZ3J9dDc2%2BiE91mVlKbcur5Hin35brBb%2F%2FeSODvMgkQULA%3D%3D",
        "path":"/fangyuan/p2/?from_price=0&to_price=2500an"
    }
    dict2 = []
    dict1 = []
    for i in range(200):
        url = "https://su.zu.anjuke.com/fangyuan/p{}/".format(i+1)
        response=requests.get(url=url,headers=headers).content.decode('utf-8')
        list=lxmldata(response)
        dict1.append(list)
        print("第"+str(i)+"页数据完成")
    for j in dict1:
        for k in j:
            dict2.append(k)
    save(dict2)
