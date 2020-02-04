from urllib import request, parse
from bs4 import BeautifulSoup, Tag
import re
import requests
import js2py
import json

import Logger


def getHenanHtml(url):
    jsonData = json.dumps(
        {"isallsites": False, "sitename": "", "sitedir": "", "siteids": "", "channelindex": "", "channelname": "",
         "channelids": "", "type": "title", "word": "肺炎疫情情况", "dateattribute": "AddDate", "datefrom": "", "dateto": "",
         "since": "", "pagenum": 0, "ishighlight": False, "isdefaultdisplay": False, "publishmentsystemid": "1",
         "ajaxdivid": "ajaxElement_1_291",
         "template": "qYw4qI0add0aqmLv509Jp79pLVslEs3rHIfOUn8zN0add0Taix1tTairdMzgqGcpmy8nCGbrZPfZvX3AM6yl1XsNQB4I6jQkjYPKdY7uCDd3qx9Uv9MRR0slash0pEj37x5jbxcem0slash0PBZx15YRiebdeisFGDtsj621qq7JGG9TragyyAEhZtP8Qja0Xm8QQzIjf6Q0slash0K0add01VaCU25NVfwdkr8Yx2Tbg4xzWFMetqYCGHp6Jq0add0r4INg7gGsZ8H3bt8RVusEDrJW43m7F0add0dLvdMWHoYZozc7bVWgqFihpi0oadE1lH0GhscEMEllXaAzgGJLGQu5FvQVE4nulgSq82yJA0add0T0add0b1i3rTmiIusa0slash0rHfAjEr0D57Qt9UwWthIa9PLciO6LDFCUo5yIU1QojoKCY0add0n0slash0V2ZKrHmdT34WztMJPNFoGtOq2X5CdRi0JKrQvGEJqsm3mhMpn0add0jLvcpkd5rqrdTsB4YneJFM21YLmMwSCAz0slash07Q3eCaQrsVRNti4URccAFjub2mnnLOmJt3l4LbQECxc6E2FSI7lALgKRGjg2ZU8OI51wengS8nR6aa0OfQR7ZGKTEclQqa4gBn2iNP6UpcTQLX35noBAQ0add0p49sYsBi0add0bvAW0ATIiU9vLlwUJa8QS0uD1WIcm6X0slash0hmKlfD0eB8KHKiq6lZwhVY0C60add0zetYiaHVS9vkEFVu6jEhnekx0add0dZymLK7XRI0add0XZ7RnHwf23nnSwkhgVHTxD4nMFOjii5gDeriAaW7v0fsK5GG0OzkIcUkf8VGm8HLbBIY80x7CB0add0SKngBFvx0slash0jyYGcCkbl0slash06NJUPOGURKWKksWtnsjQTnuOpU2M3U0add0wpgYkdKW60slash0wxCkuYebykJJ3wtjNuwx8bkEhJshqSDWuX89oB00add03Dy4ZshE6ZqdmB50qk9IgcT4o3EgcH0Pn0slash0LrOu0add0Yta9oO7BIyO0bY0slash0pDdqOVlrvy54Oo2cZ8NIGsCbb9FMmdlbhkW4GGEy5pvAR00EUx6vlpfZ00add03P2kVr0gDKLtkCDCPRCpi0slash0bLSVl4H2NQXa59Ylp9LTTYcXvHXBKXVRF54XPnb6nzFPmOZj5epRVEm8p7aY1N2YNRXqJfHiGfUaNqtVyFc0slash071BvoKqKl4krmTdubFF0add08cVaSzGOwZQ2p1psgGGFgc4LB6YDFfB7JfnD9nnE40slash0xOtGO7g5NakdGfxUWKOlkmPCx5U0slash06nw0slash0zPjWmvLckVig5UBVkJ0slash0RxSny7Bd7w3PxdZWT6xfXmvDvh6erAyDoQhn0add0fvFJ3zbrAwVVgWaeqsE0vUEg0add0dMivtA2Z8vq4rzvgfsoB0slash0ApBDkBzdNqdaPbL0add0FaWq0slash0GtILVT0add0SRRcAPTiw6rq9PsEle0jzJBjl0slash09cT9y18nAwAnNfy4d67qRqrMWb0add0ZOENbVr9sbrTB2kT3UZtKgYYrXqbWuGg2vcWH1G0slash0v2RBB0LGmm6YDiQoyc2yP8PUjELT7LLygesH1yIFxJZfkqULtEPe6kVo0add0PY9fXahg0slash0a0add0230slash0BOBJ4ECj9l8ZR4VJCFIfCLuyAlGrIAPEnNCstdGnFIrf0qKmMLI4UQMGH1",
         "channelid": "", "page": 1})
    wieldHtml = postHtml(url, jsonData)
    html = str(wieldHtml).replace('\\\\"', '')
    return html


def getShanghaiHtml(url):
    first_html = getHtml(url)
    js_func = ''.join(re.findall(r'(function .*?)</script>', first_html.decode("utf-8")))
    js_arg = ''.join(re.findall(r'setTimeout\(\"\D+\((\d+)\)\"', first_html.decode("utf-8")))
    js_func = js_func.replace('eval("qo=eval;qo(po);")', 'return po')
    cookie_str = executeJS(js_func, js_arg)
    cookie = parseCookie(cookie_str)
    return getHtml(url, cookie)


def executeJS(js_func_string, arg):
    func = js2py.eval_js(js_func_string)
    return func(arg)


def parseCookie(string):
    string = string.replace("document.cookie='", "")
    clearance = string.split(';')[0]
    return {clearance.split('=')[0]: clearance.split('=')[1]}


def selectDom(name, dom, soup):
    # print(soup)
    try:

        if dom[-6:] == "script":
            cdata = soup.select(dom)[0].contents[0]
            if name == '贵州':
                result = re.findall('str_1 = "(.+?)";', cdata)[0]
                return result
            else:
                record = BeautifulSoup(cdata, 'html.parser').select("record")[0].contents[0]
                result = BeautifulSoup(record, 'html.parser').select("li a")[0]['href']
                return result
        else:
            hrefList = soup.select(dom)
            result = hrefList[0]['href']
            return result
    except:
        logger = Logger.Logger()
        logger.error("Name:" + name)
        logger.error("Source:")
        logger.error(soup)
        logger.error("Dom is:" + dom)
        logger.error("After selected:")
        logger.error(hrefList)


def getHref(name, url, dom):
    """
    获取文章的链接
    :param name:
    :param url: 文章列表
    :param dom: 待查找的dom
    :return: 文章链接
    """
    try:
        if (name == '上海'):
            html = getShanghaiHtml(url)
        elif (name == '河南'):
            html = getHenanHtml(url)
        else:
            html = getHtml(url)
        soup = BeautifulSoup(html, 'html.parser')
        '''
        R.I.P
        href: str = parseDom(dom, soup)
        '''
        href: str = selectDom(name, dom, soup)
        if href is None:
            return None
        print("首篇文章（相对）链接为 " + href)
        # 返回链接，对相对链接进行拼接处理
        if href[0:3] == 'http':
            return href
        else:
            return parse.urljoin(url, href)
    except Exception as e:
        print(e)


def getHtml(url, cookie=None):
    try:
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'}
        html = requests.get(url=url, headers=header, cookies=cookie).content
        return html
    except requests.exceptions.RequestException:
        print("request fail! url = " + url)


def postHtml(url, jsonData):
    try:
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
            'Content-Type': 'application/json'
        }
        html = requests.post(url=url, headers=header, data=jsonData).content
        return html
    except requests.exceptions.RequestException:
        print("request fail! url = " + url)


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


def findSubId(sub_dom: str, dom_list: list, tag: Tag):
    """
    按照id名查找子tag
    :param sub_dom: 要查找的字符串
    :param dom_list: 剩余字符串列表
    :param tag: 已找到的tag
    :return: 查找之后的新tag
    """
    tag = tag.findChild(id=sub_dom)
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
    tag = tag.findChild(sub_dom)
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
        elif sub_dom[0] == '#':
            tag = findSubId(sub_dom[1:len(sub_dom)], dom_list, tag)
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


def removeTag(soup):
    reg = re.compile('<[^>]*>')
    content = reg.sub('', str(soup)).replace('\n', '').replace(' ', '')
    return content
