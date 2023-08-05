# Version of the ADT Upload API
API_VERSION = 'api/v1'

# Size of a chunk in bytes. If the data for upload is larger than the size
# the data will be send in chunks with this size.
CHUNK_SIZE = 16 * 2**20  # 16 MiB
