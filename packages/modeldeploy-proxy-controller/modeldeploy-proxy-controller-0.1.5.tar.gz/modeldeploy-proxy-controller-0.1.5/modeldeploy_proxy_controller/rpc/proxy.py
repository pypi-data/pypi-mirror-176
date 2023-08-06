import os
import requests

API_HOST_URL = os.environ.get("API_HOST_URL", "")
API_VERSION = os.environ.get("API_VERSION", "v1")
PROXY_API_PREFIX = "{}/api/{}/".format(API_HOST_URL, API_VERSION)
TRANSFORMER_UPLOAD_URL = "{}/transformer/upload".format(PROXY_API_PREFIX)
REQUIREMENTS_UPLOAD_URL = "{}/requirements/upload".format(PROXY_API_PREFIX)
STATUS_URL = "{}/proxy/health/status".format(PROXY_API_PREFIX)

def probe(request):
    request.log.debug("probe_proxy")
    global API_HOST_URL
    global API_VERSION
    global PROXY_API_PREFIX
    global TRANSFORMER_UPLOAD_URL
    global REQUIREMENTS_UPLOAD_URL
    global STATUS_URL
    if not API_HOST_URL:
        try:
            cwd = os.getcwd()
            proxy_url = "{}/.proxy".format(cwd)
            with open(proxy_url) as f:
                API_HOST_URL = f.readline()
                PROXY_API_PREFIX = "{}/api/{}/".format(API_HOST_URL, API_VERSION)
                TRANSFORMER_UPLOAD_URL = "{}/transformer/upload".format(PROXY_API_PREFIX)
                REQUIREMENTS_UPLOAD_URL = "{}/requirements/upload".format(PROXY_API_PREFIX)
                STATUS_URL = "{}/proxy/health/status".format(PROXY_API_PREFIX)
        except Exception as e:
            request.log.warn(str(e))
            return

    response = requests.get(STATUS_URL)
    request.log.debug(str(response))
