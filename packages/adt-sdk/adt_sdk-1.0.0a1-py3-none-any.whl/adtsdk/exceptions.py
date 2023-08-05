from enum import Enum


class ErrorCodes(Enum):
    """
    Custom error codes to provide together with status_code so that it is
    easier for client to distinguish two different events with the same
    status_code.
    """

    UPLOAD_EXPIRED = 40000
    BAD_PART_NUMBER = 40001
    INVALID_QUERY_PARAMETER = 40002
    UNAUTHORIZED = 40100
    TOKEN_EXPIRED = 40101
    UPLOAD_COMMITTED = 40300
    STREAM_NAME_ILL_FORMATTED = 40301
    DATASOURCE_LOCKED = 40302
    DATASOURCE_IN_USE = 40303
    TOO_MANY_DATASOURCES = 40304
    INVALID_UPLOAD_ENDPOINT = 40400
    STREAM_DOES_NOT_EXIST = 40401
    UPLOAD_DOES_NOT_EXIST = 40402
    RESOURCE_ALREADY_EXISTS = 40900
    PAYLOAD_TOO_LARGE = 41300
    UPLOAD_FAILED = 42400
    COMMIT_FAILED = 42401


class ClientNotInitialized(Exception):
    """When the client is not initialized correctly - calling its method
    without context manager.
    """


class BaseServerError(Exception):
    """Exception when the server either does not return `error_code` in the
    message response or it is unknown value.
    """

    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.status_code}: {self.message}'


class InternalServerError(BaseServerError):
    """Exception when the server either does not return `error_code` in the
    message response or it is unknown value, or the status_code is 5xx.
    """


class DataSourceNotCreated(BaseServerError):
    """When the datasource could not be created"""


class DataSourceNotDeleted(BaseServerError):
    """When the datasource could not be deleted"""


class UploadBaseException(Exception):
    """Base Upload Exception"""

    ERROR_CODE = None

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return f'{self.ERROR_CODE.value}: {self.message}'


class UploadExpired(UploadBaseException):
    """Raise when upload is expired"""

    ERROR_CODE = ErrorCodes.UPLOAD_EXPIRED


class BadPartNumber(UploadBaseException):
    """Raise when chunk part number is invalid"""

    ERROR_CODE = ErrorCodes.BAD_PART_NUMBER


class InvalidQueryParameter(UploadBaseException):
    """Raise when the query parameter is invalid"""

    ERROR_CODE = ErrorCodes.INVALID_QUERY_PARAMETER


class UploadCommitted(UploadBaseException):
    """Raise when the upload has already been committed"""

    ERROR_CODE = ErrorCodes.UPLOAD_COMMITTED


class StreamNameIllFormatted(UploadBaseException):
    """Raise when the stream name is ill-formatted"""

    ERROR_CODE = ErrorCodes.STREAM_NAME_ILL_FORMATTED


class StreamLocked(UploadBaseException):
    """Raise when the stream/datasource is locked"""

    ERROR_CODE = ErrorCodes.DATASOURCE_LOCKED


class ResourceAlreadyExists(UploadBaseException):
    """Raise when the resource already exist"""

    ERROR_CODE = ErrorCodes.RESOURCE_ALREADY_EXISTS


class DataSourceInUse(UploadBaseException):
    """Raise when data source has at least one ADT pipeline running"""

    ERROR_CODE = ErrorCodes.DATASOURCE_IN_USE


class TooManyDataSources(UploadBaseException):
    """Raise when three are too many data sources for the user's ADT tier"""

    ERROR_CODE = ErrorCodes.TOO_MANY_DATASOURCES


class UploadDoesNotExist(UploadBaseException):
    """Raise when the upload identifier does not exist"""

    ERROR_CODE = ErrorCodes.UPLOAD_DOES_NOT_EXIST


class Unauthorized(UploadBaseException):
    """Raise when the request is unauthorized"""

    ERROR_CODE = ErrorCodes.UNAUTHORIZED


class TokenExpired(UploadBaseException):
    """Raise when the authentication JWT is expired"""

    ERROR_CODE = ErrorCodes.TOKEN_EXPIRED


class InvalidUploadId(UploadBaseException):
    """Raise when the upload_id is invalid"""

    ERROR_CODE = ErrorCodes.INVALID_UPLOAD_ENDPOINT


class StreamDoesNotExist(UploadBaseException):
    """Raise when the stream/datasource does not exist"""

    ERROR_CODE = ErrorCodes.STREAM_DOES_NOT_EXIST


class PayloadTooLarge(UploadBaseException):
    """Raise when the payload is too large"""

    ERROR_CODE = ErrorCodes.PAYLOAD_TOO_LARGE


class UploadFailed(UploadBaseException):
    """Raise when the upload failed"""

    ERROR_CODE = ErrorCodes.UPLOAD_FAILED


class CommitFailed(UploadBaseException):
    """Raise when the upload commit failed"""

    ERROR_CODE = ErrorCodes.COMMIT_FAILED


ERROR_TO_EXCEPTION = {
    ErrorCodes.UPLOAD_EXPIRED: UploadExpired,
    ErrorCodes.BAD_PART_NUMBER: BadPartNumber,
    ErrorCodes.INVALID_QUERY_PARAMETER: InvalidQueryParameter,
    ErrorCodes.UNAUTHORIZED: Unauthorized,
    ErrorCodes.TOKEN_EXPIRED: TokenExpired,
    ErrorCodes.UPLOAD_COMMITTED: UploadCommitted,
    ErrorCodes.STREAM_NAME_ILL_FORMATTED: StreamNameIllFormatted,
    ErrorCodes.DATASOURCE_LOCKED: StreamLocked,
    ErrorCodes.DATASOURCE_IN_USE: DataSourceInUse,
    ErrorCodes.RESOURCE_ALREADY_EXISTS: ResourceAlreadyExists,
    ErrorCodes.TOO_MANY_DATASOURCES: TooManyDataSources,
    ErrorCodes.INVALID_UPLOAD_ENDPOINT: InvalidUploadId,
    ErrorCodes.STREAM_DOES_NOT_EXIST: StreamDoesNotExist,
    ErrorCodes.UPLOAD_DOES_NOT_EXIST: UploadDoesNotExist,
    ErrorCodes.PAYLOAD_TOO_LARGE: PayloadTooLarge,
    ErrorCodes.UPLOAD_FAILED: UploadFailed,
    ErrorCodes.COMMIT_FAILED: CommitFailed,
}
