import json
import typing

if typing.TYPE_CHECKING:
    from .models import GWDGUser


class IDMNotReachableError(Exception):
    pass


class IDMRequestError(Exception):
    pass


class BadJsonError(Exception):
    pass


class AlreadyDeletedError(Exception):
    pass


def pretty_print(obj: "GWDGUser | list[GWDGUser]") -> str:
    if isinstance(obj, list):
        return pretty_multy_print(obj)
    else:
        return pretty_single_print(obj)


def pretty_single_print(obj: "GWDGUser") -> str:
    return json.dumps(obj.dict(), indent=2)


def pretty_multy_print(obj: list["GWDGUser"]) -> str:
    return json.dumps([entry.dict() for entry in obj], indent=2)
