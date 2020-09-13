from typing import Any, Dict, List, Mapping, Optional

from aiofreepybox.access import Access


class Airmedia:
    """
    Airmedia
    """

    def __init__(self, access: Access) -> None:
        self._access = access

    action = ["start", "stop"]

    media_type = ["photo", "video"]

    airmedia_data_schema = {
        "action": action[0],
        "media": "",
        "media_type": media_type[1],
        "password": "",
        "position": 0,
    }

    async def get_airmedia_receivers(self) -> Optional[List[Dict[str, Any]]]:
        """
        Get airmedia receivers
        """
        return await self._access.get("airmedia/receivers/")

    async def send_airmedia(
        self, receiver_name: str, airmedia_data: Dict[str, Any]
    ) -> None:
        """
        Send airmedia

        receiver_name : `str`
        airmedia_data : `dict`
        """
        await self._access.post(f"airmedia/receivers/{receiver_name}/", airmedia_data)

    async def get_airmedia_configuration(self) -> Optional[Dict[str, bool]]:
        """
        Get airmedia configuration
        """
        return await self._access.get("airmedia/config/")

    async def set_airmedia_configuration(
        self, airmedia_config: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Set airmedia configuration

        airmedia_config : `dict`
        """
        return await self._access.put("airmedia/config/", airmedia_config)

    async def update_airmedia_configuration(
        self, enabled: Optional[bool] = None, password: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Update airmedia configuration

        enabled : `bool`, optional
            , Default to None
        password : `str`, optional
            , Default to None
        """

        if enabled is None and password is None:
            return None

        config: Dict[str, Any] = {}
        if enabled is not None:
            config.update({"enabled": enabled})
        if password is not None:
            config.update({"password": password})
        return await self.set_airmedia_configuration(config)
