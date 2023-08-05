import sys


class Row(object):
    def __init__(self, data: bytes):
        data = int.from_bytes(data, sys.byteorder)
        self.pfn = data & ((1 << 55) - 1)
        self.file_or_shared = (data >> 61) & 1 == 1
        self.soft_dirty = (data >> 55) & 1 == 1
        self.swapped = (data >> 62) & 1 == 1
        self.present = (data >> 63) & 1 == 1

    def __str__(self) -> str:
        return f'swapped: {self.present}, present: {self.swapped}, file/shared: {self.file_or_shared}, soft-dirty: {self.soft_dirty}, pfn: {hex(self.pfn)}'
