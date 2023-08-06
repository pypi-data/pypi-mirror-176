from gcore_flavors_api_old import Flavors
from gcore_floatingips_api_old import FloatingIPs
from gcore_instances_api import Instances
from gcore_loadbalancers_api import Loadbalancers
from gcore_networks_api import Networks
from gcore_regions_api_old import Regions
from gcore_reserved_fixed_ips_api import ReservedFixedIPs
from gcore_routers_api_old import Routers
from gcore_subnets_api import Subnets
from gcore_useractions_api import Useractions
from gcore_volumes_api import Volumes


class GCoreAPI:
    def __init__(self, token: str, project_id: int):
        self.token = token
        self.project_id = project_id

    @property
    def routers(self):
        return Routers(token=self.token, project_id=self.project_id)

    @property
    def flavors(self):
        return Flavors(token=self.token, project_id=self.project_id)

    @property
    def regions(self):
        return Regions(token=self.token, project_id=self.project_id)

    @property
    def floatingips(self):
        return FloatingIPs(token=self.token, project_id=self.project_id)

    @property
    def networks(self):
        return Networks(token=self.token, project_id=self.project_id)

    @property
    def subnets(self):
        return Subnets(token=self.token, project_id=self.project_id)

    @property
    def useractions(self):
        return Useractions(token=self.token, project_id=self.project_id)

    @property
    def reserved_fixed_ips(self):
        return ReservedFixedIPs(token=self.token, project_id=self.project_id)

    @property
    def volumes(self):
        return Volumes(token=self.token, project_id=self.project_id)

    @property
    def instances(self):
        return Instances(token=self.token, project_id=self.project_id)

    @property
    def loadbalancers(self):
        return Loadbalancers(token=self.token, project_id=self.project_id)



