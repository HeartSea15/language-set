"""
    作者：FLY
    功能：AQI空气质量计算
    5.0: 通过网络链接获取网页内容，对获得的网页内容进行处理
    存在的弊端：不知道aqi是不是都是2位
              aqi_div中的空格字符串问题
    6.0：输入拼音，返回AQI，解决上述弊端，获取一个城市
    7.0：获取所有城市
    8.0：将获取所有城市的aqi保存成csv文件，写操作
    版本：:8.0
    日期：05/21/2019
"""
import requests
from bs4 import BeautifulSoup
import csv

def get_city_aqi(city_pinyin):
    """
        获取城市的AQI
    """
    url = 'http://pm25.in/' + city_pinyin
    r = requests.get(url, timeout=30)  # 等待30秒，30秒无结果就不等了
    bs = BeautifulSoup(r.text, 'lxml')  # 创建BeautifulSoup对象，页面内容，指定解码器摸（一般是lxml），编码格式不指定默认是和网页编码格式一致
    div_list = bs.find_all('div', {'class': 'span1'})  # 找到左右的div节点，指定条件：class = span1

    city_aqi = []
    for i in range(8):
        city_content = div_list[i]
        # caption = city_content.find('div', {'class': 'caption'}).text.strip()  # 获取节点内的内容，strip()移除字符串头尾指定的字符（默认为空格或换行符）或字符序列
        value = city_content.find('div', {'class': 'value'}).text.strip()
        city_aqi.append(value)

    return city_aqi


def get_all_city():
    """
        获取所有城市的名称，拼音
    """
    city_list = []
    url = 'http://pm25.in/'
    r = requests.get(url, timeout=30)
    bs = BeautifulSoup(r.text, 'lxml')
    city_div = bs.find_all('div', {'class': 'bottom'})[1]  #有两个条件一样的div,取第二个
    city_a_div = city_div.find_all('a')

    for city in city_a_div:
        city_text_name = city.text
        city_pinyin = city['href'][1:]  # 拼音要取href的属性，前面有/，所有切片
        city_list.append((city_text_name, city_pinyin))
    return city_list


def main():
    """
        主函数
    """
    city_list = get_all_city()

    # csv的第一行
    header = ['City', 'AQI', 'PM2.5/1h', 'PM10/h', 'CO/1h', 'NO2/1h', 'O3/1h', 'O3/8h', 'SO2/1h']
    # csv 的写操作
    with open('china_city_aqi.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)  # 写入csv的第一行

        for i, city in enumerate(city_list):
            # 记录进度
            if (i+1) % 10 == 0:
                print('已处理{}条记录，共{}条记录'.format(i+1, len(city_list)))

            city_name = city[0]    # 它是一个字符串
            city_pinyin = city[1]  # 它是一个字符串
            city_aqi = get_city_aqi(city_pinyin)  # 它是一个列表
            row = [city_name]+city_aqi
            writer.writerow(row)


if __name__ == '__main__':
    main()
