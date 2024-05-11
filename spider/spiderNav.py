import csv
import os

import numpy as np
import requests


def init():
    if not os.path.exists('navData.csv'):
        with open('navData.csv', 'w', encoding='utf8', newline='') as csvfile:
            wirter = csv.writer(csvfile)
            wirter.writerow([
                'typeName',
                'gid',
                'containerid'
            ])


def wirterRow(row):
    with open('navData.csv', 'a', encoding='utf8', newline='') as csvfile:
        wirter = csv.writer(csvfile)
        wirter.writerow(row)


def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Cookie': 'SINAGLOBAL=8689001798899.339.1693398052536; SCF=AiwT_hOmoAOtEPiT3EiW1EwnsVQQBPUCcpyhzCMmUKyM_YAC45VYKYuA7w1TPJhLLbxV83a1ivWlKwLJvUcpVs4.; ULV=1711699170115:10:2:1:3827696145003.674.1711699170096:1711164209573; XSRF-TOKEN=7OJCa3h7Z2LtqqcOpUvVq2UE; ALF=1715349117; SUB=_2A25LEuktDeRhGeBL41UX8ynNwj6IHXVobmTlrDV8PUJbkNB-LUvakW1NRt0rM4z7X_X7kEvA1dvfKTLF4l-_xxDD; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFdW.7JbH86ecG-OaB9YKfL5JpX5KMhUgL.Foqf1hMce0Mp1Kz2dJLoIpjLxKML1hnLBo2LxKnLBK.LBo.LxK-LBKqLB--t; WBPSESS=HH3PttadquOLqzk2Y84XyKqBs07EsARIAzwN9McBVtfMWzRMzmKu38SYikQVX19CuHZ4Ap6h6EbJ9-H7xC5Imcn-U5LytQ09p_YtpIgGe6Kc_eLF7IK9pzji0XAbdx7npFW9M_NP0EUMnN2qPnlAcg==',
    }
    params = {
        'is_new_segment': 1,
        'fetch_hot': 1
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def parse_json(response):
    navList = np.append(response['groups'][3]['group'], response['groups'][4]['group'])
    for nav in navList:
        navName = nav['title']
        gid = nav['gid']
        containerid = nav['containerid']
        wirterRow([
            navName,
            gid,
            containerid,
        ])


if __name__ == '__main__':
    url = 'https://weibo.com/ajax/feed/allGroups'
    init()
    response = get_html(url)
    parse_json(response)
