from __future__ import annotations

import os
import types
from importlib import import_module
from typing import Any, Dict, List, TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from typing_extensions import Protocol

    class FrameFilter(Protocol):
        def __call__(self, frame: types.FrameType, event: str, arg: object) -> bool:
            pass

    ProtoFrameFilter = str | FrameFilter | Dict[str, str]

    class FrameProcessor(Protocol):
        config: Dict[str, Any]
        co_names: Tuple[str, ...]

        def __call__(self, frame: types.FrameType, event: str, arg: object) -> bool:
            pass

        def process(
            self,
            frame: types.FrameType,
            event: str,
            arg: object,
            call_frame_ids: List[Dict[str, str]],
        ) -> Dict[str, Any]:
            pass


class HasPath:
    def __init__(self, path: str):
        self.path = path

    def __call__(self, frame: types.FrameType, event: str, arg: object) -> bool:
        return self.path in frame.f_code.co_filename

    def __repr__(self):
        return f'HasPath("{self.path}")'

    def __eq__(self, other):
        return self.path == other.path


def build_frame_filter(filter: "ProtoFrameFilter") -> "FrameFilter":
    if isinstance(filter, str):
        return HasPath(filter)
    if isinstance(filter, dict):
        filter_path = filter["callable"]
        module_path, _sep, filter_name = filter_path.rpartition(".")
        module = import_module(module_path)
        return getattr(module, filter_name)
    return filter


def exec_filter(frame: types.FrameType, event: str, arg: object) -> bool:
    """
    Ignore a frame running a string executed using exec

    We can't show especially interesting information about it, so we skip it.

    A namedtuple is a common example of this case.
    """
    return frame.f_code.co_filename == "<string>"


def frozen_filter(frame: types.FrameType, event: str, arg: object) -> bool:
    """
    Ignore all frozen modules

    Frozen modules are compiled into the interpreter, so are almost
    always part of the standard library.

    To opt into showing a frozen module, specify it in include_frames.
    """
    return "<frozen " in frame.f_code.co_filename


def import_filter(frame: types.FrameType, event: str, arg: object) -> bool:
    """
    Ignore import machinery

    The import system uses frozen modules, which don't have the same
    "lib/python" string fragment in their filepath as the standard
    library or third party code.
    """
    import_modules = (
        "<builtin>/frozen importlib._bootstrap_external",
        "<builtin>/frozen _structseq",
    )
    return frame.f_code.co_filename in import_modules


class LibraryPathFilter:
    """
    Ignore library code

    We want to not show library calls, so attempt to filter them out here.
    """

    __slots__ = ()

    # Cache all normalised path fragments.
    # Note: there is potentially a future where we can use `sys.base_prefix`, `sys.exec_prefix`,
    # `sys.prefix`, `sys.path`, and `sys.platlibdir` to amortise some of this further based on the
    # configured platform environment.
    paths = (
        os.path.normpath("lib/python"),
        os.path.normpath("lib/pypy"),
        os.path.normpath("versions/pypy"),
        os.path.normpath("/PyPy/"),
        os.path.normpath("/site-packages/"),
        os.path.normpath("/x64/lib/"),
    )
    special_case_windows = (
        os.path.normpath("/Python/"),
        os.path.normpath("/lib/"),
    )

    def __call__(self, frame: types.FrameType, *args, **kwargs) -> bool:
        filepath = frame.f_code.co_filename
        # Avoid any() + a <genexp> and break ASAP, it's marginally faster.
        for path in self.paths:
            if path in filepath:
                return True
        # Something like \python\python310\lib\ on windows
        return (
            self.special_case_windows[0] in filepath
            and self.special_case_windows[1] in filepath
        )


library_filter = LibraryPathFilter().__call__


def module_init_filter(frame: types.FrameType, event: str, arg: object) -> bool:
    return frame.f_code.co_name == "<module>"
