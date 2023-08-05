from io import BytesIO, FileIO
from pathlib import Path
from typing import Dict, Optional, Union

import pandas as pd

from adtsdk.constants import CHUNK_SIZE
from adtsdk.core import AdtApiClient, session_check
from adtsdk.exceptions import ErrorCodes


class Uploader(AdtApiClient):
    """ADT Upload API client for uploading files, pandas dataframes,
    or any byte-stream data in the ADT compliant data format.
    """

    @property
    def scope(self) -> str:
        return 'upload'

    def upload(
        self,
        stream_name: str,
        data: Optional[Union[BytesIO, FileIO, pd.DataFrame]] = None,
        file_path: Optional[Path] = None,
        retry_total: Optional[int] = None,
        backoff_factor: Optional[Union[int, float]] = None,
    ) -> Dict[str, str]:
        """Based on the provided data/file_path size uploads the data either
        using single upload type (for small uploads), or chunks the data
        and uploads the data chunk by chunk.

        Parameters
        ----------
        stream_name : str
            Name of the data source where to upload the data
        data : Optional[Union[BytesIO, FileIO, pd.DataFrame]]
            Variant data object to upload, it can be either byte-stream object,
            or file-like object, or pandas DataFrame. Cannot be set if
            `file_path` is set.
        file_path : Optional[Path]
            If provided the data to be uploaded will be read from the file.
            Cannot be set if `data` is set.
        retry_total : Optional[int]
            Number of retries for retry-able exceptions, e.g. when the
            upload failed, or the data source is locked. If not provided
            a default value will be applied.
        backoff_factor :Optional[Union[int, float]]
            The retrying of the retry-able exceptions is done with exponential
            back-off with provided back-off factor. If not provided a default
            value will be applied.

        Returns
        -------
        Dict[str, str]
            JSON server response
        """
        self._validate_parameters(stream_name, data, file_path)
        bdata = self._prepare_data(data, file_path)
        # Get size of the data
        init_position = bdata.tell()
        size_bytes = bdata.seek(0, 2)
        bdata.seek(init_position)  # move back to init position

        method = self.upload_single
        if size_bytes > CHUNK_SIZE:
            method = self.upload_chunks

        output = method(
            stream_name=stream_name,
            data=bdata,
            retry_total=retry_total,
            backoff_factor=backoff_factor,
        )
        return output

    @session_check
    def upload_single(
        self,
        stream_name: str,
        data: Union[BytesIO, FileIO],
        retry_total: Optional[int] = None,
        backoff_factor: Optional[Union[int, float]] = None,
    ) -> Dict[str, str]:
        """Uses single upload endpoint to upload small data (max 16 MiB).

        Parameters
        ----------
        stream_name : str
            Name of the data source where to upload the data
        data : Union[BytesIO, FileIO]
            Variant data object to upload, it can be either byte-stream object,
            or file-like object
        retry_total : Optional[int]
            Number of retries for retry-able exceptions, e.g. when the
            upload failed, or the data source is locked. If not provided
            a default value will be applied.
        backoff_factor : Optional[Union[int, float]]
            The retrying of the retry-able exceptions is done with exponential
            back-off with provided back-off factor. If not provided a default
            value will be applied.

        Returns
        -------
        Dict[str, str]
            JSON server response
        """
        url = self._build_url(endpoint=f'{stream_name}/single')
        try:
            response = self._retry_4xx(
                self._session.post,
                error_codes=(
                    ErrorCodes.UPLOAD_FAILED,
                    ErrorCodes.DATASOURCE_LOCKED,
                ),
                total=retry_total,
                backoff_factor=backoff_factor,
                url=url,
                data=data,
                headers=self.headers,
                timeout=self._timeout,
            )
        finally:
            data.close()

        return response.json()

    @session_check
    def upload_chunks(
        self,
        stream_name: str,
        data: Union[BytesIO, FileIO],
        retry_total: Optional[int] = None,
        backoff_factor: Optional[Union[int, float]] = None,
    ) -> Dict[str, str]:
        """Uses data chunking to upload data chunk by chunk. This method
        should be used for uploading larger data (more than 16 MiB).

        Parameters
        ----------
        stream_name : str
            Name of the data source where to upload the data
        data : Union[BytesIO, FileIO]
            Variant data object to upload, it can be either byte-stream object,
            or file-like object
        retry_total : Optional[int]
            Number of retries for retry-able exceptions, e.g. when the
            upload failed, or the data source is locked. If not provided
            a default value will be applied.
        backoff_factor : Optional[Union[int, float]]
            The retrying of the retry-able exceptions is done with exponential
            back-off with provided back-off factor. If not provided a default
            value will be applied.

        Returns
        -------
        Dict[str, str]
            JSON server response
        """
        init_url = self._build_url(f'{stream_name}/multipart')
        response = self._retry_4xx(
            self._session.post,
            error_codes=(ErrorCodes.DATASOURCE_LOCKED,),
            total=retry_total,
            backoff_factor=backoff_factor,
            url=init_url,
            headers=self.headers,
            timeout=self._timeout,
        )

        upload_id = response.json()['upload_id']
        upload_url = self._build_url(f'multipart/{upload_id}')

        try:
            chunk = data.read(CHUNK_SIZE)
            part = 0
            while chunk:
                # send data by chunks
                params = {'part': part}
                resp = self._retry_4xx(
                    self._session.post,
                    error_codes=(ErrorCodes.UPLOAD_FAILED,),
                    white_list=(ErrorCodes.RESOURCE_ALREADY_EXISTS,),
                    total=retry_total,
                    backoff_factor=backoff_factor,
                    url=upload_url,
                    data=chunk,
                    params=params,
                    timeout=self._timeout,
                )

                chunk = data.read(CHUNK_SIZE)
                part += 1
        finally:
            data.close()

        commit_url = self._build_url(f'multipart/{upload_id}/commit')
        resp = self._retry_4xx(
            self._session.post,
            error_codes=(ErrorCodes.COMMIT_FAILED,),
            total=retry_total,
            backoff_factor=backoff_factor,
            url=commit_url,
            timeout=self._timeout,
        )

        return resp.json()

    def _validate_parameters(
        self,
        stream_name: str,
        data: Optional[Union[BytesIO, FileIO, pd.DataFrame]] = None,
        file_path: Optional[Path] = None,
    ) -> None:
        """Validates input parameters.

        Parameters
        ----------
        stream_name : str
            Name of the data source where to upload the data
        data : Optional[Union[BytesIO, FileIO, pd.DataFrame]]
            Variant data object to upload, it can be either byte-stream object,
            or file-like object, or pandas DataFrame
        file_path : Optional[Path]
            If provided the data to be uploaded will be read from the file.

        Raises
        ------
        ValueError
            When the `stream_name` is ill-formatted
        ValueError
            When both `data` and `file_path` are set
        TypeError
            When `data` is of wrong data type
        TypeError
            When `file_path` is of wrong data type
        """
        self._validate_stream_name(stream_name)

        if data is None and file_path is None:
            raise ValueError('Either "data" or "file_path" must be provided')

        if data is not None:
            if not isinstance(data, (BytesIO, FileIO, pd.DataFrame)):
                raise TypeError(
                    '"data" parameter can only be BytesIO, FileIO or'
                    ' pandas DataFrame.'
                )

        if file_path is not None:
            if not isinstance(file_path, Path):
                raise TypeError('"file_path" must be Pathlib-like object')

    @staticmethod
    def _prepare_data(
        data: Optional[Union[BytesIO, FileIO, pd.DataFrame]] = None,
        file_path: Optional[Path] = None,
    ) -> Union[BytesIO, FileIO]:
        """Converts the inputs to unified data types. If the `data` is not set
        opens the `file_path` into file-like object. If the provided
        `data` is pandas DataFrame converts it to byte-stream object.

        Parameters
        ----------
        data : Optional[Union[BytesIO, FileIO, pd.DataFrame]]
            Variant data object to upload, it can be either byte-stream object,
            or file-like object, or pandas DataFrame
        file_path : Optional[Path]
            If provided the data to be uploaded will be read from the file.

        Returns
        -------
        Union[BytesIO, FileIO]
            Either byte-stream object or file-like object
        """
        if data is None:
            data = file_path.open('rb')

        if isinstance(data, pd.DataFrame):
            data = BytesIO(data.to_csv(index=False).encode('utf-8'))
        return data
