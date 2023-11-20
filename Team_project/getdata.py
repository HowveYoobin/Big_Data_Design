## Download packages
# ! pip install requests
# ! pip install jsonlines
# pip install geopandas

# Import Packages
import requests
import json
import numpy as np
import matplotlib.pyplot as plt
import folium
from folium.plugins import FloatImage
import pandas as pd
import geopandas as gpd
from shapely import wkt
from matplotlib import rc
rc('font', family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False
from datetime import datetime



class GetData:
    def __init__(self, API_key, background):
        #### API 관련 변수 정의 ####
        self.key = API_key
        self.endpoint = "https://api.vworld.kr/req/data"
        self.service = "data"
        self.version = "2.0"
        self.request = "GetFeature"
        self.format = "json"
        self.size = "1000"
        self.page = "1"
        # self.attrFilter = "ctp_kor_nm:=:대구광역시"
        self.geomFilter = "BOX(128.1198, 35.6516, 129.5, 37.069)" # 128.1198, 35.6516, 130.8899, 37.4835
        self.geometry = "true"
        self.attribute = "true"
        self.buffer = "10"
        self.regions = {
            "sido": {
                "data":"LT_C_ADSIDO_INFO",
                "columns": "ctprvn_cd, ctp_kor_nm, ctp_eng_nm, ag_geom"
            },
            "res": {
                "data": "LT_C_AISRESC",
                "columns": "restricted,res_lbl_1,res_lbl_2,res_lbl_3,ag_geom"
            },
            "dng": {
                "data": "LT_C_AISDNGC",
                "columns": "dng_lbl_1,dng_lbl_2,dng_lbl_3,ag_geom"
            },
            "prh": {
                "data": "LT_C_AISPRHC",
                "columns": "prohibited,prh_lbl_1,prh_lbl_2,prh_lbl_3,prh_lbl_4,prh_typ,ag_geom"
            }
        }
    
        #### 배경지도 그리기 위해 geojson을 csv로 변환한 파일 가져오기 ####
        df = pd.read_csv(str(background))
        df['geometry'] = df['geometry'].apply(wkt.loads)
        self.geo = gpd.GeoDataFrame(df, crs='epsg:4326')
        
    # 지역별 [경도, 위도] 좌표 (plt용)
    def get_lon_lat(self, region):
            
            if region not in self.regions.keys():
                 print("region 값에는 아래의 구역만 받습니다. \n", "'sido': KOREA BACKGROUND MAP", "'res': RESTRICTED AREA \n", "'dng': DANGER AREA")

            else:
                if region == 'sido':
                    # geomfilter를 attrFilter로 대체
                    # 요청 url 생성
                    data = self.regions[region]["data"]
                    columns = self.regions[region]["columns"]
                    url = f"{self.endpoint}?service={self.service}&version={self.version}&request={self.request}&format={self.format}&size={self.size}&page={self.page}&data={data}&columns={columns}&geomFilter={self.geomFilter}&geometry={self.geometry}&attribute={self.attribute}&buffer={self.buffer}&key={self.key}&domain="
                    print(url)
                else:
                     # 요청 url 생성
                    data = self.regions[region]["data"]
                    columns = self.regions[region]["columns"]
                    url = f"{self.endpoint}?service={self.service}&version={self.version}&request={self.request}&format={self.format}&size={self.size}&page={self.page}&data={data}&columns={columns}&geomFilter={self.geomFilter}&geometry={self.geometry}&attribute={self.attribute}&buffer={self.buffer}&key={self.key}&domain="
                    print(url)
                
                # 요청 결과
                res = json.loads(requests.get(url).text)                    

                # GeoJson 생성
                regions = res["response"]["result"]["featureCollection"]['features']

                # 구역별 좌표값 딕셔너리 만들기
                lon_lat = dict()

                for i in range(len(regions)):
                    coordinates = regions[i]['geometry']['coordinates'][0][0]
                    if region == 'sido':
                        region_label = regions[i]['properties']['ctp_kor_nm']
                    else:
                        region_label = regions[i]['properties'][str(region)+'_lbl_1']
                        
                    lon_lat[str(region_label)] = coordinates

                
                return lon_lat
                # return res

    # 지역별 [위도, 경도] 좌표 (Folium용)
    def get_lat_lon(self, region):
        
        lat_lon = dict()
        lon_lat = self.get_lon_lat(region)
        
        for label in lon_lat.keys():
             coordinates = []
             for coord in lon_lat[str(label)]:
                  rev = coord[::-1]
                  coordinates.append(rev)
                  lat_lon[label] = coordinates
        
        return lat_lon
    
    # Folium으로 시각화
    def folium_visualize(self, *lat_lon_dicts):
        
        center = [36.0194, 129.3434] # 경상북도 포항에서 시작
        line_colors = ["red", "blue", "green", "purple"]
        
        m = folium.Map(location = center, zoom_start = 8)

        # layer 색깔 지정
        map = {'fillColor':"", "lineColor": "000000"}

        # 배경 지도 그리기
        geo_json_str = self.geo.to_json()
        folium.GeoJson(geo_json_str,
                       name="경상북도 및 대구 (시군구)",
                       style_function = lambda x:map
                       ).add_to(m)

        # 인자로 받은 제한구역들 그리기
        for i, dict in enumerate(lat_lon_dicts):
            for region in dict.keys():
                popup_content = region
                folium.PolyLine(locations = dict[str(region)], 
                                #tooltip = "Polyline",
                                color = line_colors[i % len(line_colors)]
                                ).add_to(m).add_child(folium.Popup(popup_content))

        return m
    
    # plt 시각화를 위한 좌표 리스트 array화하기
    def coord_array(self, dict):
        coord_array = {}

        for region in dict.keys():
            coordinates = np.array(dict[str(region)])
            coordinates = coordinates.reshape(-1,2)
            coordinates = np.vstack((coordinates[:,0], coordinates[:,1]))
            coord_array[str(region)] = coordinates
        
        return coord_array
         
    # plt로 나타내기
    def plt_visualize(self, *lon_lat_dicts, save = False):
        fig,ax = plt.subplots(figsize=(12,12))

        # 배경 지도(경북, 대구) 그리기
        self.geo.boundary.plot(ax=ax, linewidth=1, colors = 'black')
        ax.set_title("경상북도 및 대구 지역 비행구역", fontsize=20)
        ax.set_xlim(127.5, 130)
        ax.set_ylim(35.5, 37.3)

        colors = ["green", "red", "blue",  "purple"]
        i = -1
        # legend_labels = []

        # 비행 구역 그리기
        for dict in lon_lat_dicts:
            i += 1
            coord_array = self.coord_array(dict)
            for region in coord_array.keys():
                # legend_labels.append(f"{colors[i]}: {region}")
                ax.plot(coord_array[str(region)][0], coord_array[str(region)][1], c = colors[i])
                # 주석 달기
                coord = [round(np.mean(coord_array[str(region)][0]),2), round(np.mean(coord_array[str(region)][1]), 2)]
                if "P" in  str(region) and "A" in str(region):
                    coord[1] = coord[1] + 0.1
                elif "P" in  str(region)  and "B" in str(region):
                    coord[1] = coord[1] - 0.1
                elif "155A" in  str(region):
                    coord[1] = coord[1] - 0.03
                ax.annotate(str(region), xy = (coord[0], coord[1]), color = "black")    
        
        plt.show()
        
        if save == True:
            fig.savefig(f"{datetime.today().year}{datetime.today().month}{datetime.today().day}{datetime.today().hour}{datetime.today().minute}_map.png")

            