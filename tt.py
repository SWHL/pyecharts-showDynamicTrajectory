# -*- coding: utf-8 -*-
# @Time    : 2020-06-05 06:20
# @Author  : SWHL
# @File    : tt.py
# @Software: PyCharm
# @Contact : jhwang0305@163.com
import pandas as pd
import random
from pyecharts import GeoLines, Style

# 读取数据
data = pd.read_excel('data.xlsx', header=None, names=['name'])
print(data.head())

# 写个遍历，把各地方的地名，经度，纬度提取出来，并存取在DataFrame中
city_list = []
lad_list = []
long_list = []
for i in data['name']:
    s = i.strip().split(':')  # 去除前后空格，并以":"为分隔符分裂字符
    city = s[0][1:-1]  # 取分裂后字符的第一个，得到地名
    lad = s[1].split(',')[0][2:]  # 取分裂后字符的第二个，继续以','为分隔符分裂字符
    long = s[1].split(',')[1][:-2]
    city_list.append(city)
    lad_list.append(lad)
    long_list.append(long)
result = pd.DataFrame({'地点': city_list, '经度': lad_list, '纬度': long_list})

# 以东莞为始点，其他各个城市为终点，整理数据
plotting = result[result['地点'] != '东莞']['地点'].apply(lambda x: ('东莞', x))

# 自定义各城市的经纬度
geo_cities_coords = {result.iloc[i]['地点']: [result.iloc[i]['经度'], result.iloc[i]['纬度']] for i in range(len(result))}

# 随机抽样20个城市组合
plotting_data = random.sample(list(plotting), 20)
# 设置画布的格式
style = Style(title_pos="center",
              width=1000,
              height=800)

# 部分地理轨迹图的格式
style_geolines = style.add(is_label_show=True,
                           line_curve=0.3,  # 轨迹线的弯曲度，0-1
                           line_opacity=0.6,  # 轨迹线的透明度，0-1
                           geo_effect_symbol='plane',  # 特效的图形，有circle,plane,pin等等
                           geo_effect_symbolsize=10,  # 特效图形的大小
                           geo_effect_color='#7FFFD4',  # 特效的颜色
                           geo_effect_traillength=0.1,  # 特效图形的拖尾效果，0-1
                           label_color=['#FFA500', '#FFF68F'],  # 轨迹线的颜色，标签点的颜色，
                           border_color='#97FFFF',  # 边界的颜色
                           geo_normal_color='#36648B',  # 地图的颜色
                           label_formatter='{b}',  # 标签格式
                           legend_pos='left')

# 作图
geolines = GeoLines('出行轨迹图', **style.init_style)
geolines.add('从东莞出发',
             plotting_data,
             maptype='china',  # 地图的类型，可以是省的地方，如'广东',也可以是地市，如'东莞'等等
             geo_cities_coords=geo_cities_coords,
             **style_geolines)

# 发布，得到图形的html文件
geolines.render()
