from __future__ import annotations

import re

from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
from robot.result import TestCase as RTestResult
from robot.running import TestSuite as RTestSuite, TestCase as RTestCase, Keyword as RKeyword

from robotframework_practitest.models.practi_test.data_formatters import practi_test_duration
from robotframework_practitest.models.robot.helpers import format_kw_list, get_name, formate_test_tags
from robotframework_practitest.models.robot.html_decoder import HTMLDecoder
from robotframework_practitest.utils.misc_utils import flat_lists

VARIABLE_REGEX = re.compile(r'([\$@&]{[a-zA-Z0-9_\-\s]+\})')


def convert(item: RTestSuite | RTestCase | RKeyword):
    return PTestSuite(item)


def get_parents_path(item: RTestSuite | RTestCase | RKeyword):
    result = []
    while item.parent:
        result.append(item.parent.name)
        item = item.parent
    result.reverse()
    return result


def extract_kw_results(results: RTestResult) -> dict:
    for kw_res in results.body:
        print(f"{kw_res}")
    return {}


def format_suite_test_description(item: PTestSuite | PTestCase):
    description = []
    if item.doc:
        description.append(f"{item.doc}")
    if item.has_setup:
        description.append("Setup:\n\t{}".format(format_kw_list([item.setup.name] + list(item.setup.args))))
    if item.has_teardown:
        teardown_kws = [item.teardown.name] + list(item.teardown.args)
        description.append("Teardown:\n\t{}".format(format_kw_list(teardown_kws)))
    return '\n'.join(description)


def extract_variables(*params):
    for pattern in params:
        variables = VARIABLE_REGEX.findall(pattern)
        if variables:
            for var_match in variables:
                try:
                    yield pattern.replace(var_match, BuiltIn().get_variable_value(var_match, var_match))
                except Exception as e:
                    logger.error(f"{e}")
        else:
            yield pattern


class PKeyword:
    def __init__(self, item: RKeyword):
        self.name = getattr(item, 'name', item.type)
        self.tags = tuple(*getattr(item, 'tags', ()))
        self.parent = get_parents_path(item)
        self.doc = getattr(item, 'doc', '')
        # self.args = tuple(extract_variables(*getattr(item, 'args', [])))
        self.args = getattr(item, 'args', ())
        self.teardown = PKeyword(item.teardown) if getattr(item, 'teardown', None) else None

    def __repr__(self):
        return f"{self.name}({self.args})"

    def __str__(self):
        return f"{self.name}({', '.join(self.args)})"

    @property
    def has_teardown(self):
        return self.teardown is not None


class PTestCase:
    def __init__(self, item: RTestCase, **kwargs):
        name_formatter = kwargs.get('name_formatter', None)
        self.name = item.name if name_formatter is None else name_formatter(item.name)
        self.tags = item.tags
        self.doc = item.doc
        self.parent = get_parents_path(item)
        self.template = getattr(item, 'template', None)
        self.setup = PKeyword(item.setup) if item.setup else None
        self.teardown = PKeyword(item.teardown) if item.teardown else None
        self.body = [PKeyword(k) for k in item.body]

    def __repr__(self):
        return f"{self.name}({self.body})"

    def __str__(self):
        return f"{self.name}({', '.join([f'{b}' for b in self.body])})"

    @property
    def all_tags(self):
        return self.tags, (k.tags for k in self.body)

    @property
    def has_setup(self):
        return self.setup is not None

    @property
    def has_teardown(self):
        return self.teardown is not None

    @property
    def steps(self):
        return [{'name': k.name, 'description': k.doc} for k in self.body]

    @property
    def pt_name(self):
        return get_name(self.name, *self.parent)

    def pt_tags(self, **test_tag_mapping):
        return formate_test_tags(*self.tags, **test_tag_mapping)

    @property
    def pt_description(self):
        return format_suite_test_description(self)


class PTestResult(PTestCase):
    def __init__(self, item: RTestResult):
        super().__init__(item)
        self.status = item.status + ('PED' if item.status == 'SKIP' else 'ED')
        self.starttime = item.starttime
        self.endtime = item.endtime
        self.elapsedtime = item.elapsedtime / 1000
        self.message = item.message

    @property
    def automated_execution_output(self):
        prefix = f"{self.status} " if self.status.startswith('SKIP') else ""
        with HTMLDecoder() as hd:
            hd.feed(self.message)
            return prefix + f"{hd}"

    @property
    def duration(self):
        return practi_test_duration(self.elapsedtime)

    def steps(self, *case_steps):
        result = []
        for k in case_steps:
            k.update(**{'status': self.status})
            result.append(dict(**{"name": k.get('name'), "expected-results": self.status}))
        return result

    @property
    def exit_code(self):
        return 0 if self.status in ('PASSED', 'SKIPPED') else 1


class PTestSuite:
    def __init__(self, item: RTestSuite, **kwargs):
        self.name = item.name
        self.doc = item.doc
        self.parent = get_parents_path(item)
        self.tests = [PTestCase(t, **kwargs) for t in item.tests]
        self.suites = [PTestSuite(s) for s in item.suites]
        self.setup = PKeyword(item.setup) if item.setup else None
        self.teardown = PKeyword(item.teardown) if item.teardown else None

    @property
    def is_data_driver(self) -> bool:
        return len(self.tests) == 1 and self.tests[0].template is not None

    @property
    def tags(self) -> list:
        return []

    def all_tags(self, exclusions: list = [], exclude_prefix: list = []):
        return flat_lists(exclusions, exclude_prefix, [s.all_tags(exclusions, exclude_prefix)
                                                       for s in self.suites], [t.all_tags for t in self.tests])

    def all_tests(self, attr=None):
        for suite in self.suites:
            if suite.is_data_driver:
                continue
            for test in suite.all_tests(attr):
                yield test
        for test in self.tests:
            yield getattr(test, attr) if attr else test

    @property
    def tests_count(self):
        return sum([s.tests_count for s in self.suites]) + len(self.tests)

    @property
    def has_setup(self):
        return self.setup is not None

    @property
    def has_teardown(self):
        return self.teardown is not None

    def __str__(self):
        return self.name
