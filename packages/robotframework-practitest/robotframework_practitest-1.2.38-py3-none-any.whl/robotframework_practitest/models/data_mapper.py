from __future__ import annotations

import time
from enum import Enum
from time import sleep
from typing import List

import pandas

from robotframework_practitest.utils.logger import LOGGER as logger

DEFAULT_RETENTION_TIMEOUT = 300

class _Color(Enum):
    FAILED = 'red'
    PASSED = 'green'
    SKIPPED = 'yellow'
    Default = 'grey'


class TestStates(Enum):
    Robot = 'robot'
    PractiTest = 'practi_test'
    Status = 'status'

    @staticmethod
    def as_tuple():
        return TestStates.Robot, TestStates.PractiTest, TestStates.Status


class TestStatuses(Enum):
    NotRun = 'not_run'
    Pending = 'Pending'
    PASSED = 'passed'
    FAILED = 'failed'
    SKIPPED = 'skipped'


class RowItem(dict):
    def __init__(self, **kwargs):
        for col in TestStates:
            self[col.name] = kwargs.get(col.name, None)
            # setattr(self, col.name, kwargs.get(col.name, ''))

    def __str__(self):
        return ', '.join([f"{col.name}={getattr(self, col.name)}" for col in TestStates])


class _TestTable(list, List[RowItem]):
    def set_test(self, col: TestStates, tests: list | str, status: TestStatuses = None):
        if isinstance(tests, str):
            tests = [tests]
        if col == TestStates.Robot:
            for test in tests:
                row_item = RowItem(**{TestStates.Robot.name: test, TestStates.PractiTest.name: '-',
                                      TestStates.Status.name: TestStatuses.NotRun})
                self.append(row_item)
        elif col == TestStates.PractiTest:
            for test in tests:
                for i, item in enumerate(self):
                    if test.startswith(self[i].get(TestStates.Robot.name)):
                        self[i][TestStates.PractiTest.name] = test
                        if status:
                            self[i][TestStates.Status.name] = status.name
                        break
        elif col == TestStates.Status:
            assert status, f"State {col.name} require status"
            for test in tests:
                for i, item in enumerate(self):
                    if self[i].get(TestStates.PractiTest.name) == test:
                        self[i][TestStates.Status.name] = status.name
                        break

    def as_dict(self, *columns, **filters):
        columns = columns if len(columns) > 0 else TestStates.as_tuple()
        res_dict = {col.name: [] for col in columns}
        for row in self:
            if len(filters) > 0:
                for field, value in filters.items():
                    if isinstance(value, (list, tuple)):
                        if row.get(field) not in (v.name for v in value):
                            continue
                    else:
                        if row.get(field) != value.name:
                            continue
                    for col in columns:
                        res_dict[col.name].append(row.get(col.name))
            else:
                for col in columns:
                    res_dict[col.name].append(row.get(col.name))
        return res_dict

    def df(self, *columns, **filters):
        return pandas.DataFrame.from_dict(self.as_dict(*columns, **filters))

    @staticmethod
    def _field_formatter(value):
        return value

    @staticmethod
    def _status_formatter(value):
        try:
            color = _Color[value]
        except Exception as e:
            color = _Color.Default

        return f"<font color='{color.value}'>{value}</font>"

    def show(self, *columns, html=False, **filters):
        df = self.df(*columns, **filters)
        pandas.set_option("display.precision", 2)
        pandas.set_option('display.max_rows', None)
        pandas.set_option('display.max_columns', None)
        pandas.set_option("max_colwidth", 500)
        pandas.set_option('display.colheader_justify', 'left')
        pandas.set_option('display.width', 10000)
        return df.to_html(justify='center') if html else df.to_string(justify='center')

    def wait_state(self, timeout=DEFAULT_RETENTION_TIMEOUT, **statuses):
        logger.console(f"{self}; Waiting to complete all tests got statuses -> {statuses}")
        start_ts = time.perf_counter()

        while True:
            try:
                if len(self.as_dict(TestStates.PractiTest, **statuses)[TestStates.PractiTest]) == 0:
                    raise AssertionError()
                if (time.perf_counter() - start_ts) >= timeout:
                    raise TimeoutError("Test completion taking too much time")
                logger.console(f"{self.show(TestStates.PractiTest, TestStates.Status, **statuses)}")
                sleep(1)
            except AssertionError:
                logger.console(f"All tests completed:\nTest list:\n{self.show()}")
                break
            except TimeoutError as e:
                logger.error(f"{e}\n\n{self.show()}")
                raise


DataStatistics = _TestTable


__all__ = [
    'TestStates',
    'TestStatuses',
    'DataStatistics'
]
