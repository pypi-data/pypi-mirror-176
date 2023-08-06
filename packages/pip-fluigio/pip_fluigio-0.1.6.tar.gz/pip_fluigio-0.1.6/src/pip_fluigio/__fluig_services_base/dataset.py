from abc import ABC
from typing import List


class DatasetProvider(ABC):
    def __init__(self):
        pass

    """
    Decription:  

    Returns:

    Args:

    Raises:
   
    """

    def get_dataset(self) -> List[dict]:

        """ """

        return list()

    def disable_dataset(self) -> None:

        """ """

        return

    def get_available_datasets(self) -> List[dict]:

        """ """

        return list()

    def get_all_available_dataset(self) -> List[dict]:

        """ """

        return list()
