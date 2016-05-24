import sys

from awsrdsmanager import json_pprint
from awsrdsmanager.sunsetrdssnapshots import SunsetRDSSnapshots


def sunset_rds_snapshots(args=sys.argv):
    """
    Wrapper for cli entrypoint for aws-rds-snapshot-cleanup

    :param List[str] args:
    :return:
    """
    json_pprint(
        SunsetRDSSnapshots.load(args).run()
    )
