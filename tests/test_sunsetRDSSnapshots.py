from unittest import TestCase
from datetime import datetime
from awsrdsmanager.sunsetrdssnapshots import SunsetRDSSnapshots


class TestSunsetRDSSnapshots(TestCase):
    def setUp(self):
        self.maxDiff = None

    # def test__sort_snapshots_by_threshold_date(self):
    #     sunset_snapshot_command = SunsetRDSSnapshots(
    #         database_name='',
    #         sunset_period=5,
    #         region='',
    #         dry_run=True,
    #         session=None,
    #         enable_logging=False
    #     )
    #
    #     snapshots_before, snapshots_after = sunset_snapshot_command._sort_snapshots_by_threshold_date(
    #         threshold_date='',
    #         snapshots=[{
    #
    #         }]
    #     )

    def test_obj_list_sort(self):
        sunset_snapshot_command = SunsetRDSSnapshots(
            database_name='',
            sunset_period=5,
            region='',
            dry_run=True,
            session=None,
            enable_logging=False
        )
        result = sunset_snapshot_command._sort_by_key('SnapshotCreateTime', [{
            'SnapshotCreateTime': datetime(2015, 1, 2),
            'MasterUsername': 'second_entry'
        }, {
            'SnapshotCreateTime': datetime(2015, 1, 1),
            'MasterUsername': 'first_entry'
        }, {
            'SnapshotCreateTime': datetime(2015, 1, 4),
            'MasterUsername': 'fourth_entry'
        }, {
            'SnapshotCreateTime': datetime(2015, 1, 3),
            'MasterUsername': 'third_entry'
        }])

        self.assertListEqual(result, [{
            'SnapshotCreateTime': datetime(2015, 1, 4),
            'MasterUsername': 'fourth_entry'
        }, {
            'SnapshotCreateTime': datetime(2015, 1, 3),
            'MasterUsername': 'third_entry'
        }, {
            'SnapshotCreateTime': datetime(2015, 1, 2),
            'MasterUsername': 'second_entry'
        }, {
            'SnapshotCreateTime': datetime(2015, 1, 1),
            'MasterUsername': 'first_entry'
        }], )

    def test__sort_snapshots_by_threshold_period(self):
        sunset_snapshot_command = SunsetRDSSnapshots(
            database_name='',
            sunset_period=5,
            region='',
            dry_run=True,
            session=None,
            enable_logging=False
        )

        snapshots_before, snapshots_after = sunset_snapshot_command._sort_snapshots_by_threshold_period(
            threshold_count=2,
            snapshots=[{
                'SnapshotCreateTime': datetime(2015, 1, 1),
                'MasterUsername': 'first_entry'
            }, {
                'SnapshotCreateTime': datetime(2015, 1, 2),
                'MasterUsername': 'second_entry'
            }, {
                'SnapshotCreateTime': datetime(2015, 1, 3),
                'MasterUsername': 'third_entry'
            }, {
                'SnapshotCreateTime': datetime(2015, 1, 4),
                'MasterUsername': 'fourth_entry'
            }]
        )

        self.assertListEqual(snapshots_before, [{
            'SnapshotCreateTime': datetime(2015, 1, 4),
            'MasterUsername': 'fourth_entry'
        }, {
            'SnapshotCreateTime': datetime(2015, 1, 3),
            'MasterUsername': 'third_entry'
        }])

        self.assertListEqual(snapshots_after, [{
            'SnapshotCreateTime': datetime(2015, 1, 2),
            'MasterUsername': 'second_entry'
        }, {
            'SnapshotCreateTime': datetime(2015, 1, 1),
            'MasterUsername': 'first_entry'
        }])
