import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Text

import coloredlogs

from neuralspace.apis import get_async_http_session
from neuralspace.constants import COMMON_HEADERS, LOGIN_URL, auth_path, neuralspace_url

logger = logging.getLogger(__name__)


def setup_logger(log_level: Text):
    logging.basicConfig(level=log_level)
    coloredlogs.install(level=log_level)


def print_logo():
    logo_path = (Path(os.path.realpath(__file__))).parent / "data" / "logo.txt"
    logger.info(f"\n{logo_path.read_text()}")


def register_auth_token(login_response: Dict[Text, Text]):
    if "data" in login_response and "auth" in login_response["data"]:
        with open(str(auth_path()), "w") as f:
            json.dump(login_response, f)
    else:
        raise ValueError(f"Login response is malformed: {login_response}")


def get_auth_token() -> Text:
    if auth_path().exists():
        credentials = json.loads(auth_path().read_text())
        return credentials["data"]["auth"]
    else:
        raise FileNotFoundError(
            "Credentials file not found. Consider logging in using."
            " Seems like you have not logged in. "
            "`neuralspace login --email <your-neuralspace-email-id> "
            "--password <your-password>`"
        )


def is_success_status(status_code: int) -> bool:
    success = False
    if 200 <= status_code < 300:
        success = True
    return success


async def do_login(email: Text, password: Text):
    user_data = {"email": email, "password": password}
    logger.debug(f"Login attempt for: {user_data}")
    async with get_async_http_session().post(
        url=f"{neuralspace_url()}/{LOGIN_URL}",
        data=json.dumps(user_data),
        headers=COMMON_HEADERS,
    ) as response:
        json_response = await response.json(encoding="utf-8")
        logger.debug(f"Platform Response: {json_response}")
        if is_success_status(response.status):
            register_auth_token(json_response)
            logger.info("Login successful!")
            logger.debug(f"Credentials registered at {auth_path()}")
            logger.info(f"Credentials: \n {json.dumps(json_response, indent=4)}")
        else:
            logger.error("Login failed! Please check your username and password")


def get_list_chunks(items: List[Any], chunk_size: int):
    for chunk in range(0, len(items), chunk_size):
        yield items[chunk : chunk + chunk_size]  # noqa : E203
