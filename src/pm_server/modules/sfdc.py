import json
import os
import requests
import time
from .config import config

class sfdc :
    def __init__(self) :
        self.obj_config = config()
        self.headers = {'Authorization': 'Bearer ',
                        'Content-Type': 'application/json'}
        self.endpoint = self.obj_config.params['sfdc_endpoint']

    def login(self) :
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        params = {'grant_type': 'password',
                  'client_id': self.obj_config.params['sfdc_client_id'],
                  'client_secret': self.obj_config.params['sfdc_client_secret'],
                  'username': self.obj_config.params['sfdc_username'],
                  'password': self.obj_config.params['sfdc_password']}
        response = requests.post('https://test.salesforce.com/services/oauth2/token', data=params, headers=headers)
        data = json.loads(response.text)

        if 'access_token' in data :
            # fh = open(self.obj_config.params['private_assets_path'] + 'sfdc.txt', 'w+')
            # fh.write(response.text)
            # fh.close()

            self.headers['Authorization'] = self.headers['Authorization'] + data['access_token']

            return True

        return False

    def list_accounts(self) :
        response = requests.get(self.endpoint + 'services/data/v20.0/query/?q=SELECT+name+from+Account', headers=self.headers)

        data = json.loads(response.text)
        if 'totalSize' in data and data['totalSize'] > 0 :
            print(data['records'])

        return list

    def list_tenants(self) :
        response = requests.get(self.endpoint + 'services/data/v20.0/query/?q=SELECT+Name,+main_domain__c,+Account_Name__c,+environment_status__c+from+OneTenant__c', headers=self.headers)

        data = json.loads(response.text)
        if 'totalSize' in data and data['totalSize'] > 0 :
            return data['records']

        return list

    def list_contracts(self) :
        response = requests.get(self.endpoint + 'services/data/v20.0/query/?q=SELECT+OneTenant__c,+contract_end_date__c,+hac_sum__c,+hdc_sum__c,+hsb_sum__c,+dlp_sum__c,+archive_sum__c,+hos_sum__c,+sub_total_price_sum__c	+from+OneContractType__c', headers=self.headers)

        data = json.loads(response.text)
        if 'totalSize' in data and data['totalSize'] > 0 :
            return data['records']

        return list

    def list_connects(self) :
        response = requests.get(self.endpoint + 'services/data/v20.0/query/?q=SELECT+Contact__c,+OneTenant__c,+Distribution_Channel__c,+support_flag__c,+renewal_flag__c,+emergency_flag__c+from+OneConnect__c', headers=self.headers)

        data = json.loads(response.text)
        if 'totalSize' in data and data['totalSize'] > 0 :
            return data['records']

        return False

    def list_contacts(self) :
        response = requests.get(self.endpoint + 'services/data/v20.0/query/?q=SELECT+Email,+Name,+Phone+from+Contact', headers=self.headers)

        data = json.loads(response.text)
        if 'totalSize' in data and data['totalSize'] > 0 :
            return data['records']

        return False

    def save_connects(self, id='', data={}) :
        data = {'emergency_flag__c': 'true',
                'support_flag__c': 'false',
                'renewal_flag__c': 'true'}
        response = requests.patch(self.endpoint + 'services/data/v20.0/sobjects/OneConnect__c/' + str(id), headers=self.headers, data=json.dumps(data))

        return True
