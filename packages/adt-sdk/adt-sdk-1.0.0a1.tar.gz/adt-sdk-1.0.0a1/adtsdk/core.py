import functools
import os
import re
import time
from typing import Callable, Dict, Optional, Tuple, Union

import requests
from requests import Response
from requests.adapters import HTTPAdapter, Retry

from adtsdk.constants import API_VERSION
from adtsdk.exceptions import (
    ERROR_TO_EXCEPTION,
    ClientNotInitialized,
    ErrorCodes,
    InternalServerError,
)


def session_check(func: Callable):
    """Decorator for AdtApiClient to decorate its methods which depend on the
    internal session object to be initialized. If the session object is not
    initialized raises ClientNotInitialized.

    Raises
    ------
    ClientNotInitialized
        When the wrapped method is not running within the context manager
        of its client.
    """

    @functools.wraps(func)
    def wrapper(ref, *args, **kwargs):
        if ref._session is None:  # pylint: disable=protected-access
            raise ClientNotInitialized(
                'The method must be called within context manager of the'
                ' client.'
            )
        return func(ref, *args, **kwargs)

    return wrapper


class AdtApiClient:

    """ADT API client for data upload and data sources management.

    Parameters
    ----------
    api_server_url : str
        ADT Upload API server URL
    jwt_auth_token : str
        JWT authentication token
    timeout : float
        How long to wait for the server to send data before giving up
    retry_policy : Retry
        Request retrying policy to use for retrying. If not provided
        a default policy will be applied.
    http_proxy : Optional[str]
        HTTP proxy URL
    https_proxy : Optional[str]
        HTTPS proxy URL
    """

    def __init__(
        self,
        api_server_url: str,
        jwt_auth_token: str,
        timeout: float = 30.0,
        retry_policy: Retry = Retry(
            total=5, backoff_factor=2.0, status_forcelist=[500]
        ),
        http_proxy: Optional[str] = None,
        https_proxy: Optional[str] = None,
    ):
        self._api_server_url = api_server_url.rstrip('/')
        self._jwt_auth_token = jwt_auth_token
        self._timeout = timeout
        self._retry_policy = retry_policy
        self._http_proxy = http_proxy or os.getenv('HTTP_PROXY')
        self._https_proxy = https_proxy or os.getenv('HTTPS_PROXY')
        self._session = None

    def __enter__(self):
        self._session = requests.Session()
        self._session.mount(
            'https://', HTTPAdapter(max_retries=self._retry_policy)
        )
        self._session.proxies = {}
        if self._http_proxy:
            self._session.proxies['http'] = self._http_proxy
        if self._https_proxy:
            self._session.proxies['https'] = self._https_proxy
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self._session.close()
        self._session = None

    @property
    def scope(self) -> str:
        """API endpoint scope"""
        raise NotImplementedError('Shall be implemented by subclass')

    @property
    def headers(self) -> Dict[str, str]:
        """Builds authentication header with JWT authentication token

        Returns
        -------
        Dict[str, str]
            Header dict to be passed to the upload initiation requests
        """
        return {'Authorization': f'Bearer {self._jwt_auth_token}'}

    @staticmethod
    def _validate_stream_name(stream_name: str) -> None:
        """Validates input parameters.

        Parameters
        ----------
        stream_name : str
            Name of the data source where to upload the data

        Raises
        ------
        ValueError
            When the `stream_name` is ill-formatted
        """
        if re.search('-', stream_name):
            raise ValueError('"stream_name" cannot contain "-"')

    def _build_url(self, endpoint: str) -> str:
        """Builds endpoint full URL

        Parameters
        ----------
        endpoint : str
            The part of the endpoint path

        Returns
        -------
        str
            Full endpoint URL
        """
        base = f'{self._api_server_url}/{API_VERSION}/{self.scope}'
        return f'{base}/{endpoint.lstrip("/")}'

    @staticmethod
    def _get_error_code(server_response: Response) -> ErrorCodes:
        """Gets `error_code` from response JSON and handles error without
        `error_code` or unknown error code as unknown error.

        Parameters
        ----------
        server_response : Response
            Response object from the server

        Returns
        -------
        ErrorCodes
            Error code instance

        Raises
        ------
        UnknownServerError
            When the `error_code` is either not in the response JSON or
            it is of unknown value.
        """
        resp_json = server_response.json()
        err_code = resp_json.get('error_code')
        try:
            err_code = ErrorCodes(err_code)
        except ValueError as exc:
            raise InternalServerError(
                status_code=server_response.status_code,
                message=server_response.reason,
            ) from exc
        return err_code

    def _retry_4xx(
        self,
        method: Callable,
        error_codes: Tuple[ErrorCodes, ...] = tuple(),
        white_list: Tuple[ErrorCodes, ...] = tuple(),
        total: Optional[int] = None,
        backoff_factor: Optional[Union[int, float]] = None,
        **method_kw,
    ) -> Response:
        """Retries the REST request method if specific `error_code` is returned
        in the server response. It retries only specific `error_codes` and
        it can ignore specific error codes in the `white_list` and will return
        the response, which is useful e.g. when the uploaded chunk has already
        been uploaded - this can happen when client retries the whole upload
        with the same `upload_id`.

        Parameters
        ----------
        method : Callable
            Method from `requests` that performs the REST request and
            shall be retried
        error_codes : Tuple[ErrorCodes, ...]
            Tuple of error codes returned by server in the response that
            shall be retried by the client
        white_list : Tuple[ErrorCodes, ...]
            Optional tuple of error codes which shall be ignored
        total : Optional[int]
            Number of retries to perform before giving up
        backoff_factor : Optional[Union[int, float]]
            The retrying of the retry-able exceptions is done with exponential
            back-off with provided back-off factor. If not provided a default
            value will be applied.
        **method_kw : Dict[str, Any]
            Key-word arguments to be passed to the callable `method`

        Returns
        -------
        Response
            Response object returned from server

        Raises
        ------
        UnknownServerError
            Either when the `error_code` is not in the response message,
            or when the `error_code` is unknown.
        UploadBaseException
            A specific sub-class of this base exception is raised
            based on the `error_code` in the response message.
        """
        retries = 0
        total_ = total or self._retry_policy.total
        assert total_ > 0, 'Total retries must be non-zero positive integer'
        backoff_factor_ = backoff_factor or self._retry_policy.backoff_factor
        assert (
            backoff_factor_ > 0
        ), 'Back-off factor must be non-zero positive integer of float'
        while retries < total_:
            resp = method(**method_kw)
            if 400 <= resp.status_code < 500:
                # Handle PayloadTooLarge
                if resp.status_code == 413:
                    err_code = ErrorCodes.PAYLOAD_TOO_LARGE
                    raise ERROR_TO_EXCEPTION[err_code](resp.reason)

                err_code = self._get_error_code(resp)

                # Check if the error code is in white list
                if err_code in white_list:
                    break

                resp_json = resp.json()
                err_message = resp_json['message']
                if err_code in error_codes:
                    sleep_time = backoff_factor_ * 2**retries
                    time.sleep(sleep_time)
                    retries += 1
                    continue

                # Not in white list nor retry-able hence raising
                raise ERROR_TO_EXCEPTION[err_code](err_message)

            break

        if retries == total:
            # retry-able exception reached maximum of retries hence raising
            raise ERROR_TO_EXCEPTION[err_code](err_message)

        return resp
