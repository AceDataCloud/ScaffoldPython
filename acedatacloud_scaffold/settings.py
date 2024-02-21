import environs

env = environs.Env()
env.read_env()

HTTP_HOST = env.str('HTTP_HOST', '0.0.0.0')
HTTP_PORT = env.int('HTTP_PORT', 8000)

DEFAULT_TIMEOUT_FORWARD = env.int('DEFAULT_TIMEOUT_FORWARD', 60)

RECORD_SERVER_URL = env.str(
    'RECORD_SERVER_URL', 'http://platform-gateway:8000/record')

# error status
ERROR_STATUS_API_ERROR = 500
ERROR_STATUS_UNKNOWN = 500
ERROR_STATUS_CONNECTION_RESET = 499
ERROR_STATUS_NOT_FOUND = 404

# error code
ERROR_CODE_API_ERROR = 'api_error'
ERROR_CODE_UNKNOWN = 'unknown'
ERROR_CODE_CONNECTION_RESET = 'connection_reset'
ERROR_CODE_NOT_FOUND = 'not_found'

# error detail
ERROR_DETAIL_API_ERROR = 'api internal error, please contact admin'
ERROR_DETAIL_UNKNOWN = 'unknown internal server error, please contact admin'
ERROR_DETAIL_CONNECTION_RESET = 'connection reset error, this usually caused by client closed connection'
ERROR_DETAIL_NOT_FOUND = 'not found'
