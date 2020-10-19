import requests
from bs4 import BeautifulSoup
import os
import time

# 服务器反爬虫机制会判断客户端请求头中的User-Agent是否来源于真实浏览器，所以，我们使用Requests经常会指定UA伪装成浏览器发起请求
headers = {'user-agent': 'Mozilla/5.0'}
bashUrl = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2019/"


# 写文件
def writedoc(ss, code, l):
    # 打开文件
    # 编码为utf-8
    with open("E:\\Python爬取的文件\\" + code + ".txt", 'a', encoding='utf-8') as f:
        # 写文件
        ss = ss + '\t' + str(l)
        f.write(ss + '\r\n')
        print(ss)


# 根据详细页面url获取目标字符串
def geturl(url, code, path, l):
    l = l + 1
    # 请求详细页面
    r = requests.get(url, headers=headers)
    # 改编码
    r.encoding = "GBK"
    soup = BeautifulSoup(r.text, "html.parser")
    # 找出类名为 info-zi mb15 下的所有p标签
    trs = soup.findAll('tr', {'class': {'countytr', 'citytr', 'towntr'}})
    # 用来储存最后需要写入文件的字符串
    for tr in trs:
        aas = tr.find_all("a")
        if len(aas) == 0:
            if l <= 5:
                tds = tr.find_all("td")
                td1 = tds[0]
                td2 = tds[1]
                mlist = str(td1.string) + "\t" + str(td2.string)
                writedoc(mlist, code, l)
        else:
            if l == 2:
                string_a_url = bashUrl + str(tr.a.get("href"))
                path_tmp = path
            if l == 3:
                string_a_url = bashUrl + path + str(tr.a.get("href"))
                path_tmp = path + str(tr.a.get("href")).split('/')[0] + '/'
            if l == 4:
                tds = tr.find_all("td")
                td1 = tds[0]
                td2 = tds[1]
                mlist = str(td1.a.string) + "\t" + str(td2.a.string)
                writedoc(mlist, code, l)
            if l == 5:
                string_a_url = bashUrl + path + str(tr.a.get("href"))
            if l < 4:
                time.sleep(3) # 休眠3秒
                geturl(string_a_url, code, path_tmp, l)
                tds = tr.find_all("td")
                td1 = tds[0]
                td2 = tds[1]
                mlist = str(td1.a.string) + "\t" + str(td2.a.string)
                writedoc(mlist, code, l)


# 获取目标网址
def getalldoc():
    # 字符串拼接成目标网址
    testurl = bashUrl + "index.html"
    # 使用request去get目标网址
    res = requests.get(testurl, headers=headers)
    # 更改网页编码--------不改会乱码
    res.encoding = "GBK"
    # 创建一个BeautifulSoup对象
    soup = BeautifulSoup(res.text, "html.parser")
    # 找出目标网址中所有的small标签
    # 函数返回的是一个list
    aas = soup.find_all("a")
    # 先创建目录
    mkdir("E:\\Python爬取的文件\\")
    for a in aas:
        string_a = a.next_element
        if string_a == '京ICP备05034670号':
            break
        path = str(a.get("href")).split('.')[0] + "/"
        l = 1
        string_aurl = bashUrl + str(a.get("href"))
        # 请求详细页面
        geturl(string_aurl, string_a, path, l)
        writedoc(string_a, string_a, l)
#    a = aas[3]
#    string_a = a.next_element
#    path = str(a.get("href")).split('.')[0] + "/"
#    l = 1
#    string_a_url = bashUrl + str(a.get("href"))
#    # 请求详细页面
#    geturl(string_a_url, string_a, path, l)
#    writedoc(string_a, string_a, l)




def mkdir(path):
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        return False


if __name__ == "__main__":
    getalldoc()
