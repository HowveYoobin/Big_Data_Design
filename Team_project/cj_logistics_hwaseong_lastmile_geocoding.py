# hgu attach --> container 들어가기
# conda activate env이름 -> 가상환경 들어가기
# pip install 라이브러리 이름 -> 없는 라이브러리 다운로드

import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import geopy
import json
import requests


if __name__=='__main__':
        parser = argparse.ArgumentParser()
        feature=True
        parser.add_argument('--warehouse_csv', type=str, default="cj_logistic_warehouse.csv",
                            help='csv file of warehouse location')
        parser.add_argument('--lastmile_csv', type=str, default='cj_logistics.csv',
                            help='csv file of lastmile file')
        parser.add_argument('--id', type=str, default=None,
                            help='Your client id of Naver Maps API')
        parser.add_argument('--secret', type=str, default=None,
                            help='Your secret code of Naver Maps API')
        parser.add_argument('--start', type=int, default=None,
                            help='Start location for data loading df.loc[start:end,]')
        parser.add_argument('--end', type=int, default=None,
                            help='End location for data loading df.loc[start:end,]')

        args = parser.parse_args()
        

warehouse_hs = pd.read_csv(args.warehouse_csv)
cj_last_mile_hs = pd.read_csv(args.lastmile_csv)
cj_last_mile_hs = cj_last_mile_hs[cj_last_mile_hs['받는분주소'].notnull()].reset_index().drop(columns = 'index')
cj_last_mile_hs = cj_last_mile_hs.assign(Road_Address = '-', longitude = 0, latitude = 0)

# geocoding
def geocoding(address, client_id, client_secret):

    API_url = 'https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?' # 네이버 지도 API setting
    input_param = 'query=' + address
    url = API_url + input_param

    headers = {
        'X-NCP-APIGW-API-KEY-ID': client_id,
        'X-NCP-APIGW-API-KEY': client_secret,
        'Accept': 'application/json'
    }
    try:
        with requests.get(url, headers=headers) as response:
            response.raise_for_status()

            if response.content:  # 응답이 비어있지 않은지 확인
                response_body = response.json()
                result_status = response_body['status']
                if result_status == 'OK':  # 정상 반환
                    if len(response_body['addresses']) != 0:    # response body가 비지 않은 경우,
                        roadAddress = response_body['addresses'][0]['roadAddress']  # 도로명주소
                        longitude = float(response_body['addresses'][0]['x'])  # 경도
                        latitude = float(response_body['addresses'][0]['y'])  # 위도
                    else:   # response body가 비어있을 경우
                        roadAddress, longitude, latitude = None, None, None
                    
                else:   # 비정상 반환
                    print('Result error code : %s' % result_status)
                    roadAddress, longitude, latitude = None, None, None
            else:   # 응답이 비어있는 경우
                print('Empty response!')
                roadAddress, longitude, latitude = None, None, None

    except requests.exceptions.HTTPError as e:  # HTTP 에러
        print(f"HTTP Error: {e}")
        roadAddress, longitude, latitude = None, None, None

    return roadAddress, longitude, latitude

# 화성시 last mile data에 대한 geocoding process
def to_coordinates_logistics(data, client_id, client_secret):
    r_add_list, lon_list, lat_list = [], [], []
    for i in range(len(data)):
        address = data.iloc[i]['받는분주소']
        print(i+1, address)
        road_address, longitude, latitude = geocoding(address, client_id, client_secret)
        r_add_list.append(road_address); lon_list.append(longitude); lat_list.append(latitude)
    
    return r_add_list, lon_list, lat_list

address_list, lon_list, lat_list = to_coordinates_logistics(cj_last_mile_hs.loc[args.start:args.end,], args.id, args.secret)
cj_last_mile_hs.loc[args.start:args.end, 'Road_Address'] = address_list
cj_last_mile_hs.loc[args.start:args.end, 'longitude'] = lon_list
cj_last_mile_hs.loc[args.start:args.end, 'latitude'] = lat_list
cj_last_mile_hs.to_csv(f"cj_last_mile_hs_{args.start}_{args.end}.csv", index = False)
