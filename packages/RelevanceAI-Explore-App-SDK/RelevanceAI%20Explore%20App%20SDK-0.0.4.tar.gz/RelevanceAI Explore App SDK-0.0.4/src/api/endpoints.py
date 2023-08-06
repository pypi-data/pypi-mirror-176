import requests

from src import __version__
from src.types import Credentials

from typing import Optional, Dict, Any


class Endpoints:
    def __init__(
        self, credentials: Credentials, job_id: str = None, name: str = None
    ) -> None:
        self._credentials = credentials
        self._base_url = (
            f"https://api-{self._credentials.region}.stack.relevance.ai/latest"
        )
        self._headers = dict(
            Authorization=f"{self._credentials.project}:{self._credentials.api_key}",
        )

    def _create_deployable(
        self, dataset_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None
    ):
        return requests.post(
            url=self._base_url + "/deployables/create",
            headers=self._headers,
            json=dict(
                dataset_id=dataset_id,
                configuration={} if config is None else config,
            ),
        ).json()

    def _share_deployable(self, deployable_id: str):
        return requests.post(
            url=self._base_url + f"/deployables/{deployable_id}/share",
            headers=self._headers,
        ).json()

    def _unshare_deployable(self, deployable_id: str):
        return requests.post(
            url=self._base_url + f"/deployables/{deployable_id}/private",
            headers=self._headers,
        ).json()

    def _update_deployable(
        self,
        deployable_id: str,
        dataset_id: str,
        configuration: Optional[Dict] = None,
        overwrite: bool = True,
        upsert: bool = True,
    ):
        return requests.post(
            url=self._base_url + f"/deployables/{deployable_id}/update",
            headers=self._headers,
            json=dict(
                dataset_id=dataset_id,
                configuration=configuration,
                overwrite=overwrite,
                upsert=upsert,
            ),
        ).json()

    def _get_deployable(self, deployable_id: str):
        return requests.get(
            url=self._base_url + f"/deployables/{deployable_id}/get",
            headers=self._headers,
        ).json()

    def _delete_deployable(self, deployable_id: str):
        return requests.post(
            url=self._base_url + f"/deployables/delete",
            headers=self._headers,
            json=dict(
                id=deployable_id,
            ),
        ).json()

    def _list_deployables(self, page_size: int):
        return requests.get(
            url=self._base_url + "/deployables/list",
            headers=self._headers,
            params=dict(
                page_size=page_size,
            ),
        ).json()
