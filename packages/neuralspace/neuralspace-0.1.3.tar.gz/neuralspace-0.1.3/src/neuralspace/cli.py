import asyncio
import atexit
import logging
from typing import Text

import click

from neuralspace.apis import get_async_http_session
from neuralspace.nlu.commands import nlu
from neuralspace.utils import do_login, print_logo, setup_logger

logger = logging.getLogger(__name__)


def close_connection():
    loop = asyncio.new_event_loop()
    loop.run_until_complete(get_async_http_session().close())


atexit.register(close_connection)


@click.group()
def entrypoint():
    pass


@entrypoint.command(name="login")
@click.option(
    "-e",
    "--email",
    type=click.STRING,
    required=True,
    help="Your NeuralSpace email id",
)
@click.option(
    "-p",
    "--password",
    type=click.STRING,
    required=True,
    help="Your NeuralSpace account password",
)
@click.option(
    "-l", "--log-level", type=click.Choice(["INFO", "DEBUG", "ERROR"]), default="INFO"
)
def login(email: Text, password: Text, log_level: Text):
    setup_logger(log_level=log_level)
    print_logo()
    loop = asyncio.new_event_loop()
    loop.run_until_complete(do_login(email, password))
    loop.run_until_complete(get_async_http_session().close())


entrypoint.add_command(nlu)


if __name__ == "__main__":
    entrypoint()
