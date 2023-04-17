import json

import requests


HTTP_EXCEPTIONS = (
    requests.exceptions.JSONDecodeError,
    requests.exceptions.ProxyError,
    requests.exceptions.ConnectionError,
    json.decoder.JSONDecodeError,
    requests.exceptions.ReadTimeout,
    requests.exceptions.SSLError,
    requests.exceptions.RequestException,
)
