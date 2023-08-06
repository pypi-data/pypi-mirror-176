from typing import List, Dict

import requests


class FloatingIPs:
    api_url = "https://api.edgecenter.ru/cloud/v1/floatingips"
    err_desc = ""

    def __init__(self, token: str, project_id: int):
        self.token = token
        self.project_id = project_id
        self.auth_header = {'Authorization': f'APIKey {self.token}'}

    def list_ip(self, region_id: int) -> dict:
        url = f'{self.api_url}/{self.project_id}/{region_id}'

        try:
            response = requests.get(url=url, headers=self.auth_header)
            if response.status_code == 200:
                return response.json()
        except Exception as err:
            err_desc = err

        print(f"Request ERROR: {self.err_desc}")
        return {}

    def create_ip(self, region_id: int,
                  metadata: dict = None,
                  port_id: str = None,
                  fixed_ip_address: str = None) -> dict:
        url = f'{self.api_url}/{self.project_id}/{region_id}'

        headers = self.auth_header
        headers.update({'Content-Type': 'application/json'})

        body: Dict = {}
        if metadata is not None:
            body.update({'metadata': metadata})
        if port_id is not None:
            body.update({'port_id': port_id})
        if fixed_ip_address is not None:
            body.update({'fixed_ip_address': fixed_ip_address})

        try:
            response = requests.post(url=url, json=body, headers=headers)
            if response.status_code == 200:
                return response.json()
        except Exception as err:
            err_desc = err

        print(f"Request ERROR: {self.err_desc}")
        return {}

    def delete_ip(self, region_id: int, pk: str) -> dict:
        url = f'{self.api_url}/{self.project_id}/{region_id}/{pk}'

        try:
            response = requests.delete(url=url, headers=self.auth_header)
            if response.status_code == 200:
                return response.json()
        except Exception as err:
            err_desc = err
            return {}

        if response.status_code == 404:
            print("IP not found")

        print(f"Request ERROR: {self.err_desc}")
        return {}

    def get_ip(self, region_id: int, pk: str) -> dict:
        url = f'{self.api_url}/{self.project_id}/{region_id}/{pk}'

        try:
            response = requests.get(url=url, headers=self.auth_header)
            if response.status_code == 200:
                return response.json()
        except Exception as err:
            err_desc = err
            return {}

        if response.status_code == 404:
            print("IP not found")

        print(f"Request ERROR: {self.err_desc}")
        return {}

    def assign_ip_to_lb(self, region_id: int,
                        pk: str,
                        port_id: str,
                        metadata: dict = None,
                        fixed_ip_address: str = None) -> dict:
        url = f'{self.api_url}/{self.project_id}/{region_id}/{pk}/assign'

        headers = self.auth_header
        headers.update({'Content-Type': 'application/json'})

        body: Dict = {'port_id': port_id}
        if metadata is not None:
            body.update({'metadata': metadata})
        if fixed_ip_address is not None:
            body.update({'fixed_ip_address': fixed_ip_address})

        try:
            response = requests.post(url=url, json=body, headers=headers)
            if response.status_code == 200:
                return response.json()
        except Exception as err:
            err_desc = err
            return {}

        if response.status_code == 404:
            print("IP not found")

        print(f"Request ERROR: {self.err_desc}")
        return {}

    def unassign_ip(self, region_id: int, pk: str) -> dict:
        url = f'{self.api_url}/{self.project_id}/{region_id}/{pk}/unassign'

        try:
            response = requests.post(url=url, headers=self.auth_header)
            if response.status_code == 200:
                return response.json()
        except Exception as err:
            err_desc = err
            return {}

        if response.status_code == 404:
            print("IP not found")

        print(f"Request ERROR: {self.err_desc}")
        return {}

    def get_available_ip(self, region_id: int) -> dict:
        url = f'{self.api_url}/{self.project_id}/{region_id}'

        try:
            response = requests.get(url=url, headers=self.auth_header)
            if response.status_code == 200:
                return response.json()
        except Exception as err:
            err_desc = err

        print(f"Request ERROR: {self.err_desc}")
        return {}

    def list_network_metadata(self, region_id: int, pk: str) -> dict:
        url = f'{self.api_url}/{self.project_id}/{region_id}/{pk}/metadata'

        try:
            response = requests.get(url=url, headers=self.auth_header)
            if response.status_code == 200:
                return response.json()
        except Exception as err:
            err_desc = err

        print(f"Request ERROR: {self.err_desc}")
        return {}

    def update_ip_metadata(self, region_id: int, pk: str, key: dict) -> bool:
        url = f'{self.api_url}/{self.project_id}/{region_id}/{pk}/metadata'

        for elem in key.keys():
            if len(elem) > 255 or len(key[elem]) > 1024:
                print(f"Too long key name '{elem}'!")
                return False

        headers = self.auth_header
        headers.update({'Content-Type': 'application/json'})

        body: Dict = key

        response = None
        try:
            response = requests.post(url=url, json=body, headers=headers)
            if response.ok:
                return True
        except Exception as err:
            err_desc = f"{err}"

        if response is None:
            print(f"Request ERROR: {self.err_desc}")
        if response is not None:
            if not response.ok:
                print(f"Request ERROR. Response status code {response.status_code}")
        return False

    def replace_ip_metadata(self, region_id: int, pk: str, key: dict) -> bool:
        url = f'{self.api_url}/{self.project_id}/{region_id}/{pk}/metadata'

        for elem in key.keys():
            if len(elem) > 255 or len(key[elem]) > 1024:
                print(f"Too long key name '{elem}'!")
                return False

        headers = self.auth_header
        headers.update({'Content-Type': 'application/json'})

        body: Dict = key

        response = None
        try:
            response = requests.put(url=url, json=body, headers=headers)
            if response.ok:
                return True
        except Exception as err:
            err_desc = err

        if response is None:
            print(f"Request ERROR: {self.err_desc}")
        if response is not None:
            if not response.ok:
                print(f"Request ERROR. Response status code {response.status_code}")
        return False

    def delete_ip_metadata(self, region_id: int, pk: str, key: str) -> bool:
        url = f'{self.api_url}/{self.project_id}/{region_id}/{pk}/metadata_item?key={key}'

        headers = self.auth_header

        response = None
        try:
            response = requests.delete(url=url, headers=headers)
            if response.ok:
                return True
        except Exception as err:
            err_desc = err

        if response is None:
            print(f"Request ERROR: {self.err_desc}")
        if response is not None:
            if not response.ok:
                print(f"Request ERROR. Response status code {response.status_code}")
        return False

    def get_ip_metadata(self, region_id: int, pk: str, key: str) -> dict:
        url = f'{self.api_url}/{self.project_id}/{region_id}/{pk}/metadata_item?key={key}'

        headers = self.auth_header

        response = None
        try:
            response = requests.get(url=url, headers=headers)
            if response.ok:
                return response.json()
        except Exception as err:
            err_desc = err

        if response is None:
            print(f"Request ERROR: {self.err_desc}")
        if response is not None:
            if not response.ok:
                print(f"Request ERROR. Response status code {response.status_code}")
        return {}



