from datetime import datetime

from snownlp import SnowNLP

from util.getPublicData import *


def getTableDataPageData():
    return getAllCiPingTotal()


def getTableData(hotWord):
    commentList = getAllCommentsData()
    tableData = []
    for comment in commentList:
        if comment[4].find(hotWord) != -1:
            tableData.append(comment)
    return tableData


def getTableDataEchartsData(hotWord):
    tableList = getTableData(hotWord)
    xData = [x[1] for x in tableList]
    xData = list(set(xData))
    xData = list(sorted(xData, key=lambda x: datetime.strptime(x, '%Y-%m-%d').timestamp(), reverse=True))
    yData = [0 for x in range(len(xData))]
    for comment in tableList:
        for index, x in enumerate(xData):
            if comment[1] == x:
                yData[index] += 1
    return xData, yData


def getTableDataArticle(flag):
    if flag:
        tableListOld = getAllData()
        tableList = []
        for item in tableListOld:
            item = list(item)
            emotionValue = SnowNLP(item[5]).sentiments
            if emotionValue > 0.5:
                emotionValue = '正面'
            elif emotionValue == 0.5:
                emotionValue = '中性'
            elif emotionValue < 0.5:
                emotionValue = '负面'
            item.append(emotionValue)
            tableList.append(item)
    else:
        tableList = getAllData()
    return tableList
