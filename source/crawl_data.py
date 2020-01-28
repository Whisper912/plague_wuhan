from urllib import request
from bs4 import BeautifulSoup, Tag


def getHref(url, dom):
    # 别忘了请求头（headers），以防万一
    user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0"
    headers = {"User-Agent": user_agent}
    # 爬取网站地址，我爬的是网易的
    req = request.Request(url, headers=headers)
    resp = request.urlopen(req)
    # 打开页面
    html = resp.read()
    # 输出编码后的结果（编码为GBK），可有可无
    # print(html)
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup.prettify())
    href: str = parseDom(dom, soup)
    if href[0] != '.':
        return href
    else:
        return url + href[2:len(href)]


def findSubClass(sub_dom: str, dom_list: list, tag: Tag):
    tag = tag.findChild(class_=sub_dom)
    # print(tag)
    return processNext(dom_list, tag=tag)


def findSubName(sub_dom: str, dom_list: list, tag: Tag):
    tag = tag.findChild(name=sub_dom)
    # print(tag)
    return processNext(dom_list, tag=tag)


def processNext(dom_list: list = None, tag=None):
    if len(dom_list) > 0:
        sub_dom = dom_list.pop(0)
        if sub_dom[0] == '.':
            tag = findSubClass(sub_dom[1:len(sub_dom)], dom_list, tag)
        else:
            tag = findSubName(sub_dom, dom_list, tag)
        return tag
    elif tag is not None:
        return tag
    else:
        return None


def parseDom(dom, soup):
    dom_list = str(dom).split(' ')
    tag = processNext(dom_list, tag=soup)
    return tag['href']


if __name__ == '__main__':
    url = "http://wjw.beijing.gov.cn/wjwh/ztzl/xxgzbd/"
    dom = ".weinei_left_con .weinei_left_con_line a"

    href = getHref(url, dom)
    print(href)
