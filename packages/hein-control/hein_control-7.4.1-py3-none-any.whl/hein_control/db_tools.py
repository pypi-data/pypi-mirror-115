"""
Module for interacting with an SQLite3 database (.db files)
"""
import sqlite3
import pathlib

from abc import ABC, abstractmethod
from typing import List, Tuple, Union, Dict
from contextlib import closing
from datetime import datetime, timedelta

import warnings


class MissingColumnError(Exception):
    """
    Error for a missing column in a DatabaseTable
    """

    def __init__(self, msg=None):
        self.msg = msg or 'An expected column is missing from the database table'

    def __str__(self):
        return self.msg


def get_db_table_names(file_path: str) -> List[str]:
    """Return a list of table names, given the database path"""
    with sqlite3.connect(file_path) as db:
        with closing(db.cursor()) as cur:
            cur.execute(f"SELECT name FROM sqlite_master WHERE type='table'")
            table_names = [names[0] for names in cur.fetchall()]
    return table_names


def get_db_column_names(file_path, table_name: str) -> List[str]:
    """Return a list of the column names for a table in a database, given the database path"""
    raise NotImplementedError('access the get_table_column_names method of DatabaseTable')


class DatabaseTable(ABC):
    def __init__(self, file_path: Union[str, pathlib.Path]):
        """
        Create a SQLite3 table at the database at the path with the columns if it doesnt already exist

        This is a SQLite3 database table mixin. To use, subclass this class and define the table_name and
        column_name_types. Basic sql injection attack prevention is provided by disallowing the user to set the
        table name and column definitions (defined when the class is defined). There is no protection against imporper
        definition of the subclasses.

        :param file_path: path to the database (.db file)
        """
        self._file_path: pathlib.Path = None
        self.file_path = file_path

        # create table if it does not exist
        commands = []
        # build command and parameters so that they can be executed safely
        for name, value_type in self.column_name_types:
            commands.append(f'{name} {value_type}')
        table_structure = ', '.join(commands)
        with sqlite3.connect(self.file_path) as db:
            with closing(db.cursor()) as cur:
                # create the table
                cur.execute(
                    f'CREATE TABLE IF NOT EXISTS {self.table_name} ({table_structure})',
                )
            db.commit()

        self.column_names: List[str] = self.get_table_column_names()

    @property
    def file_path(self) -> pathlib.Path:
        """Path to the database .db file"""
        return self._file_path

    @file_path.setter
    def file_path(self, value):
        if value is not None:
            if isinstance(value, pathlib.Path) is False:
                value = pathlib.Path(value)
            if value.suffix != '.db':
                value = value.parent / (value.name + '.db')
            self._file_path = value

    @property
    @abstractmethod
    def table_name(self) -> str:
        """Name of the table in the database"""
        raise NotImplementedError

    @property
    @abstractmethod
    def column_name_types(self) -> List[Tuple[str, str]]:
        """defines the column names and types to be used if the table needs to be created"""
        raise NotImplementedError

    @property
    def _base_query(self) -> str:
        """the base query for the instance. This provides a basic security layer between the user and the query for
        avoiding sql injections"""
        warnings.warn('use _select_query instead', DeprecationWarning, stacklevel=2)
        return self._select_query

    @property
    def _select_query(self) -> str:
        """the select query for the instance. This provides a basic security layer between the user and the query for
        avoiding sql injections"""
        return f'select * from {self.table_name}'

    @property
    def _insert_query(self) -> str:
        """the delete query for the instance. This provides a basic security layer between the user and the
        query for avoiding sql injections"""
        return f'insert into {self.table_name} values ({", ".join(["?" for _ in range(len(self.column_names))])})'

    @property
    def _delete_query(self) -> str:
        """the base query for the instance. This provides a basic security layer between the user and the query for
        avoiding sql injections"""
        # todo should it be that this must be implemented in the subclass to for safety?
        return f'delete from {self.table_name}'

    @property
    def db_table_names(self) -> List[str]:
        """A list of the name of all tables in the database"""
        names = get_db_table_names(file_path=self.file_path)
        return names

    def get_table_column_names(self) -> List[str]:
        """Return a list of the column names for a table in a database, given the database path"""
        with sqlite3.connect(self.file_path) as db:
            with closing(db.cursor()) as cur:
                # todo scrub for sql injection
                cur.execute(self._select_query)
                column_names = [description[0] for description in cur.description]
        return column_names

    def insert(self, values) -> None:
        """
        Inserts values into the database table. The order of the values in the Tuple must match to how they are
        listed in the column_name_types property

        :param values: tuple of the values to insert into the database table
        :return:
        """
        with sqlite3.connect(self.file_path) as db:
            with closing(db.cursor()) as cur:
                cur.execute(self._insert_query, values)
                db.commit()


class TimeBasedDatabaseTable(DatabaseTable):
    def __init__(self, file_path: Union[str, pathlib.Path]):
        """
        A DatabaseTable, with additional methods to retrieve and delete entries based on time; a TimeBasedDatabaseTable
        MUST have a column called 'datetime'

        This is a SQLite3 database table mixin. To use, subclass this class and define the table_name and
        column_name_types. Basic sql injection attack prevention is provided by disallowing the user to set the
        table name and column definitions (defined when the class is defined). There is no protection against imporper
        definition of the subclasses. All subclasses MUST have a column called 'datetime'

        :param file_path: path to the database (.db file)
        """
        column_names = [name for name, value_type in self.column_name_types]
        if 'datetime' not in column_names:
            raise MissingColumnError('datetime must be a column in the table')
        DatabaseTable.__init__(self, file_path)

    @abstractmethod
    def retrieve(self,
                 start_time: datetime = None,
                 end_time: datetime = None,
                 duration: timedelta = timedelta(hours=1),
                 ) -> List[List]:
        """
        Retrieve entries that fall within a time range (inclusive of the start and end times). Must be overwritten
        by the subclass, and the subclass must have a column called "datetime".

        Either provide:
            - start_time and end_time, then duration won't be used
            - start_time and duration, then end_time is start_time + duration
            - end_time and duration, then start_time is end_time - duration
            - only duration, then a default end_time of now is used

        Example of how this might be implemented:
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
                # overwrite until out.append(r) to properly cast the values for the subclass and add them to r
                col_1 = str(row[1])
                col_2 = int(row[2])
                col_3 = bool(row[3])
                # add the row of values to the output
                r = [dt, col_1, col_2, col_3]
                out.append(r)
            return out

        :param start_time: datetime object to denote the start of the time range to retrieve entries
        :param end_time: datetime object to denote the end of the time range to retrieve entries
        :param duration: timedelta object for how long the the time range to retrieves entries is. Default 1 hour
        :return: a list of lists. the inner lists each represent a row from the database, and each value in the inner
            list represents the value for a column index
        """
        raise NotImplementedError

    def retain(self,
               start_time: datetime = None,
               end_time: datetime = None,
               duration: timedelta = timedelta(days=31),
               ) -> None:
        """
        Only retain the entries that fall within a time range and delete everything else from the database table
        (retain entries that fall on the start and end times).

        'datetime' must be a column in the database table

        Either provide:
            - start_time and end_time, then duration won't be used
            - start_time and duration, then end_time is start_time + duration
            - end_time and duration, then start_time is end_time - duration
            - only duration, then a default end_time of now is used

        https://sqlite.org/lang_delete.html

        :param start_time: datetime object to denote the start of the time range to retain entries
        :param end_time: datetime object to denote the end of the time range to retain entries
        :param duration: timedelta object for how long the the time range to retain entries is. Default 31 days
        :return:
        """
        if 'datetime' not in self.column_names:
            raise MissingColumnError('datetime must be one of the columns in the database')

        if start_time is None and end_time is None:
            end_time = datetime.now()

        if start_time and end_time:
            pass
        elif start_time:
            end_time = start_time + duration
        elif end_time:
            start_time = end_time - duration

        command = self._delete_query + " WHERE datetime NOT BETWEEN :start_time AND :end_time"
        values = {
            'start_time': start_time,
            'end_time': end_time,
        }

        with sqlite3.connect(self.file_path) as db:
            with closing(db.cursor()) as cur:
                cur.execute(command, values)


class DatabaseRetentionPolicy(ABC):
    def __init__(self, enabled: bool = False):
        """
        A retention policy that can be run by on a DatabaseTable; it should remove entries from the .db SQLite database
        based on the _retention_policy

        This is an abstract base class. To use, subclass this class and define the _retention_policy. There is no
        protection against improper definition of the subclasses. Since an exact _retention_policy must be defined,
        it is up to the implementor to ensure that the retention policy will successfully execute on the provided
        DatabaseTable instance

        :param enabled: whether to actually execute the retention policy on a DatabaseTable when a
            DatabaseRetentionPolicy instance is called
        """
        self._enabled = enabled

    @property
    @abstractmethod
    def _retention_policy(self) -> str:
        """The exact SQL statement to execute to edit a SQLite .db database table"""
        raise NotImplementedError

    def __call__(self, *args, **kwargs) -> bool:
        """Execute the retention policy for the database if the policy is enabled and return whether the retention
        policy was actually run or not"""
        return self._run(*args, **kwargs)

    @property
    @abstractmethod
    def _retention_policy_values(self) -> Dict:
        """Dictionary for the _retention_policy. Keys should match the variables that should be replaced in the
        _retention_policy"""
        raise NotImplementedError

    @property
    def enabled(self) -> bool:
        """Whether the retention policy is enabled and should actually be executed when the DatabaseRetentionPolicy
        instance is called"""
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        if value:
            self._enabled = value

    def _run(self, database_table: DatabaseTable) -> bool:
        """
        Execute the retention policy for the database if the policy is enabled

        :param database_table: the DatabaseTable that will run the policy
        :return: bool, whether the retention policy was run or not
        """
        if self.enabled:
            with sqlite3.connect(database_table.file_path) as db:
                with closing(db.cursor()) as cur:
                    cur.execute(self._retention_policy, self._retention_policy_values)
            return True
        else:
            return False
