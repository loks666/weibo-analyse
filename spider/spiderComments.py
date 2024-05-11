import csv
import os
from datetime import datetime

import requests


def init():
    if not os.path.exists('commentsData.csv'):
        with open('commentsData.csv', 'w', encoding='utf8', newline='') as csvfile:
            wirter = csv.writer(csvfile)
            wirter.writerow([
                'articleId',
                'created_at',
                'like_counts',
                'region',
                'content',
                'authorName',
                'authorGender',
                'authorAddress',
                'authorAvatar'
            ])


def wirterRow(row):
    with open('commentsData.csv', 'a', encoding='utf8', newline='') as csvfile:
        wirter = csv.writer(csvfile)
        wirter.writerow(row)


def get_html(url, id):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Cookie': 'SINAGLOBAL=8689001798899.339.1693398052536; SCF=AiwT_hOmoAOtEPiT3EiW1EwnsVQQBPUCcpyhzCMmUKyM_YAC45VYKYuA7w1TPJhLLbxV83a1ivWlKwLJvUcpVs4.; ULV=1711699170115:10:2:1:3827696145003.674.1711699170096:1711164209573; XSRF-TOKEN=7OJCa3h7Z2LtqqcOpUvVq2UE; ALF=1715349117; SUB=_2A25LEuktDeRhGeBL41UX8ynNwj6IHXVobmTlrDV8PUJbkNB-LUvakW1NRt0rM4z7X_X7kEvA1dvfKTLF4l-_xxDD; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFdW.7JbH86ecG-OaB9YKfL5JpX5KMhUgL.Foqf1hMce0Mp1Kz2dJLoIpjLxKML1hnLBo2LxKnLBK.LBo.LxK-LBKqLB--t; WBPSESS=HH3PttadquOLqzk2Y84XyKqBs07EsARIAzwN9McBVtfMWzRMzmKu38SYikQVX19CuHZ4Ap6h6EbJ9-H7xC5Imcn-U5LytQ09p_YtpIgGe6Kc_eLF7IK9pzji0XAbdx7npFW9M_NP0EUMnN2qPnlAcg==',
    }
    params = {
        'is_show_bulletin': 2,
        'id': id
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def parse_json(response, articleId):
    commentList = response['data']
    for comment in commentList:
        created_at = datetime.strptime(comment['created_at'], "%a %b %d %H:%M:%S %z %Y").strftime("%Y-%m-%d")
        like_counts = comment['like_counts']
        authorName = comment['user']['screen_name']
        authorGender = comment['user']['gender']
        authorAddress = comment['user']['location'].split(' ')[0]
        authorAvatar = comment['user']['avatar_large']
        try:
            region = comment['source'].replace('来自', '')
        except:
            region = '无'
        content = comment['text_raw']
        wirterRow([
            articleId,
            created_at,
            like_counts,
            region,
            content,
            authorName,
            authorGender,
            authorAddress,
            authorAvatar,
        ])


def start():
    init()
    url = 'https://weibo.com/ajax/statuses/buildComments'
    with open('./articleData.csv', 'r', encoding='utf8') as readerFile:
        reader = csv.reader(readerFile)
        next(reader)
        for article in reader:
            articleId = article[0]
            response = get_html(url, articleId)
            parse_json(response, articleId)


if __name__ == '__main__':
    start()
