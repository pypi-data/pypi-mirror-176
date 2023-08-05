import os
from .constant import *


def check_pid(pid):
    """ check for the existence of a unix pid. """
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True


def get_offest(virtual_address: int) -> int:
    return virtual_address // PAGE_SIZE * ROW_SIZE


def virtual_to_physical(virtual_address: int, pfn: int) -> int:
    page_offset = virtual_address % PAGE_SIZE
    return pfn * PAGE_SIZE + page_offset
