from typing import List, Dict

import requests


class Regions:
    api_url = "https://api.edgecenter.ru/cloud/v1/regions"
    err_desc = ""

    def __init__(self, token: str, project_id: int):
        self.token = token
        self.project_id = project_id
        self.auth_header = {'Authorization': f'APIKey {self.token}'}

    def get_region(self, region_id: int, show_volume_types: bool = True) -> dict:
        url = f'{self.api_url}/{region_id}'

        headers = self.auth_header
        headers.update({'Content-Type': 'application/json'})
        body: Dict = {'show_volume_types': show_volume_types}
        try:
            response = requests.get(url=url, json=body, headers=headers)
            if response.status_code == 200:
                return response.json()
        except Exception as err:
            err_desc = err

        print(f"Request ERROR: {self.err_desc}")
        return {}

    def list_region(self, show_volume_types: bool = False) -> dict:
        url = f'{self.api_url}'

        headers = self.auth_header
        headers.update({'Content-Type': 'application/json'})
        body: Dict = {'show_volume_types': show_volume_types}

        try:
            response = requests.get(url=url, json=body, headers=headers)
            if response.status_code == 200:
                return response.json()
        except Exception as err:
            err_desc = err

        print(f"Request ERROR: {self.err_desc}")
        return {}

    def get_city_id_by_name(self, region_name: str) -> int:
        list_regions = self.list_region()
        for region in list_regions['results']:
            if region['display_name'].lower() == region_name.strip().lower():
                return int(region['id'])

    def get_city_name_by_id(self, region_id: int) -> str:
        list_regions = self.list_region()
        for region in list_regions['results']:
            if int(region['id']) == region_id:
                return str(region['display_name'])

    def get_cities(self, country: str = None) -> List:
        cities = []
        list_regions = self.list_region()
        for region in list_regions['results']:
            if region['country'].lower() == country.lower():
                cities.append(region['display_name'])
        return cities

    def get_countries(self) -> List:
        countries = []
        list_regions = self.list_region()
        for region in list_regions['results']:
            countries.append(region['country'])

        return countries
