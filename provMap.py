#python

from math import sin, asin, cos, radians, fabs, sqrt
from re import match
#from geographiclib.geodesic import Geodesic

cn_pov_pos = '''
北京  北京 北纬39.55 东经116.24
天津  天津 北纬39.02 东经117.12
上海  上海 北纬31.14 东经121.29
重庆  重庆 北纬29.59 东经106.54
台湾  台北  北纬25.03 东经121.30
安徽  合肥 北纬31.52 东经117.17
福建  福州 北纬26.05 东经119.18
甘肃  兰州 北纬36.04 东经103.51
广东  广州  北纬23.08 东经113.14
广西  南宁  北纬22.48 东经108.19
贵州  贵阳  北纬26.35 东经106.42
海南  海口  北纬20.02 东经110.20
河北  石家庄  北纬38.02 东经114.30
河南  郑州  北纬34.46 东经113.40
黑龙江  哈尔滨  北纬45.44 东经126.36
湖北  武汉  北纬30.35 东经114.17
湖南  长沙  北纬28.12 东经112.59
吉林  长春  北纬43.54 东经125.19
江苏  南京  北纬32.03 东经118.46
江西  南昌  北纬28.40 东经115.55
辽宁  沈阳  北纬41.48 东经123.25
内蒙古  呼和浩特  北纬40.48 东经111.41
宁夏  银川  北纬38.27 东经106.16
青海  西宁  北纬36.38 东经101.48
山东  济南  北纬36.40 东经117.00
山西  太原  北纬37.54 东经112.33
陕西  西安  北纬34.17 东经108.57
四川  成都  北纬30.40 东经104.04
西藏  拉萨  北纬29.39 东经91.08
新疆  乌鲁木齐  北纬43.45 东经87.36
云南  昆明  北纬25.04 东经102.42
浙江  杭州  北纬30.16 东经120.10
香港  香港  北纬22.20 东经114.10
澳门  澳门  北纬22.20 东经113.50
'''

cn_pov_adj_dict ={
    '北京': ['河北','天津'],
    '天津': ['北京','河北'],
    '河北': ['北京','天津','山东','河南','山西','内蒙古','辽宁'],
    '山西': ['内蒙古','陕西','河南','河北','北京'],
    '陕西': ['山西','河南','湖北','重庆','四川','甘肃','宁夏','内蒙古'],
    '内蒙古': ['黑龙江','吉林','辽宁','河北','山西','宁夏','甘肃','陕西'],
    '河南': ['河北','湖北','陕西','安徽','山西','山东'],
    '黑龙江': ['内蒙古','吉林'],
    '吉林': ['内蒙古','辽宁'],
    '辽宁': ['内蒙古','吉林','河北'],
    '山东': ['河北','河南','江苏','安徽'],
    '宁夏': ['陕西','内蒙古','甘肃'],
    '甘肃': ['陕西','新疆','青海','四川','宁夏','内蒙古'],
    '青海': ['西藏','新疆','甘肃','四川'],
    '西藏': ['新疆','青海','四川','云南'],
    '新疆': ['西藏','甘肃','青海'],
    '云南': ['西藏','四川','贵州','广西'],
    '湖北': ['陕西','河南','安徽','江西','湖南','重庆'],
    '重庆': ['陕西','贵州','湖北','湖南','四川'],
    '四川': ['重庆','陕西','青海','甘肃','云南','贵州','西藏'],
    '上海': ['浙江','江苏'],
    '广东': ['福建','江西','湖南','广西'],
    '广西': ['广东','海南','贵州','云南'],
    '安徽': ['浙江','江西','河南','山东','江苏','湖北'],
    '贵州': ['湖南','广西','四川','重庆','云南'],
    '海南': ['广东'],
    '湖南': ['江西','重庆','贵州','广东','广西','湖北'],
    '江苏': ['山东','河南','安徽','浙江','上海'],
    '江西': ['浙江','福建','安徽','湖北','湖南','广东'],
    '浙江': ['江西','上海','江苏','福建','安徽'],
    '福建': ['浙江','江西','广东'],
    '台湾': ['福建'],
    '香港': ['广东'],
    '澳门': ['广东']
    }


class provMap:

    __pos = dict()
    __citys = dict()
    __adj = list()
    
    def __init__(self, name, prov_pos=cn_pov_pos, adjac=cn_pov_adj_dict):
        self.name = name

        txt_lines = prov_pos.splitlines()
        pat = "(\S+\s).(\S+\s).*北纬(\d+\.\d+).*东经(\d+\.\d+)"
        
        for tl in txt_lines:
            mat = match(pat, tl)
            if mat:
                name = mat.group(1).replace(' ', '')
                c = mat.group(2).replace(' ', '')
                n = float(mat.group(3).replace(' ', ''))
                e = float(mat.group(4).replace(' ', ''))
                self.__pos[name] = (e, n) #经纬度
                self.__citys[name] = c #城市
                
        for i in adjac:
            li = adjac[i]
            for j in li:
                if j:
                    #dist = self.__get_distance_hav(self.__pos[i], self.__pos[j])
                    if (j,i) not in self.__adj:
                        self.__adj.append((i, j))


    def __get_distance_hav(self, p1, p2):
        geodict = Geodesic.WGS84.Inverse( p1[1],p1[0], p2[1], p2[0])
        return int(geodict['s12']/1000)
    
    #获取位置信息 [p:(lon, lat)...] 
    def get_position(self):
        return self.__pos

    #获取邻接关系和距离，[(pa,pb)...]
    def get_adjacency(self):      
        return self.__adj
    
    #获取城市名
    def get_citys(self):      
        return self.__citys

if __name__ == '__main__':

    my_map = provMap("china")

    pos = my_map.get_position()
    for i in pos:
        print(i, pos[i])

    city = my_map.get_citys()
    for i in city:
        print(i, city[i])
        
    adj = my_map.get_adjacency( )
    for i in range(0, len(adj)):
        print(adj[i])

    