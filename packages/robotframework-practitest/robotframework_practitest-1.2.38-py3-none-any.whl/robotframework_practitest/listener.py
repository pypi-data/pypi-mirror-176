"""This module includes Robot service for reporting results to Report Portal.

"""
from __future__ import annotations

from typing import Optional

from robot.api import logger
from robot.result.model import TestSuite as RSuite, TestCase as RTest
from robot.running import TestSuite as ESuite, TestCase as ETest

import robotframework_practitest.models.practi_test as practit_m
import robotframework_practitest.models.robot as robot_m
import robotframework_practitest.services.configuration as config
from robotframework_practitest.models import adapter
from robotframework_practitest.models.data_mapper import TestStates, TestStatuses
from robotframework_practitest.models.robot.helpers import PT_MANAGED_ITEMS, publish_to_metadata, \
    log_report
from robotframework_practitest.models.robot.running import get_parents_path
from robotframework_practitest.services.background import *
from robotframework_practitest.utils.logger import LOGGER as bg_logger
from robotframework_practitest.utils.misc_utils import get_error_info, read_variables


class Listener(adapter.RobotToPractiTest_Adapter):
    """Class represents service that sends Robot items to PractiTest API."""
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self):
        """Initialize service attributes."""
        self._debug = False
        self.api_client: Optional[practit_m.PtClient] = None
        self.test_set_level = None
        self.current_suite_path_list = []

        self.version = None
        self.external_run_id = None
        self._metadata_collection = []

        super(Listener, self).__init__()

    @property
    def test_set_name(self):
        return '/'.join(self.current_suite_path_list)

    def init_api(self, **kwargs):
        """Initialize common PractiTest API client."""
        if self.api_client is None:
            try:
                assert kwargs.get('PT_ENABLED', False), "PractiTest report disabled"
                endpoint = kwargs.get('PT_ENDPOINT', None)
                project = kwargs.get('PT_PROJECT_NAME', None)
                tester_name = kwargs.get('PT_USER_NAME', None)
                user_email = kwargs.get('PT_USER_NAME_EMAIL', None)
                user_token = kwargs.get('PT_USER_TOKEN', None)
                self.test_tag_mapping = (kwargs.get('TAG_MAPPING'))

                self._debug = kwargs.get('PT_DEBUG')
                self.version = kwargs.get('PT_VERSION')
                self.external_run_id = kwargs.get('PT_EXTERNAL_RUN_ID')
                self.test_set_level = kwargs.get('PT_TEST_SET_LEVEL', 0)
                self.api_client = practit_m.PtClient(endpoint, project_name=project, tester_name=tester_name,
                                                     user_email=user_email, user_token=user_token,
                                                     foreground=kwargs.get('PT_FOREGROUND', False))
                self.api_client.initiate_session()
                self.init_adapter(self.api_client, *kwargs.get('PT_FIELDS_MAP'),
                                  **{PT_MANAGED_ITEMS.Test.name: kwargs.get(PT_MANAGED_ITEMS.Test.value),
                                     PT_MANAGED_ITEMS.TestSet.name: kwargs.get(PT_MANAGED_ITEMS.TestSet.value),
                                     PT_MANAGED_ITEMS.Instance.name: kwargs.get(PT_MANAGED_ITEMS.Instance.value)
                                     })
                self.enabled_reporting = True
                logger.info(
                    'PractiTest report enabled; Session info:'
                    'endpoint={0}, project={1}, User={2}'.format(endpoint, project, tester_name))
            except AssertionError as e:
                logger.info(f"{e}", also_console=True)
            except Exception as e:
                f, li = get_error_info()
                logger.warn(f"{e}; File: {f}:{li}")
        else:
            logger.warn('Practitest service already initialized.')

    def close(self):
        """Terminate common PractiTest API Client."""
        Task.shutdown()
        if self.api_client is not None:
            self.api_client.terminate_session()
        bg_logger.log_background_messages()

    def test_set_post_process(self, suite):
        def _():
            self._metadata_collection.append(dict(suite=suite.name, project_id=self.project_id,
                                                  **self.get_active_test_set_id(20)))
        return _

    def start_suite(self, suite: ESuite, result: RSuite):
        """Call start_test method of the common client.

        :param result:
        :param suite: model.Suite object
        :return:
        """
        try:
            if suite.parent is None:
                self.init_api(**read_variables(*config.PRACTI_TEST_VARIABLES))
            if not self.enabled_reporting:
                return

            if len(get_parents_path(suite)) == self.test_set_level:
                data_snapshot = robot_m.running.PTestSuite(suite)
                self.set_test(TestStates.Robot, list(data_snapshot.all_tests('name')))
                run_mode = TaskType.Foreground if self._debug else TaskType.Synchron
                Task(self.start_test_set, data_snapshot, self.version, run_id=self.external_run_id,
                     post_process=self.test_set_post_process(suite)).run(run_mode)
                logger.console(f"Start suite {suite.name}; Planned tests:\n{self.show(TestStates.Robot)}")
        except Exception as e:
            f, li = get_error_info()
            logger.error(f"Start suite {suite.name} [Error: {e}; File: {f}:{li}]")

    def end_suite(self, suite: ESuite, result: RSuite):
        if not self.enabled_reporting:
            return
        if suite.parent is None:
            try:
                self.wait_state(**{TestStates.Status.name: (TestStatuses.NotRun, TestStatuses.Pending)})
            except TimeoutError as e:
                logger.warn(f"Cannot complete uploading to PractiTest ({self})")
            except Exception as e:
                f, li = get_error_info()
                logger.warn(f"Start test: {suite.name} [Error: {e}; File: {f}:{li}]")

            publish_to_metadata("PractiTest reports", *self._metadata_collection)
            if adapter.MISSED_TEST_IDs:
                logger.warn(f"PractiTest: Following tests not found: {', '.join(adapter.MISSED_TEST_IDs)}")
            log_report("PractiTest reports", f"{self.show(TestStates.PractiTest, TestStates.Status, html=True)}",
                       *self._metadata_collection)

        bg_logger.log_background_messages()

    def start_test(self, test: ETest, result: RTest):
        if not self.enabled_reporting:
            return
        try:
            test_p = robot_m.running.PTestCase(test)
            run_mode = TaskType.Foreground if self._debug else TaskType.Synchron
            Task(self.create_test_instance, test_p, self.version).run(run_mode)
        except Exception as e:
            f, li = get_error_info()
            logger.warn(f"Start test: {test.name} [Error: {e}; File: {f}:{li}]")
        finally:
            bg_logger.log_background_messages()

    def end_test(self, test: ETest, result: RTest):
        if not self.enabled_reporting:
            return
        try:
            test_p = robot_m.running.PTestCase(test)
            result_p = robot_m.running.PTestResult(result)
            run_mode = TaskType.Foreground if self._debug else TaskType.Synchron
            Task(self.set_test_results, test_p, result_p).run(run_mode)
        except Exception as e:
            f, w = get_error_info()
            logger.warn(f"End test {test.name} [Error: {e}; File: {f}:{w}]")
        finally:
            bg_logger.log_background_messages()


__all__ = [
    'Listener'
]
