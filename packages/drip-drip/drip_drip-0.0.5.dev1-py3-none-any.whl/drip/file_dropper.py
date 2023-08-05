"""Define the FileDropper class"""

from typing import List, Tuple

import os
from pathlib import Path
import shutil

from drip import Dropper

Paths = list[Path]


class FileDropper(Dropper):
    """
    This class provides the concrete implementation use by a Feeder
    instance to copy files from one directory to another.
    """

    def __init__(self, source: Path, destination: Path, threshold: int):
        """
        Creates an instance of this class.

        :param source: the Path to the source directory
        :param destination: the Path to the destination directory
        :param threshold: the maximum number of files allowed in the destination directory.
        """
        # Check the source directory exists
        if not source.exists():
            raise ValueError(f"{source.resolve()} does not exist!")
        self.__src: Path = source

        # Check the source directory exists
        if not destination.exists():
            raise ValueError(f"{destination.resolve()} does not exist!")
        self.__dst: Path = destination

        self.__threshold = threshold

    def assess_condition(self) -> Tuple[int, str]:
        """
        Assess whether a drip should be executed or not.

        :return maximum number if items that can be dropped and
        explanation of any limitations.
        """
        count = len(os.listdir(self.__dst))
        if 1 == count:
            multiple = ""
            plural = ""
        else:
            multiple = "some of "
            plural = "s"
        if count >= self.__threshold:
            return (
                0,
                f"{multiple}the {count} file{plural} in the target directory to be handled",
            )
        return self.__threshold - count, ""

    def drop(self, item) -> None:
        """
        "Drops" the supplied item, i.e. acts on that item.
        """
        shutil.move(item, self.__dst)

    def fill_cache(self) -> List[Path]:
        """
        Fills internal list of files to be moved.
        """
        result = []
        for file in os.listdir(self.__src):
            result.append(self.__src.joinpath(file))
        result.sort(key=os.path.getmtime)
        return result
