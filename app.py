# coding=utf-8

from flask import Flask, make_response, request
import sqlite3
import pandas as pd

app = Flask(__name__)


@app.route('/list')
def getRegionList():  # put application's code here
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('select distinct regionName from data')
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    res = {'allRegion': result}
    response = make_response(res)
    return response


@app.route('/confirmed')
def getConfirmedNum():
    region_name = request.args.get('regionName')
    num = request.args.get('num')
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('select time, confirmedNumber from data where regionName=?', (region_name, ))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    num = int(num)
    if num > 0:
        result = result[:num]
    res = {'data': result}
    response = make_response(res)
    return response


@app.route('/cured')
def getCuredNum():
    region_name = request.args.get('regionName')
    num = request.args.get('num')
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('select time, curedNumber from data where regionName=?', (region_name,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    num = int(num)
    if num > 0:
        result = result[:num]
    res = {'data': result}
    response = make_response(res)
    return response


@app.route('/dead')
def getDeadNum():
    region_name = request.args.get('regionName')
    num = request.args.get('num')
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('select time, deadNumber from data where regionName=?', (region_name,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    num = int(num)
    if num > 0:
        result = result[:num]
    res = {'data': result}
    response = make_response(res)
    return response


def createTable():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('''create table data
    (
    regionName varchar(12),
    time timestamp ,
    confirmedNumber varchar(12),
    curedNumber varchar(12),
    deadNumber varchar(12)
    )
    ''')


def storeData():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    raw_data = pd.read_csv('DXYArea.csv')
    data = []
    regions = []
    for index, each in raw_data.iterrows():
        if each['countryName'] == each['provinceName']:
            region = each['countryName']
        else:
            region = each['countryName'] + each['provinceName']
        if region in regions:
            temp_time = each['updateTime']
            confirmCount = each['province_confirmedCount']
            deadCount = each['province_deadCount']
            curedCount = each['province_curedCount']
            temp_index = 0
            for item in data:
                if item['region_name'] == region:
                    break
                temp_index += 1
            data[temp_index]['confirm'].append(list((temp_time, confirmCount)))
            data[temp_index]['dead'].append(list((temp_time, deadCount)))
            data[temp_index]['cured'].append(list((temp_time, curedCount)))
        else:
            regions.append(region)
            temp_time = each['updateTime']
            confirmCount = each['province_confirmedCount']
            deadCount = each['province_deadCount']
            curedCount = each['province_curedCount']
            temp_dict = {'region_name': region, 'confirm': [], 'dead': [], 'cured': []}
            temp_dict['confirm'].append(list((temp_time, confirmCount)))
            temp_dict['dead'].append(list((temp_time, deadCount)))
            temp_dict['cured'].append(list((temp_time, curedCount)))
            data.append(temp_dict)
    for each_data in data:
        region_name = each_data['region_name']
        for i in range(len(each_data['confirm'])):
            time = each_data['confirm'][i][0]
            confirm = each_data['confirm'][i][1]
            cured = each_data['cured'][i][1]
            dead = each_data['dead'][i][1]
            cursor.execute('insert into data values (?, ?, ?, ?, ?)',
                           (region_name, str(time), confirm, cured, dead))
    cursor.close()
    conn.commit()
    conn.close()


if __name__ == '__main__':
    try:
        createTable()
        storeData()
    except:
        pass
    app.run(port=5001)
