"""Define the Feeder class"""

from typing import Any, Callable, List, TypeAlias, Union
from types import FrameType

import logging
from pathlib import Path
from signal import Handlers
import signal
from threading import Event
import time

from drip import Dropper

_SigHandler: TypeAlias = Union[
    Callable[[int, FrameType | None], Any], int, Handlers, None
]
Paths = list[Path]


class Feeder:
    """
    This class manages the drip feeding of a collection of items, where
    "drip feeding" means that when a specified condition is met an
    action is taken on a batch of those items that are then removed from
    that list. While executing the collection new items name be added to
    the collection.
    """

    PAUSE_INTERVAL_DEFAULT: int = 30
    REFILL_INTERVAL_DEFAULT: int = 120

    def __init__(
        self,
        dropper: Dropper,
        pause_interval: int = PAUSE_INTERVAL_DEFAULT,
        refill_interval: int = REFILL_INTERVAL_DEFAULT,
    ):
        """
        Creates an instance of this class.

        :param dropper_class: the class that will feed the drops while dripping.
        :param pause_interval: the number of seconds to wait before checking the condition again.
        :param refill_interval: the number of seconds to wait after the source is
                                empty before resuming.
        """

        # Create instance of function implementing the feeding mechanism
        self.__dropper = dropper
        self.__batch_size = 2
        self.__cache: List[Any] = []
        self.__pause_interval = pause_interval
        self.__refill_interval = refill_interval
        self.__running = Event()
        self.__previous_sigint: _SigHandler = None

    def drip(self) -> int:
        """
        Runs a single "drip", i.e moves one batch of files from source
        to destination when a specified condition is met.
        """

        cache_size = len(self.__cache)
        if cache_size < self.__batch_size:
            self.__cache = self.__dropper.fill_cache()
            cache_size = len(self.__cache)
        if 0 == cache_size:
            logging.info(
                "Source of items is empty, waiting for %i seconds",
                self.__refill_interval,
            )
            self.__running.wait(self.__refill_interval)
            return 0

        if 1 == cache_size:
            to_be = "is"
            plural = ""
        else:
            to_be = "are"
            plural = "s"
        logging.info(
            "There %s at least %i item%s waiting to be fed.", to_be, cache_size, plural
        )
        (available, condition) = self.__dropper.assess_condition()
        if 0 == available:
            logging.info(
                "Waiting %i seconds for %s",
                self.__pause_interval,
                condition + " before feeding more items",
            )
            self.__running.wait(self.__pause_interval)
            return 0
        end = min(available, self.__batch_size, cache_size)
        count = 0
        t_0 = time.time()
        for path in self.__cache[0:end]:
            self.__dropper.drop(path)
            count = count + 1
        t_1 = time.time()
        self.__cache = self.__cache[count:]
        if 1 == count:
            plural = ""
        else:
            plural = "s"
        logging.info(
            "Finished moving item%s %i to the destination in %i seconds",
            plural,
            count,
            int(t_1 - t_0 + 0.5),
        )
        return count

    def run(self) -> None:
        """
        Runs a loop to execute the drop-feeding.
        """
        self.__running.clear()
        self.__previous_sigint = signal.signal(signal.SIGINT, self._stop)
        while not self.__running.is_set():
            self.drip()

    def _stop(
        self,
        signum,  # pylint: disable=unused-argument
        frame,  # pylint: disable=unused-argument
    ) -> None:
        self.stop()

    def stop(self) -> None:
        """
        Signals that the drip-feeding loop should exit.
        """
        self.__running.set()
        if None is not self.__previous_sigint:
            signal.signal(signal.SIGINT, self.__previous_sigint)
