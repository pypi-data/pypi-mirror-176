import click
import os
from . import __version__
from .hexint import HexInt
from .utils import check_pid, get_offest, virtual_to_physical
from .constant import *
from .row import Row


# Convert virtual memory address to physical memory address
@click.command()
@click.option(
    "--pid", "-p", type=int, default=os.getpid(), help="the process id to convert"
)
@click.option(
    "--virtual_address",
    "-v",
    type=HexInt(),
    required=True,
    help="the virtual address to convert",
)
def convert(pid: int, virtual_address: int):
    print(f"pid = {pid}, va = {hex(virtual_address)}")
    assert check_pid(pid), f"process {pid} is not exists."

    offset = get_offest(virtual_address)
    with open(f"/proc/{pid}/pagemap", "rb") as f:
        f.seek(offset)
        row = Row(f.read(ROW_SIZE))
        print(row)
        if not row.present:
            print(f"{hex(virtual_address)} is not present.")
            return
        physical_address = virtual_to_physical(virtual_address, row.pfn)
        print(f"{hex(virtual_address)} -> {hex(physical_address)}")
        f.close()


# Count the actual number of virtual memory pages currently occupied by the process,
# the number of physical memory pages, and the number of virtual memory pages that
# have been swapped to external memory.
@click.command()
@click.option(
    "--pid", "-p", type=int, default=os.getpid(), help="the process id to convert"
)
def show(pid: int):
    virtual_page_cnt = 0
    physical_page_cnt = 0
    swapped_cnt = 0
    print(f"pid = {pid}")
    with open(f"/proc/{pid}/maps", "r") as maps:
        with open(f"/proc/{pid}/pagemap", "rb") as pagemap:
            for line in maps.readlines():
                begin, end = map(lambda x: int(x, 16),
                                 (line.split()[0]).split("-"))
                for offset in map(get_offest, range(begin, end, PAGE_SIZE)):
                    pagemap.seek(offset, 0)
                    virtual_page_cnt += 1
                    row = Row(pagemap.read(ROW_SIZE))
                    if row.present:
                        physical_page_cnt += 1
                    if row.swapped:
                        swapped_cnt += 1
            pagemap.close()
        maps.close()
    print(
        f"virtual pages: {virtual_page_cnt}, physical pages: {physical_page_cnt}, swapped pages: {swapped_cnt}"
    )


@click.version_option(__version__)
@click.group()
def run():
    pass


run.add_command(convert)
run.add_command(show)


def main():
    run()
