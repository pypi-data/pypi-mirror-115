"""Example cli using click."""
from distutils.util import strtobool
import sys
import click
from .config import load
from .diffsync.cvutils import connect_cv, disconnect_cv
from .diffsync.nbutils import connect_nb
from .diffsync.cloudvision import CloudVision
from .diffsync.nautobot import Nautobot


def is_truthy(arg):
    """Convert "truthy" strings into Booleans.

    Examples:
        >>> is_truthy('yes')
        True

    Args:
        arg (str): Truthy string (True values are y, yes, t, true, on and 1; false values are n, no,
        f, false, off and 0. Raises ValueError if val is anything else.
    """
    if isinstance(arg, bool):
        return arg
    return bool(strtobool(arg))


@click.command()
# @click.option("--nautobot_server", default="127.0.0.1:8000", help="IP or hostname of Nautobot instance.")
# @click.option("--cloudvision_server", default="www.arista.io:443", help="IP or hostname of Cloudvision instance.")
# @click.option("--cvaas_token_file")
def main():
    """Sync user tags from Cloudvision to Nautobot."""
    settings = load().dict()

    # Load Cloudvision user tags
    print("Connecting to Cloudvision.")
    connect_cv(settings)
    cv_connection = CloudVision()
    cv_connection.load()

    # Load Nautobot tags
    print("Connecting to Nautobot.")
    connect_nb(settings["nautobot_url"], settings["nautobot_token"])
    nb_connection = Nautobot()
    nb_connection.load()

    print("Performing diff between Nautobot and Cloudvision.")
    diff = nb_connection.diff_from(cv_connection)
    print(diff.summary())
    proceed = input("Would you like to continue with the user tag sync? (yes/no)")
    if is_truthy(proceed):
        nb_connection.sync_from(cv_connection)
    else:
        print("Exiting command line tool.")
        sys.exit()

    print("Disconnecting from Cloudvision.")
    disconnect_cv()
