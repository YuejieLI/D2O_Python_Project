import json
import requests
import time
import os
import sys

# https://auuorkqkh.accounts.ondemand.com/admin
# https://abac83m6p.accounts.ondemand.com/admin/ S4C80
# User Group Name: ExternalSandbox0, ExternalSandbox1, ExternalSandbox2 and ExternalSandbox3
# System Administrator's credentials: 'Username: UpdatePassword / Password: Sandbox1'

print('---------------------------------------------------------------------------------------------------------------------------------------------------------------------')

print("This application is for deactivating 400 TRAINXXX users at IAS tenant 'https://auuorkqkh.accounts.ondemand.com'. Please quite this script if you are not responsible")

print('---------------------------------------------------------------------------------------------------------------------------------------------------------------------')

headers = {
        'Content-Type': 'application/scim+json'  # can not be 'application/json' in this case, scim is a must

        }



def deActivateUser():



    userNameList = []
    userIdList = []

    global i
    global j

    for i in range(0,400):  # (0, 400)
        #把数字i转换成字符串，然后调用字符串的zfill方法，限定三位，不足前面补零，举例： 1=001
        userNameList.append('TRAIN'+str(i).zfill(3))


    for j in range(7, 407):  	# (7, 407)  407-->TRAIN399 对应 P000406，range的第二位减一位 407 - 1 = 406
        userIdList.append('P000'+str(j).zfill(3))

    # print(userNameList)
    # print(userIdList)


    url_Users = 'https://auuorkqkh.accounts.ondemand.com/service/scim/Users/'
    #
    username = '55d76093-9a02-44cd-a6c8-6a534fbdfc92'  # refer to System Administrator 'UpdatePassword'
    password = input(f'==>Please enter your PASSCODE: ')




    try:
        for i in range(len(userIdList)):
            body = {
                "emails": [
                    {
                        "primary": True,
                        "value": userNameList[i]+"@education.cloud.sap"
                    }
                ],
                "name": {
                    "familyName": userNameList[i]
                    # "givenName": givenNameList[i]  given name in this IAS is not necessary
                },
                "schemas": [
                    "urn:ietf:params:scim:schemas:core:2.0:User"
                ],
                "userName": userNameList[i],   # equals login name
                # "userName": familyNameList[i],   # equals login name
                # "password": setPassword,
                # "active": True,
                "active": False,
                "passwordStatus": "enabled",
                "id": userIdList[i]  # 第0个开始 也就是P000000
            }

            body1 = json.dumps(body)

            r = requests.put(url=url_Users+userIdList[i], data=body1, headers=headers, auth=(username, password))
            # time.sleep(1)
            responseCode = r.status_code
            if responseCode == 200:
                print(f'- ResponseCode: {responseCode} [User {userNameList[i]} is deactivated successful]')
            else:
                print(f'- deactivating user {userNameList[i]} failed due to return code: {responseCode}.')
                time.sleep(10)
                sys.exit()

    except requests.exceptions.ConnectionError:
        print('Connection is lost due to timeout error! Please check your Internet connection and try again.')
        print('Current window will close in 10 seconds......')

    else:

        print(f'==> In total {len(userIdList)} users have been deactivated successfully. \n Current window will be closed in next 20 seconds.')




deActivateUser()


time.sleep(20)



