"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""

from __future__ import (
    annotations,
)

import logging
from typing import (
    NoReturn,
)

from minos.common import (
    MinosConfig,
    MinosSetup,
)

from ..utils import (
    get_host_ip,
)
from .clients import (
    MinosDiscoveryClient,
)

logger = logging.getLogger(__name__)


class DiscoveryConnector(MinosSetup):
    """Discovery Connector class."""

    def __init__(self, client, name: str, host: str, port: int, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.client = client

        self.name = name
        self.host = host
        self.port = port

    @classmethod
    def _from_config(cls, *args, config: MinosConfig, **kwargs) -> DiscoveryConnector:
        client = MinosDiscoveryClient(host=config.discovery.host, port=config.discovery.port)
        port = config.rest.port
        name = config.service.name
        host = get_host_ip()
        return cls(client=client, name=name, host=host, port=port, *args, **kwargs)

    async def _setup(self) -> NoReturn:
        await self.subscribe()

    async def subscribe(self) -> NoReturn:
        """Send a subscribe operation to the discovery.

        :return: This method does not return anything.
        """
        logger.info("Performing discovery subscription...")
        await self.client.subscribe(self.host, self.port, self.name)

    async def _destroy(self) -> NoReturn:
        await self.unsubscribe()

    async def unsubscribe(self) -> NoReturn:
        """Send an unsubscribe operation to the discovery.

        :return: This method does not return anything.
        """
        logger.info("Performing discovery unsubscription...")
        await self.client.unsubscribe(self.name)
