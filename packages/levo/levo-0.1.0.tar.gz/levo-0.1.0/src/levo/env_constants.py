import os
from pathlib import Path

ROOT_DIR = Path(__file__).parent.absolute()
CONFIG_FILE = str(Path.home()) + "/.config/configstore/levo.json"
DAF_CLIENT_ID = os.getenv("LEVO_DAF_CLIENT_ID", "aa9hJp2bddyhZeEXjAsura6bWIdSEr5s")
BASE_URL = os.getenv("LEVO_BASE_URL", "https://api.dev.levo.ai")
DAF_DOMAIN = os.getenv("LEVO_DAF_DOMAIN", "https://levoai.us.auth0.com")
DAF_GRANT_TYPE = os.getenv(
    "LEVO_DAF_GREANT_TYPE", "urn:ietf:params:oauth:grant-type:device_code"
)
DAF_AUDIENCE = os.getenv("LEVO_DAF_AUDIENCE", "https://api.levo.ai")
DAF_SCOPES = os.getenv("LEVO_DAF_SCOPES", "email offline_access openid")

######################################################################################
# Docker related items
HOST_SCHEMA_DIR = os.getenv("HOST_SCHEMA_DIR", "")  # This is an ENV passed to docker
LOCAL_SCHEMA_DIR = "/home/levo/schemas"
LEVO_CONFIG_DIR = "/home/levo/.config/configstore"
######################################################################################
