"""
Tests database tools
"""
import pathlib
import time
import unittest
from pathlib import Path
import threading
from typing import List, Tuple, Dict

import sqlite3
from contextlib import closing
from datetime import datetime, timedelta

from hein_control.db_tools import DatabaseTable, TimeBasedDatabaseTable, MissingColumnError, DatabaseRetentionPolicy

lock = threading.Lock()


def run_locked(func):
    """decorator to run a function using a lock"""
    def wrapper(*args, **kwargs):
        with lock:
            func(*args, **kwargs)
    return wrapper


class TestDatabaseTable(TimeBasedDatabaseTable):
    @property
    def table_name(self) -> str:
        return 'TEST_DB_TABLE'

    @property
    def column_name_types(self) -> List[Tuple[str, str]]:
        return [
            ('datetime', 'DATE'),
            ('col_1', 'TEXT'),
            ('col_2', 'REAL'),
            ('col_3', 'BOOL'),
        ]

    def retrieve(self,
                 start_time: datetime = None,
                 end_time: datetime = None,
                 duration: timedelta = timedelta(hours=1),
                 ) -> List[List]:
        if start_time is None and end_time is None:
            end_time = datetime.now()

        if start_time and end_time:
            pass
        elif start_time:
            end_time = start_time + duration
        elif end_time:
            start_time = end_time - duration
        command = self._select_query + " WHERE datetime BETWEEN :start_time AND :end_time"
        values = {
            'start_time': start_time,
            'end_time': end_time,
        }
        with sqlite3.connect(self.file_path) as db:
            with closing(db.cursor()) as cur:
                cur.execute(command, values)
                rows = cur.fetchall()
        out = []
        for row in rows:
            # cast each value to the types they should be
            try:
                dt = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S.%f")
            except ValueError:
                dt = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
            col_1 = str(row[1])
            col_2 = int(row[2])
            col_3 = bool(row[3])
            # add the row of values to the output
            r = [dt, col_1, col_2, col_3]
            out.append(r)
        return out


class BadTestTimeBasedDatabaseTable(TimeBasedDatabaseTable):
    @property
    def column_name_types(self) -> List[Tuple[str, str]]:
        return [
            ('col_1', 'TEXT'),
            ('col_2', 'REAL'),
            ('col_3', 'BOOL'),
        ]

    @property
    def table_name(self) -> str:
        return 'A_BAD_TEMPORAL_TEST_DB_TABLE'

    def retrieve(self,
                 start_time: datetime = None,
                 end_time: datetime = None,
                 duration: timedelta = timedelta(hours=1),
                 ) -> List[List]:
        # just pass this because we dont expect to be able to instantiate a class instance
        pass


class AnotherTestDatabaseTable(DatabaseTable):
    @property
    def column_name_types(self) -> List[Tuple[str, str]]:
        return [
            ('col_1', 'TEXT'),
            ('col_2', 'REAL'),
            ('col_3', 'BOOL'),
        ]

    @property
    def table_name(self) -> str:
        return 'ANOTHER_TEST_DB_TABLE'


class TestDatabaseTable31DayRetentionPolicy(DatabaseRetentionPolicy):
    """A policy to only retain entries made within the last 31 days"""
    @property
    def _retention_policy(self) -> str:
        policy = "delete from TEST_DB_TABLE  where datetime not between :start_time and :end_time"
        return policy

    @property
    def _retention_policy_values(self) -> Dict:
        end_time = datetime.now()
        start_time = end_time - timedelta(days=31)
        values = {
            'start_time': start_time,
            'end_time': end_time,
        }
        return values


class TestDBTools(unittest.TestCase):

    db_path: str = 'test_db.db'
    db_time_based_table: TimeBasedDatabaseTable = None
    db_retention_policy_31_days: TestDatabaseTable31DayRetentionPolicy = TestDatabaseTable31DayRetentionPolicy(enabled=False)

    def setUp(self) -> None:
        if Path(self.db_path).exists():
            # delete any existing db files
            Path(self.db_path).unlink()
        self.db_time_based_table = TestDatabaseTable(file_path=self.db_path)

    def test_db_extension(self):
        """tests db basic setting"""
        self.assertIsInstance(self.db_time_based_table.file_path, pathlib.Path, 'ensure table path is pathlib.Path')
        self.assertEqual(self.db_time_based_table.file_path.suffix, '.db', 'ensure extension exists')

    @run_locked
    def test_db_basic_properties(self):
        table_names = self.db_time_based_table.db_table_names
        self.assertEqual(1, len(table_names), 'there should only be 1 table in the database')
        self.assertEqual('TEST_DB_TABLE', table_names[0], 'the database table name should match')

        column_names = self.db_time_based_table.column_names
        self.assertEqual(4, len(column_names), 'there should only be 3 columns in the database')
        for index in range(4):
            if index == 0:
                self.assertEqual('datetime', column_names[index])
            else:
                col_number = index
                self.assertEqual(f'col_{col_number}', column_names[index])

    @run_locked
    def test_insert_retrieve_remove(self):
        wait_time = 1  # second, wait time between inserting data into the table

        # test inserting into the database table
        insert_1_time = datetime.now()
        insert_1 = (insert_1_time, 'insert 1', 1, True)
        self.db_time_based_table.insert(insert_1)
        expected_1 = [list(insert_1)]
        retrieve_1 = self.db_time_based_table.retrieve()
        self.assertEqual(expected_1, retrieve_1, 'ensure only 1 row with the correct values')
        time.sleep(wait_time)

        insert_2_time = datetime.now()
        insert_2 = (insert_2_time, 'insert 2', 2, True)
        self.db_time_based_table.insert(insert_2)
        expected_1_and_2 = [list(insert_1), list(insert_2)]
        retrieve_1_and_2 = self.db_time_based_table.retrieve()
        self.assertEqual(expected_1_and_2, retrieve_1_and_2, 'ensure both rows returned with the correct values')
        time.sleep(wait_time)

        insert_3_time = datetime.now()
        insert_3 = (insert_3_time, 'insert 3', 3, False)
        self.db_time_based_table.insert(insert_3)
        time.sleep(wait_time)

        insert_4_time = datetime.now()
        insert_4 = (insert_4_time, 'insert 4', 4, False)
        self.db_time_based_table.insert(insert_4)
        time.sleep(wait_time)

        insert_5_time = datetime.now()
        insert_5 = (insert_5_time, 'insert 5', 5, False)
        self.db_time_based_table.insert(insert_5)
        expected_1_and_2_and_3_and_4_and_5 = [list(insert_1), list(insert_2), list(insert_3), list(insert_4),
                                              list(insert_5)]
        retrieve_1_and_2_and_3_and_4_and_5 = self.db_time_based_table.retrieve()
        self.assertEqual(expected_1_and_2_and_3_and_4_and_5,
                         retrieve_1_and_2_and_3_and_4_and_5,
                         'ensure all five rows returned with the correct values')

        # test that retrieving data within specific timeframes work
        expected_1_and_2_and_3 = [list(insert_1), list(insert_2), list(insert_3)]
        retrieve_1_and_2_and_3 = self.db_time_based_table.retrieve(start_time=insert_1_time, end_time=insert_3_time)
        self.assertEqual(expected_1_and_2_and_3, retrieve_1_and_2_and_3,
                         'ensure retrieving from a start time & end time works')

        expected_2_and_3_and_4 = [list(insert_2), list(insert_3), list(insert_4)]
        # use duration of wait_time * 2.5 instead of 2 as a bit of a fudge factor for the time it takes to run code
        retrieve_2_and_3_and_4 = self.db_time_based_table.retrieve(start_time=insert_2_time, duration=timedelta(seconds=wait_time * 2.5))
        self.assertEqual(expected_2_and_3_and_4,
                         retrieve_2_and_3_and_4,
                         'ensure retrieving from a start time & duration works')

        expected_3_and_4 = [list(insert_3), list(insert_4)]
        # use duration of wait_time * 2.5 instead of 2 as a bit of a fudge factor for the time it takes to run code
        retrieve_3_and_4 = self.db_time_based_table.retrieve(end_time=insert_4_time, duration=timedelta(seconds=wait_time * 1.5))
        self.assertEqual(expected_3_and_4, retrieve_3_and_4,
                         'ensure retrieving from an end time & duration works')

        # test retaining rows only within specific times
        self.db_time_based_table.retain(start_time=insert_2_time, end_time=insert_5_time)
        expected_2_and_3_and_4_and_5 = [list(insert_2), list(insert_3), list(insert_4), list(insert_5)]
        retrieve_2_and_3_and_4_and_5 = self.db_time_based_table.retrieve()
        self.assertEqual(expected_2_and_3_and_4_and_5, retrieve_2_and_3_and_4_and_5,
                         'ensure retrieving from a start time & end time works')

        self.db_time_based_table.retain(start_time=insert_2_time, duration=timedelta(seconds=wait_time * 2.5))
        expected_2_and_3_and_4 = [list(insert_2), list(insert_3), list(insert_4)]
        retrieve_2_and_3_and_4 = self.db_time_based_table.retrieve()
        self.assertEqual(expected_2_and_3_and_4, retrieve_2_and_3_and_4,
                         'ensure retrieving from a start time & duration works')

        self.db_time_based_table.retain(end_time=insert_4_time, duration=timedelta(seconds=wait_time * 1.5))
        expected_3_and_4 = [list(insert_3), list(insert_4)]
        retrieve_3_and_4 = self.db_time_based_table.retrieve()
        self.assertEqual(expected_3_and_4, retrieve_3_and_4,
                         'ensure retrieving from an end time & duration works')

        # test retrieve and retain with default values works
        insert_31_days_ago_time = datetime.now() - timedelta(days=31, seconds=1)
        insert_31_days_ago = (insert_31_days_ago_time, 'insert 31 days ago', -31, True)
        self.db_time_based_table.insert(insert_31_days_ago)

        retrieve_3_and_4 = self.db_time_based_table.retrieve()
        self.assertEqual(expected_3_and_4, retrieve_3_and_4,
                         'ensure retrieving with defaults end time now duration 1 hour works')

        expected_3_and_4_and_neg31 = [list(insert_3), list(insert_4), list(insert_31_days_ago)]
        retrieve_3_and_4_and_neg31 = self.db_time_based_table.retrieve(duration=timedelta(days=32))
        self.assertEqual(expected_3_and_4_and_neg31, retrieve_3_and_4_and_neg31,
                         'ensure retrieving older than the default duration of 31 days works')

        self.db_time_based_table.retain()
        retrieve_3_and_4 = self.db_time_based_table.retrieve(duration=timedelta(days=32))
        self.assertEqual(expected_3_and_4, retrieve_3_and_4,
                         'ensure retaining with default end time now duration 1 hour works')

    @run_locked
    def test_retention_policy(self):
        self.assertFalse(self.db_retention_policy_31_days.enabled, 'retention policy should not be enabled')

        # initially add values into the database table
        insert_1_time = datetime.now()
        insert_1 = (insert_1_time, 'insert 1', 1, True)
        self.db_time_based_table.insert(insert_1)

        insert_almost_31_days_ago_time = datetime.now() - timedelta(days=30, hours=23, minutes=59)
        insert_almost_31_days_ago = (insert_almost_31_days_ago_time, 'insert almost 31 days ago', -31, True)
        self.db_time_based_table.insert(insert_almost_31_days_ago)

        insert_32_days_ago_time = datetime.now() - timedelta(days=32)
        insert_32_days_ago = (insert_32_days_ago_time, 'insert 32 days ago', -32, True)
        self.db_time_based_table.insert(insert_32_days_ago)

        # run the policy on the database table, but dont enable the policy so the values should not be removed
        expected_1_and_almost_31_and_32 = [list(insert_1), list(insert_almost_31_days_ago), list(insert_32_days_ago)]
        self.assertFalse(self.db_retention_policy_31_days(self.db_time_based_table),
                         'policy should not run because it is not enabled')
        retrieved_1_and_almost_31_and_32 = self.db_time_based_table.retrieve(duration=timedelta(days=33))
        self.assertEqual(expected_1_and_almost_31_and_32, retrieved_1_and_almost_31_and_32,
                         'all entries should be in the database')

        # run the policy on the database table with the policy enabled so values older than 31 days should be removed
        self.db_retention_policy_31_days.enabled = True
        self.assertTrue(self.db_retention_policy_31_days.enabled, 'retention policy should now be enabled')
        expected_1_and_almost_31 = [list(insert_1), list(insert_almost_31_days_ago)]
        policy_ran = self.db_retention_policy_31_days(self.db_time_based_table)
        self.assertTrue(policy_ran,
                        'policy should run because it is enabled')
        retrieved_1_and_almost_31 = self.db_time_based_table.retrieve(duration=timedelta(days=33))
        self.assertEqual(expected_1_and_almost_31, retrieved_1_and_almost_31,
                         'the 32 day old entry should be removed and only the other two entries should remain')

    @run_locked
    def test_adding_second_table(self):
        # test adding a second table to the database
        another_db_table = AnotherTestDatabaseTable(file_path=self.db_path)

        table_names = another_db_table.db_table_names
        self.assertEqual(2, len(table_names), 'there should only be 2 tables in the database')
        self.assertEqual(['TEST_DB_TABLE', 'ANOTHER_TEST_DB_TABLE'], table_names,
                         'the database table names should match')

    @run_locked
    def test_dont_add_a_bad_table(self):
        # should not be able to instantiate this TimeBasedDatabaseTable because datetime is not a column
        with self.assertRaises(MissingColumnError) as cm:
            BadTestTimeBasedDatabaseTable(file_path=self.db_path)
        self.assertEqual(cm.exception.msg, 'datetime must be a column in the table', 'ensure MissingColumnError was thrown')

    def test_basic_protection(self):
        """tests the basic sqlite injection prevention"""
        for attr in ['_base_query', 'table_name']:
            self.assertRaises(
                AttributeError,
                setattr,
                self.db_time_based_table,
                attr,
                'malicious value'
            )


