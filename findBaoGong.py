# -*- coding: UTF-8 -*-
# __author__ = 'guyongzx'
# __date__ = '2022-04-17'

import json
import requests
from time import sleep
import random

# ## init config ###
# 填写个人信息

deviceid = 'x'
authtoken = 'x'
# deliveryType = 2  # 1：极速达 2：全城配送
# cartDeliveryType = 2  # 1：极速达 2：全城配送


def address_list():
    global addressList_item
    print('###初始化地址')
    myUrl = 'https://api-sams.walmartmobile.cn/api/v1/sams/sams-user/receiver_address/address_list'
    headers = {
        'Host': 'api-sams.walmartmobile.cn',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'SamClub/5.0.45 (iPhone; iOS 15.4; Scale/3.00)',
        'device-name': 'iPhone14,3',
        'device-os-version': '15.4',
        'device-id': deviceid,
        'device-type': 'ios',
        'auth-token': authtoken,
        'app-version': '5.0.45.1'
    }
    requests.packages.urllib3.disable_warnings()
    ret = requests.get(url=myUrl, headers=headers, verify=False)
    myRet = ret.json()
    addressList = myRet['data'].get('addressList')
    addressList_item = []

    for i in range(0, len(addressList)):
        addressList_item.append({
            'addressId': addressList[i].get("addressId"),
            'mobile': addressList[i].get("mobile"),
            'name': addressList[i].get("name"),
            'countryName': addressList[i].get('countryName'),
            'provinceName': addressList[i].get('provinceName'),
            'cityName': addressList[i].get('cityName'),
            'districtName': addressList[i].get('districtName'),
            'receiverAddress': addressList[i].get('receiverAddress'),
            'detailAddress': addressList[i].get('detailAddress'),
            'latitude': addressList[i].get('latitude'),
            'longitude': addressList[i].get('longitude')
        })
        print('[' + str(i) + ']' + str(addressList[i].get("name")) + str(addressList[i].get("mobile")) + str(addressList[i].get(
            "districtName")) + str(addressList[i].get("receiverAddress")) + str(addressList[i].get("detailAddress")))
    print('根据编号选择地址:')
    s = int(input())
    addressList_item = addressList_item[s]
    # print(addressList_item)
    return addressList_item


def getRecommendStoreListByLocation(latitude, longitude):
    global uid
    global good_store

    storeList_item = []
    print('###初始化商店')
    myUrl = 'https://api-sams.walmartmobile.cn/api/v1/sams/merchant/storeApi/getRecommendStoreListByLocation'
    data = {
        'longitude': longitude,
        'latitude': latitude}
    headers = {
        'Host': 'api-sams.walmartmobile.cn',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'Content-Type': 'application/json;charset=UTF-8',
        'Content-Length': '45',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'SamClub/5.0.45 (iPhone; iOS 15.4; Scale/3.00)',
        'device-name': 'iPhone14,3',
        'device-os-version': '15.4',
        'device-id': deviceid,
        'latitude': latitude,
        'device-type': 'ios',
        'auth-token': authtoken,
        'app-version': '5.0.45.1'
    }
    try:
        requests.packages.urllib3.disable_warnings()
        ret = requests.post(url=myUrl, headers=headers, data=json.dumps(data), verify=False)
        myRet = ret.json()
        storeList = myRet['data'].get('storeList')
        for i in range(0, len(storeList)):
            storeList_item.append(
                {
                    'storeType': storeList[i].get("storeType"),
                    'storeId': storeList[i].get("storeId"),
                    'areaBlockId': storeList[i].get('storeAreaBlockVerifyData').get("areaBlockId"),
                    'storeDeliveryTemplateId': storeList[i].get('storeRecmdDeliveryTemplateData').get(
                        "storeDeliveryTemplateId"),
                    'deliveryModeId': storeList[i].get('storeDeliveryModeVerifyData').get("deliveryModeId"),
                    'storeName': storeList[i].get("storeName")
                })
            print('[' + str(i) + ']' + str(storeList_item[i].get("storeId")) + str(storeList_item[i].get("storeName")))
        print('根据编号下单商店:')
        s = int(input())
        good_store = storeList_item[s]
        uidUrl = 'https://api-sams.walmartmobile.cn/api/v1/sams/sams-user/user/personal_center_info'
        requests.packages.urllib3.disable_warnings()
        ret = requests.get(url=uidUrl, headers={
            'Host': 'api-sams.walmartmobile.cn',
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': 'SamClub/5.0.45 (iPhone; iOS 15.4; Scale/3.00)',
            'device-name': 'iPhone14,3',
            'device-os-version': '15.4',
            'device-id': deviceid,
            'latitude': latitude,
            'device-type': 'ios',
            'auth-token': authtoken,
            'app-version': '5.0.45.1'
        }, verify=False)
        # print(ret.text)
        uidRet = json.loads(ret.text)
        uid = uidRet['data']['memInfo']['uid']
        return storeList_item, uid

    except Exception as e:
        print('getRecommendStoreListByLocation [Error]: ' + str(e))
        return False

def getBaoGongInfo(uid, address):
    global isGo
    myUrl = 'https://api-sams.walmartmobile.cn/api/v1/sams/decoration/portal/show/getPageData'
    data = {
        "uid": uid,
        "pageContentId": "1187641882302384150",
        "addressInfo": {
            "provinceCode": "",
            "receiverAddress": address['detailAddress'],
            "districtCode": "",
            "cityCode": ""
        },
        "authorize": True,
        "latitude": address.get('latitude'),
        "longitude": address.get('longitude')
    }
    headers = {
        'Host': 'api-sams.walmartmobile.cn',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'Content-Type': 'application/json;charset=UTF-8',
        'Content-Length': '45',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'SamClub/5.0.45 (iPhone; iOS 15.4; Scale/3.00)',
        'device-name': 'iPhone14,3',
        'device-os-version': '15.4',
        'device-id': deviceid,
        'latitude': address.get('latitude'),
        'device-type': 'ios',
        'auth-token': authtoken,
        'app-version': '5.0.45.1'
    }
    requests.packages.urllib3.disable_warnings()
    ret = requests.post(url=myUrl, headers=headers, data=json.dumps(data), verify=False)
    myRet = ret.json()
    if not myRet['success']:
        return
    else:
        goodlist = myRet['data']['pageModuleVOList'][2]['renderContent']['goodsList']
        for good in goodlist:
            if int(good['spuStockQuantity']) > 0:
                print("有货!!! 详情" + good['subTitle'])
                if addCart(uid, good):
                    isGo = False
            else:
                print("无货... 详情" + good['subTitle'])

def addCart(uid, good):
    myUrl = 'https://api-sams.walmartmobile.cn/api/v1/sams/trade/cart/addCartGoodsInfo'
    data = {
        "uid": uid,
        "cartGoodsInfoList": [
            {
                "spuId": good['spuId'],
                "storeId": good['storeId'],
                "increaseQuantity": 1,
                "price": good['priceInfo'][0]['price'],
                "goodsName": good['title']
            }
        ]
    }
    headers = {
        'Host': 'api-sams.walmartmobile.cn',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'Content-Type': 'application/json;charset=UTF-8',
        'Content-Length': '45',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'SamClub/5.0.45 (iPhone; iOS 15.4; Scale/3.00)',
        'device-name': 'iPhone14,3',
        'device-os-version': '15.4',
        'device-id': deviceid,
        'latitude': address.get('latitude'),
        'device-type': 'ios',
        'auth-token': authtoken,
        'app-version': '5.0.45.1'
    }
    requests.packages.urllib3.disable_warnings()
    ret = requests.post(url=myUrl, headers=headers, data=json.dumps(data), verify=False)
    myRet = ret.json()
    if not myRet['success']:
        print("加入购物车失败... " + good['subTitle'])
        return False
    else:
        print("加入购物车成功!!! " + good['subTitle'])
        return True


# 加入bark通知 url地址改为自己的!!!
def notify(name):
    myUrl = 'https://api.day.app/xxxx/保供有货!!!/' + name
    try:
        requests.packages.urllib3.disable_warnings()
        requests.get(url=myUrl, verify=False)
    except Exception as e:
        print('notify [Error]: ' + str(e))


def init():
    address = address_list()
    store, uid = getRecommendStoreListByLocation(address.get('latitude'), address.get('longitude'))
    return address, store, uid


if __name__ == '__main__':
    thCount = 1
    count = 0
    isGo = True
    deliveryTime = []
    goodlist = []
    # 初始化,应该不需要做重试处理
    address, store, uid = init()
    # 获取购物车信息,高峰期需要重试
    while isGo:
        # getUserCart(address, store, uid)
        getBaoGongInfo(uid, address)
        sleep_time = random.randint(2000, 5000) / 1000
        sleep(sleep_time)
    print("已经加入购物车")
    # notify("已经加入购物车")

