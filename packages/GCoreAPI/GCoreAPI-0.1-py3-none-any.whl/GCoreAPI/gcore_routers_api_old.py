from typing import List, Dict

import requests


class Routers:
    api_url = "https://api.edgecenter.ru/cloud/v1/routers"
    err_desc = ""

    def __init__(self, token: str, project_id: int):
        self.token = token
        self.project_id = project_id
        self.auth_header = {'Authorization': f'APIKey {self.token}'}

    def get_router(self, router_id: str, region_id: int) -> dict:
        url = f'{self.api_url}/{self.project_id}/{region_id}/{router_id}'

        try:
            response = requests.get(url=url, headers=self.auth_header)
            if response.status_code == 200:
                return response.json()
        except Exception as err:
            err_desc = err

        print(f"Request ERROR: {self.err_desc}")
        return {}

    def list_routers(self, region_id: int) -> dict:
        url = f'{self.api_url}/{self.project_id}/{region_id}'

        try:
            response = requests.get(url=url, headers=self.auth_header)
            if response.status_code == 200:
                return response.json()
        except Exception as err:
            err_desc = err

        print(f"Request ERROR: {self.err_desc}")
        return {}

    def create_router(self, region_id: int,
                      name: str = None,
                      routes: List = None,
                      interfaces: List = None,
                      external_gateway_info: Dict = None,
                      params: Dict = None) -> dict:
        url = f'{self.api_url}/{self.project_id}/{region_id}'

        if name is None and params is None:
            print("Can't create router without necessary parameters 'name' or dict 'params' with key 'name'!")

        if routes is None:
            routes = []
        if interfaces is None:
            interfaces = []
        if external_gateway_info is None:
            external_gateway_info = {}

        if params is not None:
            routes = params['routes']
            interfaces = params['interfaces']
            external_gateway_info = params['external_gateway_info']
            if 'name' not in params.keys() and name is None:
                print("Can't create router without necessary parameters 'name' or dict 'params' with key 'name'!")
            elif 'name' in params.keys():
                name = params['name']
                name = name[:61]

        headers = self.auth_header
        headers.update({'Content-Type': 'application/json'})
        body: Dict = {'routes': routes}
        body.update({'interfaces': interfaces})
        body.update({'external_gateway_info': external_gateway_info})
        body.update({'name': name})

        try:
            response = requests.post(url=url, json=body, headers=headers)
            if response.status_code == 200:
                return response.json()
        except Exception as err:
            err_desc = err

        print(f"Request ERROR: {self.err_desc}")
        return {}

    def delete_router(self, region_id: int, router_id: str = None, router_name: str = None) -> dict:
        if router_id is None and router_name is None:
            print("Enter name or router ID to delete router!")
            return {}

        if router_id is None and router_name is not None:
            list_routers = self.list_routers(region_id=region_id)

            for router in list_routers['results']:
                if router['name'] == router_name:
                    router_id = router['id']

        url = f'{self.api_url}/{self.project_id}/{region_id}/{router_id}'

        try:
            response = requests.delete(url=url, headers=self.auth_header)
            if response.status_code == 200:
                return response.json()
        except Exception as err:
            err_desc = err

        print(f"Request ERROR: {self.err_desc}")
        return {}

    def update_router(self, region_id: int,
                      router_id: str = None,
                      router_name: str = None,
                      routes: List = None,
                      external_gateway_info: Dict = None) -> dict:
        if router_id is None and router_name is None:
            print("Enter name or router ID to update router!")
            return {}

        if router_id is None and router_name is not None:
            list_routers = self.list_routers(region_id=region_id)

            for router in list_routers['results']:
                if router['name'] == router_name:
                    router_id = router['id']

        url = f'{self.api_url}/{self.project_id}/{region_id}/{router_id}'

        if routes is None:
            routes = []
        if external_gateway_info is None:
            external_gateway_info = {}

        headers = self.auth_header
        headers.update({'Content-Type': 'application/json'})
        body: Dict = {'routes': routes}
        body.update({'external_gateway_info': external_gateway_info})

        try:
            response = requests.patch(url=url, json=body, headers=headers)
            if response.status_code == 200:
                return response.json()
        except Exception as err:
            err_desc = err

        print(f"Request ERROR: {self.err_desc}")
        return {}

    def attach_subnet(self, region_id: int, subnet_id: str, router_id: str = None, router_name: str = None) -> dict:
        if router_id is None and router_name is None:
            print("Enter router name or router ID to attach subnet to router!")
            return {}

        if router_id is None and router_name is not None:
            list_routers = self.list_routers(region_id=region_id)

            for router in list_routers['results']:
                if router['name'] == router_name:
                    router_id = router['id']

        url = f'{self.api_url}/{self.project_id}/{region_id}/{router_id}/attach'

        headers = self.auth_header
        headers.update({'Content-Type': 'application/json'})
        body: Dict = {'subnet_id': subnet_id}

        try:
            response = requests.post(url=url, json=body, headers=headers)
            if response.status_code == 200:
                return response.json()
        except Exception as err:
            err_desc = err

        print(f"Request ERROR: {self.err_desc}")
        return {}

    def detach_subnet(self, region_id: int, subnet_id: str, router_id: str = None, router_name: str = None) -> dict:
        if router_id is None and router_name is None:
            print("Enter router name or router ID to attach subnet to router!")
            return {}

        if router_id is None and router_name is not None:
            list_routers = self.list_routers(region_id=region_id)

            for router in list_routers['results']:
                if router['name'] == router_name:
                    router_id = router['id']

        url = f'{self.api_url}/{self.project_id}/{region_id}/{router_id}/attach'

        headers = self.auth_header
        headers.update({'Content-Type': 'application/json'})
        body: Dict = {'subnet_id': subnet_id}

        try:
            response = requests.patch(url=url, json=body, headers=headers)
            if response.status_code == 200:
                return response.json()
        except Exception as err:
            err_desc = err

        print(f"Request ERROR: {self.err_desc}")
        return {}

