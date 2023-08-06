from typing import List, Dict

import requests


class Flavors:
    api_url = "https://api.edgecenter.ru/cloud/v1"
    err_desc = ""

    def __init__(self, token: str, project_id: int):
        self.token = token
        self.project_id = project_id
        self.auth_header = {'Authorization': f'APIKey {self.token}'}

    def list_flavors(self, region_id: int,
                     include_prices: bool = True,
                     disabled: bool = True,
                     exclude_windows: bool = False) -> dict:
        url = f'{self.api_url}/flavors/{self.project_id}/{region_id}'

        headers = self.auth_header
        headers.update({'Content-Type': 'application/json'})
        body: Dict = {'include_prices': include_prices}
        body.update({'disabled': disabled})
        body.update({'exclude_windows': exclude_windows})

        try:
            response = requests.get(url=url, json=body, headers=headers)
            if response.status_code == 200:
                return response.json()
        except Exception as err:
            err_desc = err

        print(f"Request ERROR: {self.err_desc}")
        return {}

    def list_flavors_k8(self, region_id: int,
                        exclude_sgx: bool = True,
                        exclude_gpu: bool = True,
                        include_prices: bool = True) -> dict:
        url = f'{self.api_url}/k8s/{self.project_id}/{region_id}/flavors'

        headers = self.auth_header
        headers.update({'Content-Type': 'application/json'})
        body: Dict = {'include_prices': include_prices}
        body.update({'exclude_sgx': exclude_sgx})
        body.update({'exclude_gpu': exclude_gpu})

        try:
            response = requests.get(url=url, json=body, headers=headers)
            if response.status_code == 200:
                return response.json()
        except Exception as err:
            err_desc = err

        print(f"Request ERROR: {self.err_desc}")
        return {}

    def list_flavors_baremetal(self, region_id: int,
                               include_prices: bool = True,
                               disabled: bool = True,
                               exclude_windows: bool = False) -> dict:
        url = f'{self.api_url}/bmflavors/{self.project_id}/{region_id}'

        headers = self.auth_header
        headers.update({'Content-Type': 'application/json'})
        body: Dict = {'include_prices': include_prices}
        body.update({'disabled': disabled})
        body.update({'exclude_windows': exclude_windows})

        try:
            response = requests.get(url=url, json=body, headers=headers)
            if response.status_code == 200:
                return response.json()
        except Exception as err:
            err_desc = err

        print(f"Request ERROR: {self.err_desc}")
        return {}

    def list_flavors_baremetal_default(self, region_id: int,
                                       include_prices: bool = True,
                                       disabled: bool = True,
                                       exclude_windows: bool = False) -> dict:
        url = f'{self.api_url}/bmflavors/{region_id}'

        headers = self.auth_header
        headers.update({'Content-Type': 'application/json'})
        body: Dict = {'include_prices': include_prices}
        body.update({'disabled': disabled})
        body.update({'exclude_windows': exclude_windows})

        try:
            response = requests.get(url=url, json=body, headers=headers)
            if response.status_code == 200:
                return response.json()
        except Exception as err:
            err_desc = err

        print(f"Request ERROR: {self.err_desc}")
        return {}

    def list_flavors_baremetal_available(self, region_id: int,
                                         windows_os: bool = False,
                                         disabled: bool = True,
                                         client_id: int = 0) -> dict:
        url = f'{self.api_url}/bm_reservation_flavors/{region_id}'

        headers = self.auth_header
        headers.update({'Content-Type': 'application/json'})
        body: Dict = {'windows_os': windows_os}
        body.update({'disabled': disabled})
        body.update({'client_id': client_id})

        try:
            response = requests.get(url=url, json=body, headers=headers)
            if response.status_code == 200:
                return response.json()
        except Exception as err:
            err_desc = err

        print(f"Request ERROR: {self.err_desc}")
        return {}
