from abc import abstractmethod
from typing import Dict, Union


class AudioExtensionHandler:
    @abstractmethod
    def get_tag(self, tag_key) -> Union[str, bin]:
        """return the value of the tag"""

    @abstractmethod
    def set_tag(self, tag_key: str, tag_value: Union[str, bin]) -> None:
        """modify the value of the tag in the audio file"""

    @abstractmethod
    def save_modifications(self) -> None:
        """save all previous modification made by the user"""

    @abstractmethod
    def check_tag_existence(self, key: str) -> bool:
        """return True if the tag exists, False otherwise"""

    @abstractmethod
    def get_tags(self) -> Dict:
        """return a dictionary containg the value of each tag"""
