"""CasaTunes: Init"""
import logging

from aiohttp import ClientResponse
from typing import List

from datetime import datetime

from .const import API_PORT
from .objects.base import CasaBase
from .objects.system import CasaTunesSystem
from .objects.zone import CasaTunesZone
from .objects.source import CasaTunesSource
from .objects.media import CasaTunesMedia
from .client import CasaClient


class CasaTunes(CasaBase):
    """Interacting with CasaTunes API."""

    logger = logging.getLogger(__name__)

    def __init__(self, client: "CasaClient", host: str) -> None:
        """Initialize the appliance."""
        self._client = client
        self._host = host
        self._system: CasaTunesSystem

        self._zones: List[CasaTunesZone] = []
        self._zones_dict: dict = {}

        self._sources: List[CasaTunesSource] = []
        self._sources_dict: dict = {}

        self._media: List[CasaTunesMedia] = []
        self._media_dict: dict = {}

    @property
    def host(self) -> str:
        return self._host

    @property
    def system(self) -> dict:
        return self._system

    @property
    def zones(self) -> dict:
        return self._zones

    @property
    def zones_dict(self) -> dict:
        return self._zones_dict

    @property
    def sources(self) -> dict:
        return self._sources

    @property
    def sources_dict(self) -> dict:
        return self._sources_dict

    @property
    def media(self) -> dict:
        return self._media

    @property
    def media_dict(self) -> dict:
        return self._media_dict

    async def fetch(self) -> None:
        """Fetch data from CasaTunes zone."""
        data: dict = {}
        data["system"] = await self.get_system()
        data["zones"] = await self.get_zones()
        data["sources"] = await self.get_sources()
        data["media"] = await self.get_media()

        return data

    async def get_system(self) -> None:
        """Get System."""
        response: ClientResponse = await self._client.get(
            f"http://{self._host}:{API_PORT}/api/v1/system/info"
        )
        json = await response.json()
        self.logger.debug(json)
        system = [CasaTunesSystem(self._client, json)]
        self._system = system[0]

    async def get_zones(self) -> None:
        """Get Zones."""
        response: ClientResponse = await self._client.get(
            f"http://{self._host}:{API_PORT}/api/v1/zones"
        )
        json = await response.json()
        self.logger.debug(json)
        self._zones = [CasaTunesZone(self._client, ZoneID) for ZoneID in json or []]

        self._zones_dict: dict = {}
        for zone in self._zones:
            self._zones_dict[zone.ZoneID] = zone

    async def get_sources(self) -> CasaTunesSource:
        """Get Sources."""
        response = await self._client.get(
            f"http://{self._host}:{API_PORT}/api/v1/sources"
        )
        json = await response.json()
        self.logger.debug(json)
        self._sources = [
            CasaTunesSource(self._client, SourceID) for SourceID in json or []
        ]

        self._sources_dict: dict = {}
        for source in self._sources:
            self._sources_dict[source.SourceID] = source

    async def get_media(self) -> CasaTunesMedia:
        response = await self._client.get(
            f"http://{self._host}:{API_PORT}/api/v1/sources/nowplaying"
        )
        json = await response.json()
        self.logger.debug(json)
        self._media = [
            CasaTunesMedia(self._client, SourceID) for SourceID in json or []
        ]

        self._media_dict: dict = {}
        for media in self._media:
            self._media_dict[media.SourceID] = media
            media.last_updated_at = datetime.utcnow()

    async def turn_on(self, zone_id):
        return await self._client.get(
            f"http://{self._host}:{API_PORT}/api/v1/zones/{zone_id}?Power=on"
        )

    async def turn_off(self, zone_id):
        return await self._client.get(
            f"http://{self._host}:{API_PORT}/api/v1/zones/{zone_id}?Power=off"
        )

    async def mute_volume(self, zone_id, mute):
        return await self._client.get(
            f"http://{self._host}:{API_PORT}/api/v1/zones/{zone_id}?Mute={mute}"
        )

    async def set_volume_level(self, zone_id, volume):
        return await self._client.get(
            f"http://{self._host}:{API_PORT}/api/v1/zones/{zone_id}?Volume={volume}"
        )

    async def change_source(self, zone_id, source):
        """Send player action and option."""
        return await self._client.get(
            f"http://{self._host}:{API_PORT}/api/v1/zones/{zone_id}?SourceID={source}"
        )

    async def player_action(self, zone_id, action, option=""):
        """Send player action and option."""
        return await self._client.get(
            f"http://{self._host}:{API_PORT}/api/v1/zones/{zone_id}/player/{action}/{option}"
        )

    async def zone_master(self, zone_id, mode):
        """Set Zone master flag."""
        response = await self._client.get(
            f"http://{self._host}:{API_PORT}/api/v1/zones/{zone_id}/?MasterMode={mode}"
        )
        json = await response.json()
        self.logger.debug(json)

    async def zone_join(self, zone_id, client_zone_id):
        """Join a CasaTunes zone with a zone."""
        response = await self._client.get(
            f"http://{self._host}:{API_PORT}/api/v1/zones/{zone_id}/group/{client_zone_id}"
        )
        json = await response.json()
        self.logger.debug(json)

    async def zone_unjoin(self, zone_id, client_zone_id):
        """Unjoin a CasaTunes zone with a zone."""
        response = await self._client.get(
            f"http://{self._host}:{API_PORT}/api/v1/zones/{zone_id}/ungroup/{client_zone_id}"
        )
        json = await response.json()
        self.logger.debug(json)
