from typing import Optional, Dict, Any

from src.api import endpoints, helpers
from src.dashboard import dashboard

from src import constants
from src import errors


class Client:
    def __init__(self, token: str) -> None:

        self._credentials = helpers.process_token(token)
        self._token = token
        self._endpoints = endpoints.Endpoints(credentials=self._credentials)

        try:
            response = self.list_deployables()
        except:
            raise errors.AuthException
        else:
            self._deployables = sorted(
                response["deployables"], key=lambda x: x["insert_date_"]
            )
            print(constants.WELCOME_MESSAGE.format(self._credentials.project))

    @property
    def deployables(self):
        return self._deployables

    def recent(self) -> dashboard.Dashboard:
        kwargs = self.deployables[-1]
        return dashboard.Dashboard(endpoints=self._endpoints, **kwargs)

    def list_deployables(self, page_size: int = 1000):
        return self._endpoints._list_deployables(page_size=page_size)

    def create_deployable(
        self,
        dataset_id: Optional[str] = None,
        deployable_id: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        if deployable_id is None:
            return self._endpoints._create_deployable(
                dataset_id=dataset_id,
                config=config,
            )
        else:
            return self._endpoints._get_deployable(
                deployable_id=deployable_id,
            )

    def delete_deployable(self, deployable_id: str) -> None:
        return self._endpoints._delete_deployable(deployable_id=deployable_id)

    def Deployable(
        self,
        dataset_id: Optional[str] = None,
        delpoyable_id: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
    ) -> dashboard.Dashboard:
        assert all(
            param is not None for param in locals().values()
        ), "Set either `dataset_id` and `config` or `deployable_id`"
        response = self.create_deployable(
            dataset_id=dataset_id, deployable_id=delpoyable_id, config=config
        )
        return dashboard.Dashboard(endpoints=self._endpoints, **response)
