"""A command to run the drip feed utility"""

from typing import Type

import argparse
from importlib.metadata import entry_points
import logging
import sys

import drip

_ENVARS_MAPPING = {
    "DRIP_INI_FILE": "INI_FILE",
    "DRIP_INI_SECTION": "INI_SECTION",
    "DRIP_BATCH_SIZE": "BATCH_SIZE",
    "DRIP_PAUSE_INTERVAL": "PAUSE_INTERVAL",
    "DRIP_REFILL_INTERVAL": "REFILL_INTERVAL",
    "DRIP_LOG_FILE": "LOG_FILE",
    "DRIP_LOG_LEVEL": "LOG_LEVEL",
}

_LOG_LEVELS = {
    "CRITICAL": logging.CRITICAL,
    "ERROR": logging.ERROR,
    "WARNING": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
    "NOTSET": logging.NOTSET,
}


def create_argument_parser() -> argparse.ArgumentParser:
    """
    Creates and populated the argparse.ArgumentParser for this executable.
    """
    parser = argparse.ArgumentParser(
        description="Executes an instance of a drop.Dropper clas"
    )
    parser.add_argument(
        "-i",
        "--drip_ini",
        dest="INI_FILE",
        help="The path to the configuration file for the drip.Dropper class,"
        + " the default is $HOME/"
        + drip.utils.DEFAULT_INI_FILE,
    )
    parser.add_argument(
        "-s",
        "--ini_section",
        dest="INI_SECTION",
        default="drip_feed",
        help="The section of the INI file to use for this execution,"
        + ' the default is "drip_feed"',
    )
    parser.add_argument(
        "-b",
        "--batch_size",
        dest="BATCH_SIZE",
        default="3",
        help="The number of dropped items in a drip",
    )
    parser.add_argument(
        "-p",
        "--pause_interval",
        dest="PAUSE_INTERVAL",
        default="30",
        help="The number of seconds to wait before checking the condition again",
    )
    parser.add_argument(
        "-r",
        "--refill_interval",
        dest="REFILL_INTERVAL",
        default="120",
        help="The number of seconds to wait after the source is empty before resuming",
    )
    parser.add_argument(
        "--log_file",
        dest="LOG_FILE",
        help="The file, as opposed to stdout, into which to write log messages",
    )
    parser.add_argument(
        "-l",
        "--log_level",
        default="INFO",
        dest="LOG_LEVEL",
        help="The logging level for this execution",
        choices=_LOG_LEVELS.keys(),
    )
    parser.add_argument(
        dest="POSITIONAL",
        nargs=1,
        help="The package:Class defining to drip:Dropper subclass to execute",
    )
    return parser


def select_dropper_class(name) -> Type[drip.Dropper]:
    """
    Returns the selected drop.Dropper class object.
    """
    droppers = entry_points(group="drip.dropper")
    for entry in droppers:
        if name == entry.value:
            return entry.load()
    raise ValueError(f'No know Dropper implementation names "{name}"')


def main() -> None:
    """
    Main routine that executes an instance of a drop.Dropper class.
    """
    parser = create_argument_parser()
    envar_values = drip.utils.read_envar_values(_ENVARS_MAPPING)
    options = parser.parse_args(namespace=envar_values)

    if None is options.LOG_FILE:
        logging.basicConfig(stream=sys.stdout, level=_LOG_LEVELS[options.LOG_LEVEL])
    else:
        logging.basicConfig(
            filename=options.LOG_FILE, level=_LOG_LEVELS[options.LOG_LEVEL]
        )

    logging.debug("Begin options:")
    for option in options.__dict__:
        if options.__dict__[option] is not None:
            logging.debug("    %s = %s", option, options.__dict__[option])
    logging.debug("End options:")
    dropper_class = select_dropper_class(options.POSITIONAL[0])
    ini_file = drip.utils.find_config(options.INI_FILE)
    dropper = dropper_class(ini_file, options.INI_SECTION)
    feeder = drip.Feeder(
        dropper,
        batch_size=int(options.BATCH_SIZE),
        pause_interval=int(options.PAUSE_INTERVAL),
        refill_interval=int(options.REFILL_INTERVAL),
    )

    feeder.run()


if __name__ == "__main__":
    main()
