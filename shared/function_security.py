from fastapi import HTTPException, Request

from shared.config import get_function_auth_token


FUNCTION_AUTH_HEADER = "x-function-token"


def verify_function_request(request: Request) -> None:
    expected_token = get_function_auth_token()
    if not expected_token:
        return

    received_token = request.headers.get(FUNCTION_AUTH_HEADER, "")
    if received_token != expected_token:
        raise HTTPException(status_code=401, detail="Unauthorized function invocation")
