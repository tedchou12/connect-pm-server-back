import json
import os
import requests
import time
from .config import config

class one_garden :
    def __init__(self) :
        self.obj_config = config()
        self.endpoint = 'https://api.service.hdems.com/customers/%s/domains'

    def get_domains(self, domain='') :
        headers = {'x-api-key': self.obj_config.params['one_garden_api_key'],
                  'authorization': self.obj_config.params['one_garden_auth']}
        endpoint = self.endpoint % domain
        response = requests.get(endpoint, headers=headers)
        data = json.loads(response.text)

        if 'customer_id' in data :
            return data['customer_domains']

        return False
