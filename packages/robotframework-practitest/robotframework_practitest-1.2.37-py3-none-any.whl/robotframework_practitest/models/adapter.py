from __future__ import annotations

import os.path
import re
from copy import deepcopy
from threading import currentThread

from robot.libraries.BuiltIn import BuiltIn

from robotframework_practitest.models.data_mapper import TestStates, DataStatistics, TestStatuses
from robotframework_practitest.models.practi_test import PtClient
from robotframework_practitest.models.practi_test.data_formatters import *
from robotframework_practitest.models.robot.helpers import PT_MANAGED_ITEMS, get_related_test_display_ids, \
    update_variable_scope_from_tags, FIELD_UPDATE, formate_test_tags, \
    get_name, TEST_ALLOWED_CREATE_ATTEMPTS
from robotframework_practitest.models.robot.running import PTestResult, PTestCase, PTestSuite, \
    format_suite_test_description
from robotframework_practitest.services import data_queue as data
from robotframework_practitest.services.configuration import WAIT_FOR_TEST_CREATED
from robotframework_practitest.utils.logger import LOGGER as logger
from robotframework_practitest.utils.misc_utils import get_error_info, write_to_temp_file


MISSED_TEST_IDs = []


def convert_test_display_to_id(client, *tags, **tag_mapping):
    kwargs = {'enforce_result': True, 'timeout': 3}
    related_test_display_ids = get_related_test_display_ids(*tags, **tag_mapping)
    result_test_ids = []
    for display_id in related_test_display_ids:
        try:
            kwargs.update(**{'formatter': filter_test_by_display_id(display_id), 'display-ids': display_id})
            test_d = client.query_test(**kwargs)
            assert test_d
            result_test_ids.append(test_d)
        except Exception as e:
            global MISSED_TEST_IDs
            MISSED_TEST_IDs.append(display_id)
    return result_test_ids


class RobotToPractiTest_Adapter(DataStatistics):
    def __init__(self):
        super().__init__()
        self._client: PtClient = None
        self.fields_map = None
        self.instances_type = None
        self.test_set_hash_tag = None
        self.test_info_fields = {}
        self.test_tag_mapping = {}
        self.test_set_info_fields = {}
        self._involved_tags = []
        self._current_suite_cache = {}
        self.enabled_reporting = False

    def init_adapter(self, client: PtClient, *fields, **types):
        self._client = client
        self.fields_map = fields
        self.instances_type = types
        self.test_info_fields = self.get_variable_scope_for(PT_MANAGED_ITEMS.Test)
        self.test_set_info_fields = self.get_variable_scope_for(PT_MANAGED_ITEMS.TestSet)

    def _add_involved_tags(self, *tags):
        for tag in tags:
            if tag not in self._involved_tags:
                self._involved_tags.append(tag)

    @property
    def involved_tags(self) -> set:
        return set(self._involved_tags)

    @property
    def project_id(self):
        return self._client.project_id

    def get_active_test_set_id(self, timeout=None):
        timeout = timeout or data.DEFAULT_ITEM_WAIT
        timeout += self._client.active_timeout
        return data.DataQueueService().wait(data.CacheItem(self._client.test_set_tag, self.test_set_hash_tag),
                                            timeout)

    def get_field_mapping(self, item):
        for field in self.fields_map:
            if field.get('id') == item:
                return field.get('name', item), field.get('variable', None), field.get('default', None), field.get(
                    'map', None)

        raise AttributeError(f"Item '{item}"' not resolved in Fields Map')

    def get_variable_scope_for(self, area_name: PT_MANAGED_ITEMS):
        assert currentThread().name == 'MainThread', "This method can run in main thread only; Check yor code"
        result = {}
        for item in self.instances_type.get(area_name.name):
            try:
                name, variable, default, map_ = self.get_field_mapping(item)
                if map_:
                    value = FIELD_UPDATE.get(map_.upper(), None), default
                else:
                    value = BuiltIn().get_variable_value(f"${variable}", default) if variable else default
                assert value is not None, \
                    f"Cannot occur value for Field: {name}: Variable{variable}; Default: {default}; Callback: {map_}"
                result[name] = value
            except AssertionError as e:
                logger.warn(f"Error in {area_name.name} field '{item}': {e}")
            except Exception as e:
                logger.error(f"Error in {area_name.name} field '{item}': {e}")
        return result

    def start_test_set(self, suite: PTestSuite, version, **kwargs):
        name = ''
        try:
            name = get_name(suite.name, *suite.parent, **kwargs)
            involved_tags = set(suite.all_tags(exclude_prefix=[tag.get('prefix', None)
                                                               for tag in self.test_tag_mapping.values()
                                                               if tag.get('prefix', None)]))
            test_set_info = dict(update_variable_scope_from_tags(self.test_tag_mapping, *involved_tags,
                                                                 **deepcopy(self.test_set_info_fields)))
            test_set_formatter = lambda data_: dict(id=data_['data']['id'],
                                                    display_id=data_['data']['attributes']['display-id'],
                                                    set_name=data_['data']['attributes']['name'],
                                                    )
            self.test_set_hash_tag = self._client.create_test_set(name,
                                                                  version=version,
                                                                  formatter=test_set_formatter,
                                                                  ignore_cache=True,
                                                                  **test_set_info)
            post_process_cb = kwargs.get('post_process', None)
            if post_process_cb:
                post_process_cb()
        except Exception as e:
            f, w = get_error_info()
            logger.error(f"PractiTest start_test_set: Cannot create TestSet '{name}'; Error: {e}; File: {f}:{w}")
            self.enabled_reporting = False
            raise

    # Bulk test data creation
    def create_test_set_recursively(self, suite: PTestSuite, version, **kwargs):

        test_set_info = self.get_variable_scope_for(PT_MANAGED_ITEMS.TestSet)
        self.test_set_hash_tag = self._client.create_test_set(
            get_name(suite.name, *suite.parent, **kwargs), version=version,
            formatter=lambda data: data['data']['id'], enforce_result=True, **test_set_info)

        test_info = self.get_variable_scope_for(PT_MANAGED_ITEMS.Test)
        self._recursive_test_create(suite, version, **test_info)

    def _recursive_test_create(self, suite: PTestSuite, version, **test_info):
        try:
            for test in suite.tests:
                self.create_test_instance(test, version)

            for sub_suite in suite.suites:
                self._recursive_test_create(sub_suite, version, **test_info)
        except Exception as e:
            f, w = get_error_info()
            logger.error(f"Recursive test creation failed: {e}; File: {f}:{w}")
            raise

    def create_test_instance(self, test: PTestCase, version):
        parent_path = test.parent
        test_name = get_name(test.name, *parent_path)
        test_info = dict(update_variable_scope_from_tags(self.test_tag_mapping,
                                                         *test.tags, **deepcopy(self.test_info_fields)))
        test_data = self._get_or_create_test(test, version, *parent_path, **test_info)
        test_id = test_data['id']
        related_tests_list = convert_test_display_to_id(self._client, *test.tags, **self.test_tag_mapping)
        full_tests_list = set([test_id] + related_tests_list)
        instance_list = []

        test_set_id = self.get_active_test_set_id(self._client.active_timeout).get('id')

        for id_ in full_tests_list:
            try:
                hash_tag = f"{test_set_id}_{id_}"
                self._client.create_test_instance(test_set_id, id_, version, hash_tag=hash_tag,
                                                  formatter=lambda d: d['data']['id'])
                self.set_test(TestStates.PractiTest, test_name, TestStatuses.Pending)
                instance_list.append(hash_tag)
                logger.console(f"Test '{test_name}': Run Instance created (Hash: {hash_tag})")
            except Exception as e:
                f, w = get_error_info()
                logger.error(
                    f"PractiTest create_test_instance: "
                    f"Cannot add '{test_name}' (Test#{id_}) to TestSet ({self.test_set_hash_tag}) "
                    f"[Error: {e}; File: {f}:{w}]"
                )
        data.DataQueueService()[data.CacheItem('run_instances', test_name)] = set(instance_list)

    def _get_or_create_test(self, test: PTestCase, version, *path, **test_info):
        test_name = get_name(test.name, *path)
        attempts = 0
        while True:
            test_data = self._client.query_test(name_exact=test_name, ignore_cache=True, enforce_result=True,
                                                formatter=filter_test_by_name(test_name), timeout=5)
            if test_data:
                logger.info(f"Test {test_name} already existing")
                return test_data
            try:
                assert attempts <= TEST_ALLOWED_CREATE_ATTEMPTS, \
                    f"Cannot get or create test '{test.name}' during {attempts} attempts"
                description = format_suite_test_description(test)
                robot_tags, custom_fields = formate_test_tags(*test.tags, **self.test_tag_mapping)
                custom_fields.update(**test_info)
                robot_tags.extend(self.test_tag_mapping.get('AUTO', {}).get('tags', []))
                self._add_involved_tags(*robot_tags)
                self._client.create_test_case(test_name, version=version, description=description,
                                              steps=test.steps, ignore_cache=True, **custom_fields)
                logger.console(f"Test {test_name} created successfully")
            except AssertionError as e:
                logger.error(e)
                raise
            except Exception as e:
                logger.error(f"Error creating test '{test_name}': {e}")
                raise
            finally:
                attempts += 1

    def set_test_results(self, test: PTestCase, results: PTestResult):
        try:
            test_name = get_name(test.name, *test.parent)
            related_test_list = data.DataQueueService().wait(data.CacheItem('run_instances', test_name),
                                                             WAIT_FOR_TEST_CREATED)
            logger.info(f"Result: {results.name}; {results.status}; Duration: {results.duration}")
            for index, instance in enumerate(related_test_list):
                try:
                    set_id, test_id = instance.split('_', 1)
                    instance_id = data.DataQueueService().wait(data.CacheItem(self._client.instance_tag, instance))
                    files = []
                    if len(results.automated_execution_output) > 255:
                        file_path = write_to_temp_file(results.automated_execution_output,
                                                       name=re.sub(r'\\|\/|\s+', '_', test.name),
                                                       suffix=f"{instance_id}.txt")
                        file_name = os.path.basename(file_path)
                        files.append(file_path)
                        automated_execution_output = f"Output redirected to file: {file_name}"
                    else:
                        automated_execution_output = results.automated_execution_output

                    self._client.create_run(instance_id, results.exit_code, results.duration,
                                            automated_execution_output, files=files)
                    logger.console(
                        f"PractiTest Reporter: {'Robot' if index == 0 else 'Referenced'} Test '{test_name}' "
                        f"completed: {results.status} (TestSet: {set_id}, Test: {test_id}, Instance {instance_id})")
                except Exception as e:
                    logger.error(f"PractiTest Reporter: Error report result for test '{test_name}': {e}")
                else:
                    self.set_test(TestStates.Status, test_name, TestStatuses[results.status])
        except Exception as e:
            f, w = get_error_info()
            logger.error(f"PractiTest set_test_results {test.name} [Error: {e}; File: {f}:{w}]")
            raise

