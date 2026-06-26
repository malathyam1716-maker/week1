import requests


def is_retryable_exception(exception):
    if isinstance(exception, requests.exceptions.HTTPError):
        if exception.response is not None:
            status_code = exception.response.status_code
            if status_code == 429 or status_code >= 500:
                return True
            if 400 <= status_code < 500:
                return False
    if isinstance(exception, (requests.exceptions.ConnectionError, requests.exceptions.Timeout)):
        return True
    if isinstance(exception, requests.exceptions.RequestException):
        return False
    return False
