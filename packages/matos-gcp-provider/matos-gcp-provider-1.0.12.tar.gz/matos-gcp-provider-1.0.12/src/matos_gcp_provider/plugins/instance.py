# -*- coding: utf-8 -*-
from typing import Any, Dict
from matos_gcp_provider.lib import factory
from matos_gcp_provider.lib.base_provider import BaseProvider
from ..config import RESOURCE_TYPE_REQUESTS

# INVERTED_TYPES = {x: y for y, x in ASSET_TYPES.items()}


class GCPInstance(BaseProvider):
    """GCP instance class

    Args:
        BaseProvider (Class): Base provider class
    """

    def __init__(self, resource: Dict, **kwargs) -> None:
        """
        Construct instance service
        """
        self.resource = resource
        self.resource_type = "instance"
        self.project_id = resource.pop("project_id")
        super().__init__(**kwargs)

    def get_inventory(self) -> Any:
        """
        Service discovery
        """
        instances = []
        for request_type in RESOURCE_TYPE_REQUESTS[self.resource_type]:
            resources = self._get_assets(self.project_id, request_type)
            for resource in resources:
                instances.append({
                    'type': 'instance',
                    **resource.get('resource').get('data')
                })
        return instances
        # old code
        # resources = self._get_assets(self.project_id, INVERTED_TYPES[self.resource_type])
        # instances = []
        # for resource in resources:
        #     instances.append({
        #         'type': 'instance',
        #         'name': resource['resource']['data']['name'],
        #         'instance_id': resource['resource']['data']['id'],
        #         'project_id': self.project_id,
        #         'location': resource['resource']['data']['zone'].split('/')[-1],
        #     })

        # return instances


def register() -> Any:
    """Register plugins type"""
    factory.register("instance", GCPInstance)
    