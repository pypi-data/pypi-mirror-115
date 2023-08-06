"""
Operating system utilities.
"""

import platform


def operating_system():
    """
    :return: Operating system of host machine.
    """
    return platform.system().lower()
