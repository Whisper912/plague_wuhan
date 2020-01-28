from urllib import request
from bs4 import BeautifulSoup
import re
# 别忘了请求头（headers），以防万一
user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0"
headers = {"User-Agent": user_agent}
# 爬取网站地址，我爬的是网易的
req = request.Request("http://wjw.beijing.gov.cn/wjwh/ztzl/xxgzbd/",headers=headers)
resp = request.urlopen(req)
# 打开页面
html = resp.read()
# 输出编码后的结果（编码为GBK），可有可无
# print(html)
soup = BeautifulSoup(html, 'html.parser')
# print(soup.prettify())
new_a = soup.find(class_ = 'weinei_left_con_line_text');
print(new_a);

# def parseDom(dom):
