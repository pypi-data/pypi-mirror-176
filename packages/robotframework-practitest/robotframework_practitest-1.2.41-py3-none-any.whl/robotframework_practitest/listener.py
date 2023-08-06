"""This module includes Robot service for reporting results to Report Portal.

"""
from __future__ import annotations

from typing import Optional

from robot.api import logger
from robot.result.model import TestCase as RTest
from robot.running import TestSuite as ESuite, TestCase as ETest
from robot.utils import is_truthy

from robotframework_practitest.models import practi_test as pt, robot as rb, adapter
from robotframework_practitest.models.robot import helpers, running
from robotframework_practitest.services import configuration as config, scheduler, statistics as st
from robotframework_practitest.utils import get_error_info, read_variables
from robotframework_practitest.utils.logger import LOGGER as bg_logger


class Listener(adapter.RobotToPractiTest_Adapter):
    """Class represents service that sends Robot items to PractiTest API."""
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self):
        """Initialize service attributes."""
        self._debug = False
        self.api_client: Optional[pt.PtClient] = None
        self.version = None
        self._metadata_collection = []

        super(Listener, self).__init__()

    @property
    def test_set_name(self):
        return '/'.join(self.current_suite_path_list)

    def init_api(self, **kwargs):
        """Initialize common PractiTest API client."""
        if self.api_client is None:
            try:
                assert is_truthy(kwargs.get('PT_ENABLED', False)), "PractiTest report disabled"
                endpoint = kwargs.get('PT_ENDPOINT', None)
                project = kwargs.get('PT_PROJECT_NAME', None)
                tester_name = kwargs.get('PT_USER_NAME', None)
                user_email = kwargs.get('PT_USER_NAME_EMAIL', None)
                user_token = kwargs.get('PT_USER_TOKEN', None)
                self.test_tag_mapping = (kwargs.get('TAG_MAPPING'))

                self._debug = is_truthy(kwargs.get('PT_DEBUG', False))
                self.version = kwargs.get('PT_VERSION')
                self.external_run_id = kwargs.get('PT_EXTERNAL_RUN_ID')
                self.test_set_level = kwargs.get('PT_TEST_SET_LEVEL', 0)
                self.api_client = pt.PtClient(endpoint, project_name=project, tester_name=tester_name,
                                              user_email=user_email, user_token=user_token,
                                              foreground=kwargs.get('PT_FOREGROUND', False))
                self.api_client.initiate_session()
                self.init_adapter(self.api_client, *kwargs.get('PT_FIELDS_MAP'),
                                  **{helpers.PT_MANAGED_ITEMS.Test.name:
                                         kwargs.get(helpers.PT_MANAGED_ITEMS.Test.value),
                                     helpers.PT_MANAGED_ITEMS.TestSet.name:
                                         kwargs.get(helpers.PT_MANAGED_ITEMS.TestSet.value),
                                     helpers.PT_MANAGED_ITEMS.Instance.name: kwargs.get(
                                         helpers.PT_MANAGED_ITEMS.Instance.value)
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
        if not self.enabled_reporting:
            return
        """Terminate common PractiTest API Client."""
        scheduler.Task.shutdown()
        if self.api_client is not None:
            self.api_client.terminate_session()
        bg_logger.log_background_messages()

    def test_set_post_process(self, suite):
        def _():
            self._metadata_collection.append(dict(suite=suite.name, project_id=self.project_id,
                                                  **self.get_active_test_set_id(20)))

        return _

    def start_suite(self, suite: ESuite, *_):
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

            pt_suite = rb.running.PTestSuite(suite)
            if len(running.get_parents_path(suite)) == self.test_set_level:
                run_mode = scheduler.TaskType.Foreground if self._debug else scheduler.TaskType.Synchron
                scheduler.Task(self.start_test_set, pt_suite, self.version, run_id=self.external_run_id,
                               post_process=self.test_set_post_process(suite)).run(run_mode)
                logger.console(f"Suite '{suite.name}' started as TestSet")

            if pt_suite.is_data_driver:
                self._data_driver_flag = True
                return
            if pt_suite.tests:
                self.add_suite_tests(pt_suite)
        except Exception as e:
            f, li = get_error_info()
            logger.error(f"Start suite {suite.name} [Error: {e}; File: {f}:{li}]")

    def end_suite(self, suite: ESuite, *_):
        if not self.enabled_reporting:
            return
        if suite.parent is None:
            try:
                self.wait_state()
            except TimeoutError as e:
                logger.warn(f"Cannot complete uploading to PractiTest ({self})")
            except Exception as e:
                f, li = get_error_info()
                logger.warn(f"Start test: {suite.name} [Error: {e}; File: {f}:{li}]")

            helpers.publish_to_metadata("PractiTest reports", *self._metadata_collection)
            if adapter.MISSED_TEST_IDs:
                logger.warn(f"PractiTest: Following tests not found: {', '.join(adapter.MISSED_TEST_IDs)}")
            helpers.log_report("PractiTest reports",
                               self.show(st.TestStates.Robot, st.TestStates.PractiTest, st.TestStates.Status,
                                         html=True),
                               *self._metadata_collection)

        bg_logger.log_background_messages()

    def start_test(self, test: ETest, *_):
        if not self.enabled_reporting:
            return
        try:
            if self._data_driver_flag:
                if test.parent:
                    self.add_suite_tests(running.PTestSuite(test.parent))
                    self._data_driver_flag = False

            test_p = rb.running.PTestCase(test)
            run_mode = scheduler.TaskType.Foreground if self._debug else scheduler.TaskType.Synchron
            scheduler.Task(self.create_test_instance, test_p, self.version).run(run_mode)
        except Exception as e:
            f, li = get_error_info()
            logger.warn(f"Start test: {test.name} [Error: {e}; File: {f}:{li}]")
        finally:
            bg_logger.log_background_messages()

    def end_test(self, test: ETest, result: RTest):
        if not self.enabled_reporting:
            return
        try:
            test_p = rb.running.PTestCase(test)
            result_p = rb.running.PTestResult(result)
            run_mode = scheduler.TaskType.Foreground if self._debug else scheduler.TaskType.Synchron
            scheduler.Task(self.set_test_results, test_p, result_p).run(run_mode)
        except Exception as e:
            f, w = get_error_info()
            logger.warn(f"End test {test.name} [Error: {e}; File: {f}:{w}]")
        finally:
            bg_logger.log_background_messages()


__all__ = [
    'Listener'
]
