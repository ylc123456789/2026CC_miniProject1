import os


APP_MODE_LOCAL = "local"
APP_MODE_CLOUD = "cloud"


TRUE_VALUES = {"1", "true", "yes", "on"}


def get_env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in TRUE_VALUES


def get_env_float(name: str, default: float) -> float:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return float(value)
    except ValueError:
        return default


def get_app_mode() -> str:
    mode = os.getenv("APP_MODE", APP_MODE_LOCAL).strip().lower()
    if mode == APP_MODE_CLOUD:
        return APP_MODE_CLOUD
    return APP_MODE_LOCAL


def is_cloud_mode() -> bool:
    return get_app_mode() == APP_MODE_CLOUD


def get_data_service_url() -> str:
    return os.getenv("DATA_SERVICE_URL", "http://localhost:8002").rstrip("/")


def get_workflow_service_url() -> str:
    return os.getenv("WORKFLOW_SERVICE_URL", "http://localhost:8001").rstrip("/")


def get_submission_event_function_url() -> str:
    return os.getenv("SUBMISSION_EVENT_FUNCTION_URL", "http://localhost:9001/invoke").rstrip("/")


def get_processing_function_url() -> str:
    return os.getenv("PROCESSING_FUNCTION_URL", "http://localhost:9002/invoke").rstrip("/")


def get_result_update_function_url() -> str:
    return os.getenv("RESULT_UPDATE_FUNCTION_URL", "http://localhost:9003/invoke").rstrip("/")


def get_function_auth_token() -> str:
    return os.getenv("FUNCTION_AUTH_TOKEN", "").strip()


def get_request_timeout() -> float:
    return get_env_float("REQUEST_TIMEOUT_SECONDS", 15.0)


def get_result_refresh_seconds() -> int:
    value = os.getenv("RESULT_REFRESH_SECONDS", "2").strip()
    try:
        parsed = int(value)
        return max(parsed, 1)
    except ValueError:
        return 2


def get_function_headers() -> dict[str, str]:
    headers = {"Content-Type": "application/json"}
    token = get_function_auth_token()
    if token:
        headers["X-Function-Token"] = token
    return headers
