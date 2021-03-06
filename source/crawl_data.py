from urllib import request
from bs4 import BeautifulSoup, Tag
import json
import re

def getHref(url, dom):
    """
    获取文章的链接
    :param url: 文章列表
    :param dom: 待查找的dom
    :return: 文章链接
    """
    soup = getSoup(url)
    href: str = parseDom(dom, soup)

    # 返回链接，对相对链接进行拼接处理
    if href[0:3] == 'http':
        return href
    elif href[0] == '.':
        return url + href[2:len(href)]
    elif href[0] == '/':
        return url + href[1:len(href)]
    else:
        return url + href

def findSubClass(sub_dom: str, dom_list: list, tag: Tag):
    """
    按照class名查找子tag
    :param sub_dom: 要查找的字符串
    :param dom_list: 剩余字符串列表
    :param tag: 已找到的tag
    :return: 查找之后的新tag
    """
    tag = tag.findChild(class_=sub_dom)
    # 递归调用
    return processNext(dom_list, tag=tag)

def findSubName(sub_dom: str, dom_list: list, tag: Tag):
    """
    按照class名查找子tag
    :param sub_dom: 要查找的字符串
    :param dom_list: 剩余字符串列表
    :param tag: 已找到的tag
    :return: 查找之后的新tag
    """
    tag = tag.findChild(name=sub_dom)
    # 递归调用
    return processNext(dom_list, tag=tag)

def processNext(dom_list: list = None, tag=None):
    """
    查找下一个tag
    :param dom_list: 总（剩余）的带查找dom字符串
    :param tag: 已找到的tag（soup）
    :return: 最后找到的tag
    """
    # 如果剩余dom表大于0
    if len(dom_list) > 0:
        sub_dom = dom_list.pop(0)
        # 按照类型，查找name或者class
        if sub_dom[0] == '.':
            tag = findSubClass(sub_dom[1:len(sub_dom)], dom_list, tag)
        else:
            tag = findSubName(sub_dom, dom_list, tag)
        return tag
    # 如果剩余表为空，而已找到的tag不为空，返回已找到的tag
    elif tag is not None:
        return tag
    # 没有找到tag或soup、dom_list解为空，则直接返回None
    else:
        return None

def parseDom(dom, soup):
    """
    按照dom查找tag
    :param dom: dom字符串
    :param soup: 待查找的soup对象
    :return: 返回查找到的元素链接
    """
    dom_list = str(dom).split(' ')
    tag = processNext(dom_list, tag=soup)
    return tag['href']

class Result:
    name = ''
    total = 0
    def __init__(self, name, total):
        self.name = name
        self.total = total

def getSoup(url):
    user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0"
    headers = {"User-Agent": user_agent}
    req = request.Request(url, headers=headers)
    resp = request.urlopen(req)
    soup = BeautifulSoup(resp.read(), 'html.parser')
    return soup

def removeTag(soup):
    reg = re.compile('<[^>]*>')
    content = reg.sub('', str(soup)).replace('\n', '').replace(' ', '')
    return content

def crawlData():
    with open("Url.json", 'r', encoding='utf-8') as f:
        temp = json.loads(f.read())
    resultList=[]
    for t in temp:
        name = t['name']
        url = t['url']
        dom = t['dom']
        latest_news_url = getHref(url, dom)
        latest_news_soup = getSoup(latest_news_url)
        content = removeTag(latest_news_soup)
        strList = re.split('[，|,]', content)
        for s in strList:
            if (s.find('累计') != -1 and s.find('确诊') != -1):
                total = re.findall(r"\d+", s)[0]
                result = Result(name, total)
                resultList.append(result)
                break;
    f=open('result.json','w')
    f.write(json.dumps(resultList))
    f.close()


if __name__ == '__main__':
    crawlData();
