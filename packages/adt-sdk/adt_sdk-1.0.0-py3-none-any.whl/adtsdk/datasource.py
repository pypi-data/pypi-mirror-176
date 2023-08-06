from enum import Enum
from typing import Dict, Union

from requests import Response

from adtsdk.core import AdtApiClient, session_check
from adtsdk.exceptions import (
    DataSourceNotCreated,
    DataSourceNotDeleted,
    InternalServerError,
)


class DataFormat(str, Enum):
    """Enum of possible data formats."""

    CSV = 'CSV'
    NDJSON = 'NDJSON'

    def __str__(self) -> str:
        return str(self.value)


class DataSources(AdtApiClient):
    """ADT Upload API client for adding or deleting data sources."""

    @property
    def scope(self) -> str:
        return 'datasource'

    @session_check
    def add_datasource(
        self,
        name: str,
        data_format: DataFormat,
    ) -> Dict[str, Union[str, int]]:
        """Calls API to create new stream data source.

        Parameters
        ----------
        name : str
            Name of the new data source
        data_format : DataFormat
            Data format of the new data source

        Raises
        ------
        DataSourceNotCreated
            When the data source failed be created
        InternalServerError
            When 5xx status code was received from the server

        Returns
        -------
        Dict[str, Union[str, int]]
            JSON with `status_code` and `reason`
        """
        url = self._build_url(f'{name}/stream')
        params = {'data_format': str(data_format)}
        resp = self._session.put(url, headers=self.headers, params=params)
        self._handle_5xx(resp)
        if resp.status_code >= 400:
            raise DataSourceNotCreated(resp.status_code, resp.reason)
        return self._deserialize_response(resp)

    @session_check
    def delete_datasource(
        self,
        name: str,
    ) -> Dict[str, Union[str, int]]:
        """Calls API endpoint to delete existing datasource

        Parameters
        ----------
        name : str
            Name of the existing datasource to remove

        Raises
        ------
        DataSourceNotDeleted
            When the data source failed be deleted
        InternalServerError
            When 5xx status code was received from the server

        Returns
        -------
        Dict[str, Union[str, int]]
            JSON with `status_code` and `reason`
        """
        url = self._build_url(f'default-{name}')
        resp = self._session.delete(url, headers=self.headers)
        self._handle_5xx(resp)
        if resp.status_code >= 400:
            raise DataSourceNotDeleted(resp.status_code, resp.reason)
        return self._deserialize_response(resp)

    @staticmethod
    def _handle_5xx(server_response: Response) -> None:
        """Handles response from the server and potential errors.

        Parameters
        ----------
        server_response : response
            Response object from the server

        Raises
        ------
        InternalServerError
            When the status code is 5xx
        """
        if server_response.status_code >= 500:
            raise InternalServerError(
                status_code=server_response.status_code,
                message=server_response.reason,
            )

    @staticmethod
    def _deserialize_response(
        server_response: Response,
    ) -> Dict[str, Union[str, int]]:
        """Formats the response into dictionary to be returned to the client.

        Parameters
        ----------
        response : Response
            Response object from the server

        Returns
        -------
        Dict[str, Union[str, int]]
            JSON with `status_code` and `reason`
        """
        return {
            'status_code': server_response.status_code,
            'reason': server_response.reason,
        }
