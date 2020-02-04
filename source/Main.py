from Utils import *
import json
from connector import *
from apscheduler.schedulers.blocking import BlockingScheduler
from pyecharts.charts import Map
from pyecharts import options as opts
import os


def map_visualmap():
    data = getTotalResult()
    map = Map()
    map.add("中国疫情地图", data, is_map_symbol_show=False)
    map.set_global_opts(
        visualmap_opts=opts.VisualMapOpts(
            is_piecewise=True,
            pieces=[
                {"min": 1000, "label": ">1000"},
                {"max": 1000, "min": 500, "label": "500 - 1000"},
                {"max": 499, "min": 100, "label": "100 - 499"},
                {"max": 99, "min": 10, "label": "10 - 99"},
                {"max": 9, "min": 1, "label": "1 - 9"},
            ],
            range_color=['#FBF8EF', '#DC143C']),
    )
    return map


def crawData():
    with open('res/Url.json', 'r', encoding='utf-8') as f:
        temp = json.loads(f.read())
    for t in temp:
        name = t['name']
        url = t['url']
        dom = t['dom']
        print("\n当前省市：" + name + ", 当前Url：" + url)

        latest_news_url = getHref(name, url, dom)
        if latest_news_url is not None:
            print("首条文章Url为 " + latest_news_url)
            if name == '上海':
                latest_news_html = getShanghaiHtml(latest_news_url)
            else:
                latest_news_html = getHtml(latest_news_url)
            latest_news_soup = BeautifulSoup(latest_news_html, 'html.parser')
            content = removeTag(latest_news_soup)
            strList = re.split('[，|,|。|(|（]', content)
            newResult = Result(name)
            flag1, flag2, flag3 = False, False, False
            if name == '上海':
                flag_LEIJI = False
                for s in strList:
                    if s.find('累计') != -1:
                        flag_LEIJI = True

                    if (flag_LEIJI and flag1 and flag2 and flag3):
                        break

                    elif (flag_LEIJI and not flag1 and s.find('确诊病例') != -1):
                        array = re.findall(r"\d+", s)
                        if (len(array) > 0):
                            flag1 = True
                            total = array[0]
                            newResult.total = total
                    elif (flag_LEIJI and flag1 and not flag2 and (s.find('出院') != -1 or s.find('治愈') != -1)):
                        array = re.findall(r"\d+", s)
                        if (len(array) > 0):
                            flag2 = True
                            cure = array[0]
                            newResult.cure = cure
                    elif (flag_LEIJI and flag1 and not flag3 and s.find('死亡') != -1):
                        array = re.findall(r"\d+", s)
                        if (len(array) > 0):
                            flag3 = True
                            dead = array[0]
                            newResult.dead = dead
                    else:
                        continue
            else:
                for s in strList:
                    if (flag1 and flag2 and flag3):
                        break
                    elif (not flag1 and s.find('累计') != -1 and s.find('病例') != -1):
                        array = re.findall(r"\d+", s)
                        if (len(array) > 0):
                            flag1 = True
                            total = array[0]
                            newResult.total = total
                    elif (flag1 and not flag2 and s.find('新增') == -1 and (s.find('出院') != -1 or s.find('治愈') != -1)):
                        array = re.findall(r"\d+", s)
                        if (len(array) > 0):
                            flag2 = True
                            cure = array[0]
                            newResult.cure = cure
                    elif (flag1 and not flag3 and s.find('死亡') != -1 and s.find('新增') == -1):
                        array = re.findall(r"\d+", s)
                        if (len(array) > 0):
                            flag3 = True
                            dead = array[0]
                            newResult.dead = dead
                    else:
                        continue
            if (newResult.total or newResult.cure or newResult.dead):
                updateResult(newResult)

        else:
            continue


if __name__ == '__main__':
    # sched = BlockingScheduler()
    # sched.add_job(crawData(), 'interval', hours=1)
    crawData()
    # map_visualmap().render('res/map.html')
