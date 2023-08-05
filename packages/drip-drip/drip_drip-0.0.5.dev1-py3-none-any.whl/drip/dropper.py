"""Define the Dropper class"""

from typing import Any, List, Tuple


class Dropper:
    """
    This class provides the concrete implementation use by a Feeder
    instance to execute a particular type of drip-feed.
    """

    def __init__(self):
        """
        Creates an instance of this class.
        """

    def assess_condition(self) -> Tuple[int, str]:
        """
        Test to see in a drip should be executed.

        :return true if the condition has been met.
        """
        return (0, "")

    def drop(self, item: Any) -> None:
        """
        "Drops" the supplied item, i.e. acts on that item.
        """

    def fill_cache(self) -> List[Any]:
        """
        Fills internal list of files to be moved.
        """
