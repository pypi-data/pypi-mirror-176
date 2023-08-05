from .__base import BaseError, InternalError, FileError


class NotImplemented(InternalError):
    """NotImplemented"""


class InconsistentData(FileError):
    """InconsistentData"""
