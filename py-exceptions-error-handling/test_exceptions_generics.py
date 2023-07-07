from typing import Generic, TypeVar

TableType = TypeVar("TableType", bound=int)


class BaseRepoError(Exception, Generic[TableType]):
    ...


#
# Errors
#


class BaseProjectJobMetadataError(Exception):
    ...
