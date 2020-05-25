import requests
import json


class BasicSNC:

    def __init__(self,usr,pwd,host):
        self.usr=usr
        self.pwd=pwd
        self.host=host
        self.header={"Content-Type":"application/json","Accept":"application/json"}



    def sncget(self,url):

        response = requests.get(url, auth=(self.usr, self.pwd), headers=self.header)

        # Check for HTTP codes other than 200
        if response.status_code != 200:
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
            exit()

        # Decode the JSON response into a dictionary and use the data
        data = response.json()
        return data

    def sncput(self,url,data):
        data = json.dumps(data)

        response = requests.put(url, auth=(self.usr, self.pwd), headers=self.header, data=data)

        # Check for HTTP codes other than 200
        if response.status_code != 200:
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
            exit()

        # Decode the JSON response into a dictionary and use the data
        data = response.json()
        print(data)


    def queue(self,table,query):
        list_=list()
        url = self.host +'/api/now/table/'+table+'?sysparm_query='+query
        print(url)
        response = BasicSNC.sncget(self,url)
        response = response.get('result','')
        for element in response:
            list_.append(element.get('sys_id',''))


        return list_

    def getShdescAndDesc(self,table,sys_id):
        url=self.host +'/api/now/table/'+table+'/'+sys_id

        data = self.sncget(url)

        sh_desc = data['result']['short_description']
        desc = data['result']['description']
        return (sh_desc,desc)


    def getCaller(self,url):
        data = self.sncget(url)


        return data['result']['u_display_name']
    def getCallDetails(self,sys_id):
        #returns dictionary with all needed details
        #sh_desc, desc, e-mail body, caller url
        d=dict()
        url = self.host +'/api/now/table/new_call/'+sys_id
        data = self.sncget(url)

        d['short_description'] = data['result']['short_description']
        d['description'] = data['result']['description']
        d['caller'] = self.getCaller(data['result']['opened_by']['link'])
        d['email_body'] = data['result']['u_email_body']

        return d

    def updateCall(self,sys_id, data):
        url = self.host + '/api/now/table/new_call/' + sys_id
        self.sncput(url,data)




