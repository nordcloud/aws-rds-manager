import typing

import awsrdsmanager.sunsetrdssnapshots
from awsrdsmanager.base import Base


class SunsetRDSSnapshots(Base):
    @classmethod
    def load(cls, args: typing.List[str]) -> awsrdsmanager.sunsetrdssnapshots.SunsetRDSSnapshots: ...

    def __init__(self, database_name: str, sunset_period: int, region: str, logging_level: str, session,
                 dry_run: bool) -> None: ...
