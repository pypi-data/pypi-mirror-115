import re
from typing import Dict, Type, Union
from opentrons.drivers.smoothie_drivers.driver_3_0 import GCODE as SMOOTHIE_G_CODE
from opentrons.drivers.mag_deck.driver import GCODE as MAGDECK_G_CODE
from opentrons.drivers.temp_deck.driver import GCODE as TEMPDECK_G_CODE


WRITE_REGEX = re.compile(r"(.*?) \| (.*?) \|(.*?)$")


def reverse_enum(
        enum_to_reverse: Union[
            Type[SMOOTHIE_G_CODE], Type[MAGDECK_G_CODE], Type[TEMPDECK_G_CODE]
        ]
) -> Dict:
    """
    Returns dictionary with keys and values switched from passed Enum
    :param enum_to_reverse: The Enum that you want to reverse
    :return: Reversed dictionary
    """
    # I don't know what is going on with mypy, it is complaining
    # about keys not existing as an attribute. I am not calling it
    # as an attribute. I am calling it as a function.
    members = enum_to_reverse.__members__.keys()
    values = [
        enum_to_reverse[member]
        for member in members
    ]
    return dict(zip(values, members))
