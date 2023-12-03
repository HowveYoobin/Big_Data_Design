####################### Download packages #############################
# ! pip install requests
# ! pip install jsonlines
# ! pip install geopandas

######################## Import Packages #############################
# API request
import requests
import json

# Calculation
import numpy as np
from scipy.spatial.distance import cdist

# Visualization
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium import Marker
from folium import Circle
import pandas as pd
import geopandas as gpd
from shapely import wkt
import matplotlib.cm as cm
from matplotlib import rc
rc('font', family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False
from datetime import datetime

# KMeans clustering & Optimization
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score

class GetData:
    ###################################################### Load Data ##########################################################

    def __init__(self, API_key, background, point_geojson, slope_gpkg):
        
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

        #### 창고 점 찍기 위한 데이터셋 가져오기 ####
        gdf = gpd.read_file(str(point_geojson))
        points = gdf['geometry'].apply(lambda geom: (geom.x, geom.y))
        self.warehouse_df = pd.DataFrame(points.tolist(), columns = ['lon', 'lat'])
        
        #### 경사도 데이터 가져오기 ####
        slope_file = gpd.read_file(str(slope_gpkg), driver = "gpkg")
        slope_file = slope_file.to_crs("EPSG:4326")
        high_slope = slope_file[slope_file["DN"] == 1]
        high_slope_array = high_slope['geometry'].apply(lambda geom: (geom.exterior.xy[0][0], geom.exterior.xy[1][0]))
        self.slope_df = pd.DataFrame(high_slope_array.tolist(), columns=['lon', 'lat'])

    ###################################################### 지역별 [경도, 위도] 좌표 (plt용) ########################################################### 
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

    ###################################################### 지역별 [위도, 경도] 좌표 (Folium용) ########################################################### 
    
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
    
    ###################################################### Folium 지도시각화 ##########################################################
    
    def folium_visualize(self,rad, vertiport_candidates, *lat_lon_dicts):
        
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
        for i, dict_ in enumerate(lat_lon_dicts):
            for region in dict_.keys():
                popup_content = region
                folium.PolyLine(locations = dict_[str(region)], 
                                #tooltip = "Polyline",
                                color = line_colors[i % len(line_colors)]
                                ).add_to(m).add_child(folium.Popup(popup_content))
        
        # 버티포트 입지후보 표시하기
        for _,row in vertiport_candidates.iterrows():
            Marker(location = [row['lat'], row['lon']],
                   icon = folium.Icon(color="red", icon = 'star')
                   ).add_to(m)
            Circle(location = [row['lat'], row['lon']], popup = row['cluster'], radius = rad, color = "red", fill = "red", fill_opacity = 0.2).add_to(m)
        
        # 대구경북 신공항 표시하기
        Marker(location = [36.3026462, 128.5236647], icon = folium.Icon(color="blue", icon = 'plane'), popup = "대구경북신공항 부지").add_to(m)

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
         
    ###################################################### Matplotlib 지도시각화 ##########################################################
    
    def plt_visualize(self, *lon_lat_dicts, slope = False, save = False):

        sns.set(style="whitegrid")
        fig, ax = plt.subplots(figsize=(12,12))
        ax.set_xlim(127.5, 130)
        ax.set_ylim(35.5, 37.3)
        
        # 배경 지도(경북, 대구) 그리기
        self.geo.boundary.plot(ax=ax, linewidth=1, colors = 'gray')

        # 경사도 그리기
        if slope == True:
            ax.scatter(x = self.slope_df['lon'], y = self.slope_df['lat'], c="gray", marker='o', s=0.1, alpha=0.4)

        # 창고 지점 그리기
        ax.scatter(x= self.warehouse_df['lon'], y = self.warehouse_df['lat'], marker = "o", alpha=0.4, label = 'Refrigerated Warehouse')

        # 대구경북신공항 그리기
        ax.scatter(x = 128.5236647,y = 36.3026462, marker = "*", color = "red", s = 300, label = "TK Airport")

        colors = ["green", "red", "blue",  "purple"]
        labels = {"green":"Flight Danger Area", "red":"Flight Prohibited Area", "blue":"Flight Restricted Area"}
        i = -1

        # 비행 구역 그리기
        for dict_ in lon_lat_dicts:
            i += 1
            coord_array = self.coord_array(dict_)
            for region in coord_array.keys():
                # legend_labels.append(f"{colors[i]}: {region}")
                ax.plot(coord_array[str(region)][0], coord_array[str(region)][1], c = colors[i], label = labels[colors[i]])
                # 주석 달기
                coord = [round(np.mean(coord_array[str(region)][0]),2), round(np.mean(coord_array[str(region)][1]), 2)]
                if "P" in  str(region) and "A" in str(region):
                    coord[1] = coord[1] + 0.1
                elif "P" in  str(region)  and "B" in str(region):
                    coord[1] = coord[1] - 0.1
                elif "155A" in  str(region):
                    coord[1] = coord[1] - 0.03
                ax.annotate(str(region), xy = (coord[0], coord[1]), color = "black")    

        
        plt.title("Refrigerated Warehouse in Daegu and Gyeongsangbuk-do", fontsize = 20)
        plt.xlabel('Longitude', fontsize = 18)
        plt.ylabel('Latitude', fontsize = 18)
        plt.grid(linestyle='--')
        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        plt.legend(by_label.values(), by_label.keys(), loc = 'upper left')
        plt.show()
        
        if save == True:
            fig.savefig(f"{datetime.today().year}{datetime.today().month}{datetime.today().day}{datetime.today().hour}{datetime.today().minute}_map.png")

    ###################################################### KMeans 실행 & 지도시각화 #########################################################

    def Kmeans(self, k, *lon_lat_dicts, slope = False, save = False, adjust = False):
        
        sns.set(style="whitegrid")
        fig,ax = plt.subplots(figsize=(12,12))
        ax.set_xlim(127.5, 130)
        ax.set_ylim(35.5, 37.3)
        title = f"Vertiport candidates in Daegu and Gyeongsangbuk-do (n={k})"

        # 경사도 그리기
        if slope == True:
            ax.scatter(x = self.slope_df['lon'], y = self.slope_df['lat'], c="gray", marker='o', s=0.1, alpha=0.4)

        # 배경 지도(경북, 대구) 그리기
        self.geo.boundary.plot(ax=ax, linewidth=1, colors = 'gray')
        
        # 대구경북신공항 추가
        ax.scatter(x = 128.5236647, y = 36.3026462, marker = "*", color = "black", s = 300, label = "TK Airport")

        # 비행 구역 그리기
        colors = ["green", "red", "blue",  "purple"]
        labels = {"green": 'Flight Danger Area', "red":'Flight Prohibited Area', "blue":'Flight Restricted Area'}
        i = -1
        
        for dict_ in lon_lat_dicts:
            i += 1
            coord_array = self.coord_array(dict_)
            for region in coord_array.keys():
                # legend_labels.append(f"{colors[i]}: {region}")
                ax.plot(coord_array[str(region)][0], coord_array[str(region)][1], c = colors[i], label = labels[colors[i]])
                # 주석 달기
                coord = [round(np.mean(coord_array[str(region)][0]),2), round(np.mean(coord_array[str(region)][1]), 2)]
                if "P" in  str(region) and "A" in str(region):
                    coord[1] = coord[1] + 0.1
                elif "P" in  str(region)  and "B" in str(region):
                    coord[1] = coord[1] - 0.1
                elif "155A" in  str(region):
                    coord[1] = coord[1] - 0.03
                ax.annotate(str(region), xy = (coord[0], coord[1]), color = "black")    
        
        # K Means 실행
        warehouse = self.warehouse_df.copy()
        km = KMeans(n_clusters = k, random_state = 42)
        km.fit(warehouse)

        warehouse['cluster'] = km.labels_
        
        centroids_df = pd.DataFrame(km.cluster_centers_, columns = ['lon', 'lat'])
        centroids_df['cluster'] = range(k)

        # Vertiport candidate 위치를 centroid에 가장 가까운 창고 좌표로 조정
        if adjust ==  True:
            # 각 cluster의 창고에서 centroid까지의 거리 계산
            closest_points_list = []

            for k in range(len(centroids_df)):
                # 각 cluster number에서 창고 좌표들과 centroid 좌표 추출
                warehouse_cluster = warehouse[warehouse['cluster'] == k][['lon', 'lat']]
                centroid = centroids_df[centroids_df['cluster'] == k][['lon', 'lat']].values

                # centroid와 해당 cluster의 각 창고 간의 지점 거리 계산 & 거리가 최솟값인 창고의 좌표 찾기
                distances = cdist(warehouse_cluster, centroid, metric='euclidean')
                closest_index = distances.argmin()
                closest_warehouse = warehouse_cluster.iloc[closest_index]
                closest_warehouse['cluster'] = k

                closest_points_list.append(closest_warehouse.to_dict())

            # 새로운 centroid_df 생성
            centroids_df = pd.DataFrame(closest_points_list)
            # warehouse.drop(labels = "distance", axis = 1, inplace=True)
            title += "(Adjusted)"
        
        warehouse['cluster'] = warehouse['cluster'].apply(lambda x: 'Cluster '+ str(x+1))
        sns.scatterplot(x = 'lon', y = 'lat', data = warehouse, hue = 'cluster', palette=['darkorange', 'mediumseagreen', 'cornflowerblue'], marker='o', alpha=0.4)
        # plt.scatter(warehouse['lon'], warehouse['lat'], c=warehouse['cluster'], cmap='viridis', marker='o', alpha=0.4)
        plt.scatter(centroids_df['lon'], centroids_df['lat'], c='red', marker='X', s=200, label='Vertiport candidate')
        plt.title(title, fontsize=20)
        plt.xlabel('Longitude', fontsize=18)
        plt.ylabel('Latitude', fontsize = 18)
        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        plt.legend(by_label.values(), by_label.keys(), loc = 'upper left')
        plt.show()
        
        if save == True:
            if adjust == True:
                fig.savefig(f"{datetime.today().year}{datetime.today().month}{datetime.today().day}{datetime.today().hour}{datetime.today().minute}_Kmeans{k}_adjusted.png")
            else:
                fig.savefig(f"{datetime.today().year}{datetime.today().month}{datetime.today().day}{datetime.today().hour}{datetime.today().minute}_Kmeans{k}.png")
        
        return warehouse, centroids_df
    
     ###################################################### Silhouette Method ##########################################################

    # Silhouette method to find optimal K value
    def silhouette(self, max_k, save = False):
        # 1 ~ max_k까지의 수
        k = [i for i in range(2, max_k + 1)]
        warehouse = self.warehouse_df.copy()

        # plt.subplots()으로 리스트에 기재된 클러스터링 수만큼의 sub figures를 가지는 axs 생성 
        fig, ax = plt.subplots(figsize=(4*(max_k-1), 4), nrows=1, ncols=max_k-1)
        
        # 리스트에 기재된 클러스터링 갯수들을 차례로 iteration 수행하면서 실루엣 개수 시각화
        for ind, n_cluster in enumerate(k):
            
            # KMeans 클러스터링 수행하고, 실루엣 스코어와 개별 데이터의 실루엣 값 계산. 
            clusterer = KMeans(n_clusters = n_cluster, random_state=42)
            cluster_labels = clusterer.fit_predict(warehouse)
            
            sil_avg = silhouette_score(warehouse, cluster_labels)
            sil_values = silhouette_samples(warehouse, cluster_labels)
            
            y_lower = 10
            ax[ind].set_title('Number of Cluster : '+ str(n_cluster)+'\n' \
                            'Silhouette Score :' + str(round(sil_avg,3)) )
            ax[ind].set_xlabel("The silhouette coefficient values")
            ax[ind].set_ylabel("Cluster label")
            ax[ind].set_xlim([-0.1, 1])
            ax[ind].set_ylim([0, len(warehouse) + (n_cluster + 1) * 10])
            ax[ind].set_yticks([])  # Clear the yaxis labels / ticks
            ax[ind].set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1])
            
            # 클러스터링 갯수별로 fill_betweenx( )형태의 막대 그래프 표현. 
            for i in range(n_cluster):
                ith_cluster_sil_values = sil_values[cluster_labels==i]
                ith_cluster_sil_values.sort()
                
                size_cluster_i = ith_cluster_sil_values.shape[0]
                y_upper = y_lower + size_cluster_i
                
                color = cm.nipy_spectral(float(i) / n_cluster)
                ax[ind].fill_betweenx(np.arange(y_lower, y_upper), 0, ith_cluster_sil_values, \
                                    facecolor=color, edgecolor=color, alpha=0.7)
                ax[ind].text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))
                y_lower = y_upper + 10
                
            ax[ind].axvline(x=sil_avg, color="red", linestyle="--")
        
        if save == True:
            fig.savefig(f"silhouette_{max_k}.png")
        
        return sil_values, sil_avg
    
     ###################################################### Elbow Method ##########################################################

    def elbow(self, max_k, save = False):
        inertia = []
        warehouse = self.warehouse_df.copy()
        for num_clusters in range(1, max_k+1):
            kmeans = KMeans(n_clusters  = num_clusters, random_state=42)
            kmeans.fit(warehouse)
            inertia.append(kmeans.inertia_)
        
        plt.plot(range(1, max_k+1), inertia, "bo-")
        plt.xlabel("Values of K")
        plt.ylabel("Sum of squared distances (Inertia)")
        plt.xticks(np.arange(1, max_k + 1))
        plt.title("Elbow Method for optimal K")
        plt.show()

        if save == True:
            plt.savefig(f"elbow_{max_k}.png")