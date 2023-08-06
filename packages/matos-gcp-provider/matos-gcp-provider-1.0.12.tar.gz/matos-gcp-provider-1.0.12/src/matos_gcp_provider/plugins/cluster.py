# -*- coding: utf-8 -*-
from typing import Any, Dict
from matos_gcp_provider.lib import factory
from matos_gcp_provider.lib.base_provider import BaseProvider
from ..config import ASSET_TYPES

INVERTED_TYPES = {x: y for y, x in ASSET_TYPES.items()}


class GCPCluster(BaseProvider):
    """GCL cluster service plugins

    Args:
        BaseProvider (Class): base provider class
    """
    def __init__(self, resource: Dict, **kwargs) -> None:
        """
        Construct cluster service
        """

        self.resource = resource
        self.resource_type = "cluster"
        self.project_id = resource.pop("project_id")
        super().__init__(**kwargs)

    def get_inventory(self) -> Any:
        """
        Service discovery
        """
        resources = self._get_assets(self.project_id, INVERTED_TYPES[self.resource_type])
        clusters = []

        for resource in resources:
            clusters.append({
                'type': 'cluster',
                'name': resource['resource']['data']['name'],
                'project_id': self.project_id,
                'location': resource['resource']['data']['zone'],
            })

        return clusters


def register() -> Any:
    """Register plugins type"""
    factory.register("cluster", GCPCluster)
    