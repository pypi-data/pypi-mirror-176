from __future__ import annotations

import time
from enum import Enum
from threading import Timer, Event
from time import sleep
from typing import List

import pandas

from robotframework_practitest.utils.logger import LOGGER as logger


DEFAULT_RETENTION_TIMEOUT = 120


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
        res_dict = {col: [] for col in columns}
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
                        res_dict[col].append(row.get(col.name))
            else:
                for col in columns:
                    res_dict[col].append(row.get(col.name))
        return res_dict

    def df(self, *columns, **filters):
        return pandas.DataFrame.from_dict(self.as_dict(*columns, **filters))

    def show(self, *columns, **filters):
        df = self.df(*columns, **filters)
        pandas.set_option('display.max_rows', None)
        pandas.set_option('display.max_columns', None)
        pandas.set_option('display.colheader_justify', 'left')
        pandas.set_option('display.width', 10000)
        return f"{df}"

    def wait_state(self, timeout=DEFAULT_RETENTION_TIMEOUT, **statuses):
        logger.console(f"{self}; Waiting to complete all tests got statuses -> {statuses}")
        start_ts = time.perf_counter()
        _event = Event()

        while not _event.is_set():
            try:
                if len(self.as_dict(TestStates.PractiTest, **statuses)[TestStates.PractiTest]) == 0:
                    raise AssertionError()
                if (time.perf_counter() - start_ts) >= timeout:
                    raise TimeoutError("Test completion taking too much time")
                logger.console(f"{self.show(TestStates.PractiTest, TestStates.Status, **statuses)}")
                sleep(1)
            except AssertionError:
                logger.info("All tests completed")
                break
            except TimeoutError as e:
                logger.error(f"{e}")
                raise


#
# class _TestInstancesCountControl(dict):
#     def __init__(self):
#         dict.__init__(self)
#         for state in TestStates:
#             self.setdefault(state.name, [])
#
#     def set_test(self, state: TestStates, tests: list | str, status: TestStatuses = None):
#         if isinstance(tests, str):
#             tests = [tests]
#         assert state.name in self.keys(), f"State '{state}' not defined"
#
#         if state == TestStates.Robot:
#             self[state.name].extend(tests)
#             self[TestStates.PractiTest.name].extend(['-' for _ in tests])
#             self[TestStates.Status.name].extend([TestStatuses.NotRun.name for _ in tests])
#
#         elif state == TestStates.PractiTest:
#             for p_test in tests:
#                 for i, r_test in enumerate(self[TestStates.Robot.name]):
#                     if p_test.startswith(r_test):
#                         self[state.name][i] = p_test
#                         if status:
#                             self[TestStates.Status.name][i] = status.name
#         elif state == TestStates.Status:
#             assert status, f"State {state.name} require status"
#             for p_test in tests:
#                 for i, r_test in enumerate(self[TestStates.Robot.name]):
#                     if p_test.startswith(r_test):
#                         self[state.name][i] = status.name
#         else:
#             raise AttributeError(f"Unknown state ({state})")
#
#     def wait_states_equality(self, state1: TestStates, state2: TestStates, timeout=DEFAULT_RETENTION_TIMEOUT):
#         logger.console(f"{self}; Waiting to complete all items between {state1.name} & {state2.name}")
#         start_ts = time.perf_counter()
#
#         def _():
#             logger.error(f"PractiTestCompletion keeps too much time ({(time.perf_counter() - start_ts) / 60000}m.)")
#
#         Timer(timeout, _).start()
#         while len(self.get(state1.name)) != len(self.get(state2.name)):
#             text = self.show(TestStates.PractiTest, TestStates.Status,
#                              **{TestStates.Status: (TestStatuses.NotRun, TestStatuses.Pending)})
#             logger.console(f"{text}")
#             sleep(1)
#         logger.info(self)
#
#     def _filter_by(self, **filters):
#         for col, values in filters.items():
#             for rows in [i for i, v in self[col.name] if v in values]:
#                 for f in TestStates:
#                     yield f.name, [v for i, v in enumerate(self[f.name]) if i in rows]
#
#     def show(self, *columns, **filters):
#         filtered_data = dict(self._filter_by(**filters)) if len(filters) > 0 else dict(**self)
#         df = pandas.DataFrame.from_dict({k: v for k, v in filtered_data.items()
#                                          if k in [c.name for c in columns]})
#         pandas.set_option('display.max_rows', None)
#         pandas.set_option('display.max_columns', None)
#         pandas.set_option('display.colheader_justify', 'left')
#         pandas.set_option('display.width', 10000)
#         return f"{df}"


DataMapper = _TestTable


__all__ = [
    'TestStates',
    'TestStatuses',
    'DataMapper'
]
