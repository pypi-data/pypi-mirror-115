import builtins
import hashlib
import os
from functools import partial

from breakword import (
    WordGroup,
    breakpoint as _breakpoint,
    common_words as cw,
    common_words_source,
    file_source,
)


def pytest_addoption(parser, pluginmanager):
    parser.addoption(
        "--bw",
        "--breakword",
        help="Breakword to use",
        default=None,
    )


def pytest_sessionstart(session):
    bw = session.config.option.bw
    if bw is not None:
        os.environ["BREAKWORD"] = bw


def pytest_runtest_setup(item):
    loc = item.location
    hsh = hashlib.md5(str((loc[0], loc[2])).encode())
    hsh = int(hsh.hexdigest(), 16)
    grp_name = cw[hsh % len(cw)]
    grp = WordGroup(
        name=grp_name,
        sources=[
            common_words_source,
            file_source("/usr/share/dict/words", exclude=cw),
        ],
    )
    builtins.breakpoint = partial(_breakpoint, group=grp)
