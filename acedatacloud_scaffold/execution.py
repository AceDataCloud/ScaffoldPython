EXECUTION_OWNER_HEADER = 'X-Ace-Execution-Owner'
X402_EXECUTION_OWNER = 'x402'


def get_execution_owner(headers):
    if headers is None:
        return None
    value = next(
        (value for key, value in headers.items() if str(key).lower() == EXECUTION_OWNER_HEADER.lower()),
        None,
    )
    if not isinstance(value, str):
        return None
    owner = value.strip().lower()
    return owner or None


def is_execute_only(headers):
    return get_execution_owner(headers) == X402_EXECUTION_OWNER