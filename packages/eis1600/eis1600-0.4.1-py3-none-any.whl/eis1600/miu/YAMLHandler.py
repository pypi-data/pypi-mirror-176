from typing import Type

from eis1600.markdown.re_patterns import MIU_HEADER
from eis1600.miu.HeadingTracker import HeadingTracker


class YAMLHandler:
    """A class to take care of the MIU YAML Headers

    :param bool reviewed: Indicating if this record has been manually reviewed. If True, the record will not be
    changed by automated analysis, defaults to False.
    :ivar Typing[HeadingTracker] headings: HeadingTracker returned by the get_curr_state method of the HeaderTracker
    """

    def __init__(self, reviewed: bool = False) -> None:
        self.reviewed = reviewed
        self.headings = None

    def set_headings(self, headings: Type[HeadingTracker]):
        self.headings = headings

    def get_yamlfied(self) -> str:
        yaml_str = MIU_HEADER + '\n\n'
        for key, val in vars(self).items():
            yaml_str += key + '    : ' + str(val) + '\n'
        yaml_str += '\n' + MIU_HEADER + '\n\n'

        return yaml_str

    def __repr__(self) -> str:
        return str(self.__dict__)

    def __str__(self) -> str:
        return self.get_yamlfied()
