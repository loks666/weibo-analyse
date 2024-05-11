import csv
import os
import time
from datetime import datetime

import requests


def init():
    if not os.path.exists('articleData.csv'):
        with open('articleData.csv', 'w', encoding='utf8', newline='') as csvfile:
            wirter = csv.writer(csvfile)
            wirter.writerow([
                'id',
                'likeNum',
                'commentsLen',
                'reposts_count',
                'region',
                'content',
                'contentLen',
                'created_at',
                'type',
                'detailUrl',  # followBtnCode>uid + mblogid
                'authorAvatar',
                'authorName',
                'authorDetail',
                'isVip'  # v_plus
            ])


def wirterRow(row):
    with open('articleData.csv', 'a', encoding='utf8', newline='') as csvfile:
        wirter = csv.writer(csvfile)
        wirter.writerow(row)


def get_json(url, params):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Cookie': 'SINAGLOBAL=8689001798899.339.1693398052536; SCF=AiwT_hOmoAOtEPiT3EiW1EwnsVQQBPUCcpyhzCMmUKyM_YAC45VYKYuA7w1TPJhLLbxV83a1ivWlKwLJvUcpVs4.; ULV=1711699170115:10:2:1:3827696145003.674.1711699170096:1711164209573; XSRF-TOKEN=7OJCa3h7Z2LtqqcOpUvVq2UE; ALF=1715349117; SUB=_2A25LEuktDeRhGeBL41UX8ynNwj6IHXVobmTlrDV8PUJbkNB-LUvakW1NRt0rM4z7X_X7kEvA1dvfKTLF4l-_xxDD; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFdW.7JbH86ecG-OaB9YKfL5JpX5KMhUgL.Foqf1hMce0Mp1Kz2dJLoIpjLxKML1hnLBo2LxKnLBK.LBo.LxK-LBKqLB--t; WBPSESS=HH3PttadquOLqzk2Y84XyKqBs07EsARIAzwN9McBVtfMWzRMzmKu38SYikQVX19CuHZ4Ap6h6EbJ9-H7xC5Imcn-U5LytQ09p_YtpIgGe6Kc_eLF7IK9pzji0XAbdx7npFW9M_NP0EUMnN2qPnlAcg==',
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def parse_json(response, type):
    for article in response:
        id = article['id']
        likeNum = article['attitudes_count']
        commentsLen = article['comments_count']
        reposts_count = article['reposts_count']
        try:
            region = article['region_name'].replace('发布于 ', '')
        except:
            region = '无'
        content = article['text_raw']
        contentLen = article['textLength']
        created_at = datetime.strptime(article['created_at'], "%a %b %d %H:%M:%S %z %Y").strftime("%Y-%m-%d")
        type = type
        try:
            detailUrl = 'https://weibo.com/' + str(article['user']['id']) + '/' + str(article['mblogid'])
        except:
            detailUrl = '无'
        authorAvatar = article['user']['avatar_large']
        authorName = article['user']['screen_name']
        authorDetail = 'https://weibo.com' + article['user']['profile_url']
        if article['user']['v_plus']:
            isVip = article['user']['v_plus']
        else:
            isVip = 0
        wirterRow([
            id,
            likeNum,
            commentsLen,
            reposts_count,
            region,
            content,
            contentLen,
            created_at,
            type,
            detailUrl,
            authorAvatar,
            authorName,
            authorDetail,
            isVip
        ])


def start(typeNum=10, pageNum=2):
    articleUrl = 'https://weibo.com/ajax/feed/hottimeline'
    init()
    typeNumCount = 0
    with open('./navData.csv', 'r', encoding='utf8') as readerFile:
        reader = csv.reader(readerFile)
        next(reader)
        for nav in reader:
            if typeNumCount > typeNum: return
            for page in range(0, pageNum):
                time.sleep(2)
                print('正在爬取类型：' + nav[0] + '中的第' + str(page + 1) + '页数据')
                params = {
                    'group_id': nav[1],
                    'containerid': nav[2],
                    'max_id': page,
                    'count': 10,
                    'extparam': 'discover|new_feed'
                }
                response = get_json(articleUrl, params)
                parse_json(response['statuses'], nav[0])
            typeNumCount += 1


if __name__ == '__main__':
    start()
