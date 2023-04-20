import shutil
import xml.etree.ElementTree as Et
from pathlib import Path
from typing import Dict

from _pytest.reports import TestReport
from dataclasses import dataclass


def modify_xml(original_xml: Path, retest_results: Dict[str, TestReport], new_xml: Path) -> None:
    """
    Modifies an XML file containing test results by removing failed test cases that were subsequently
    passed in a retest.

    :param original_xml: Path to the original XML file containing test results.
    :param retest_results: A dictionary mapping test cases to their retest results.
    :param new_xml: The path to the new modified XML file that will be created.
    :return: None. The modified XML file is written to the specified `new_xml` path.
    """

    tree = Et.parse(original_xml)
    root = tree.getroot()
    testsuite = root.find("testsuite")
    original_failure_count = retest_failure_count = int(testsuite.attrib["failures"])
    original_error_count = retest_error_count = int(testsuite.attrib["errors"])

    # test_uid = nodeid => classname + name do xml
    succeed_in_retest = {
        TestUid.from_nodeid(report.nodeid) for report in retest_results.values() if report.outcome == "passed"
    }

    for testcase in testsuite:
        testcase_identifier = TestUid(testcase.attrib["classname"], testcase.attrib["name"])
        if testcase_identifier in succeed_in_retest:
            failure = testcase.find("failure")
            if failure is not None:
                retest_failure_count -= 1
                testcase.remove(failure)
                continue
            error = testcase.find("error")
            if error is not None:
                retest_error_count -= 1
                testcase.remove(error)

    # Only writes a new XML if some test outcome has changed
    if retest_failure_count < original_failure_count or retest_error_count < original_error_count:
        testsuite.attrib["failures"] = str(retest_failure_count)
        testsuite.attrib["errors"] = str(retest_error_count)
        tree.write(new_xml, encoding="utf-8", xml_declaration=True)
    elif original_xml != new_xml:
        shutil.copy(original_xml, new_xml)


@dataclass(frozen=True)
class TestUid:
    classname: str
    testname: str

    @classmethod
    def from_nodeid(cls, test_nodeid) -> "TestUid":
        """
        Converts a TestReport nodeid to a unique identifier for a test case, and returns a tuple containing
        the UID and the test name. This is required because there is no direct way to map a `TestReport`
        object to a jUnit XML entry.

        :param nodeid: A TestReport nodeid string, typically in the format: "path/to/test_file.py::TestClass::test_name".
        :return: A tuple containing the UID and the test name. The UID will be in the format:
                 "path.to.test_file.TestClass" if there's a class, or "path.to.test_file" if not.
        """
        test_filepath_uid, test_name = test_nodeid.rsplit("::", 1)

        if "::" in test_filepath_uid:
            test_filepath_uid, class_name = test_filepath_uid.split("::")
        else:
            class_name = ""

        test_filepath_without_ext = Path(test_filepath_uid).with_suffix('')
        test_name_with_dots = ".".join(test_filepath_without_ext.parts)

        test_uid = f"{test_name_with_dots}.{class_name}" if class_name else test_name_with_dots

        return TestUid(test_uid, test_name)
