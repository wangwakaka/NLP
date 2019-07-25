import requests
import re
import math
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']

#创建容纳所有地铁站的字典
lines = {}

#北京地铁官方网址
url_1 = 'https://www.bjsubway.com/station/xltcx/'

#京港地铁官方网址
url_2 = 'http://www.mtr.bj.cn/instruct/station_main.html'

#地铁1,2,5,6,7,8,9,10,13,15号线以及八通线、昌平线、亦庄线、房山线、机场线
lines_list_1 = ['1','2','5','6','7','8','9','10','13','15','bt','cp','yz','fs','jc']

#地铁4,14,16号线
lines_list_2 = ['4','14','16']

#相应的正则匹配
pattern_str_1 = r'<div class="station"><a href="/station/xltcx/line{}/\d+-\d+-\d+/\d+.html">(\w+)</a></div>'
pattern_str_2 = r'<li><a href="../instruct/map_{}.html" title="">(\w+)</a></li>'

def get_subway_station(url, codeing, lines_list, pattern_str):
    response = requests.get(url,verify=False)
    response.encoding = codeing

    for line in lines_list:

        if line == '7':# 7号线正则匹配比较特殊，单独拿出来
            pattern_7 = re.compile(r'<div class="station"><a href="/station/xltcx/lines7/\d+-\d+-\d+/\d+.html">(\w+)</a></div>')
            lines['7'] = pattern_7.findall(response.text)

        elif line == '16': # 16号线正则匹配比较特殊，单独拿出来
            pattern_16 = re.compile(r'<li><a href="/instruct/map_16.html" title="">(\w+)</a></li>')
            lines['16'] = pattern_16.findall(response.text)
        else:
            pattern = re.compile(pattern_str.format(line))
            lines[line] = pattern.findall(response.text)

    return lines

#获得地铁1,2,5,6,7,8,9,10,13,15号线以及八通线、昌平线、亦庄线、房山线、机场线车站的名称
get_subway_station(url_1,'gb2312',lines_list_1,pattern_str_1)

#获得地铁4,14,16号线车站的名称
get_subway_station(url_2,'utf-8',lines_list_2,pattern_str_2)


#地铁s1线官方网站没有数据，手动添加
lines['s1'] = ['石厂', '小园', '栗园庄', '上岸', '桥户营', '四道桥', '金安桥']

#输出所有地铁站
# print(lines)


#创建地铁连接字典
connection_graphs = defaultdict(list)


#把应该连接在一起的地铁站连在一起
for values in lines.values():
    for i in range(1,len(values)):
        pre_station = values[i-1]
        later_station = values[i]

        connection_graphs[pre_station].append(later_station)
        connection_graphs[later_station].append(pre_station)



#画出地铁连接图
# nx.draw(nx.Graph(connection_graph),with_labels=True,node_size=30)
# plt.show()


def pretty_print(rouets):
    print('->'.join(rouets))


#宽度优先搜索方法
def search(start_station, destination_station,connection_graph_param,sort_candidate):
    pathes = [[start_station]]
    visited = set()

    while pathes:
        path = pathes.pop(0)
        front = path[-1]

        if front in visited:continue

        new_stations = connection_graph_param[front]
        for station in new_stations:

            if station in path:continue

            new_path = path + [station]
            pathes.append(new_path)

            if station == destination_station:
                return new_path

        visited.add(front)
        pathes = sort_candidate(pathes)

#采取经过站点最少排序策略
def transfer_stations_little(pathes):
    return sorted(pathes,key=len)


pretty_print(search('石厂','3号航站楼',connection_graphs,transfer_stations_little))

#输出：石厂->小园->栗园庄->上岸->桥户营->四道桥->金安桥->苹果园->杨庄->西黄村->廖公庄->田村->海淀五路居->慈寿寺->花园桥->白石桥南->车公庄西->车公庄->平安里->北海北->南锣鼓巷->东四->朝阳门->东四十条->东直门->三元桥->3号航站楼





































































































