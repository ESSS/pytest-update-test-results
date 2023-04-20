from pathlib import Path
from xml.etree import ElementTree as ET

from _pytest.reports import TestReport
from pytest_regressions.file_regression import FileRegressionFixture
from pytest_update_test_results.update_test_results import modify_xml


def test_one_failure(datadir: Path) -> None:
    retest_results = {
        "test_one_failure": TestReport(
            nodeid="test/test_flaky.py::test_one_failure_passed",
            outcome="passed",
            location=("test/test_pytest_merge_xml.py", 16, "test_one_failure_passed"),
            keywords={},
            longrepr=None,
            when="call",
        )
    }

    modified_file = datadir / "one_failure.retest.xml"
    modify_xml(Path(datadir / "one_failure.xml"), retest_results, modified_file)

    et = ET.parse(modified_file)
    root_el = et.getroot()
    testsuite_el = root_el.find("testsuite")
    assert testsuite_el.attrib["failures"] == "0"
    assert len(list(testsuite_el.iter("failure"))) == 0


def test_two_failures(datadir: Path) -> None:
    retest_results_passed = {
        "test_xml_one_failed_two_passed": TestReport(
            nodeid="test/test_flaky.py::first_test_passed",
            outcome="passed",
            location=("test/test_flaky.py", 8, "first_test_passed"),
            keywords={},
            longrepr=None,
            when="call",
        ),
        "second_test_passed": TestReport(
            nodeid="test/test_flaky.py::second_test_passed",
            outcome="passed",
            location=("test/test_flaky.py", 16, "second_test_passed"),
            keywords={},
            longrepr=None,
            when="call",
        ),
        "third_test_failed": TestReport(
            nodeid="test/test_flaky.py::third_test_failed",
            outcome="failed",
            location=("test/test_flaky.py", 48, "third_test_failed"),
            keywords={},
            longrepr=None,
            when="call",
        ),
    }
    modified_file = datadir / "two_failures.retest.xml"
    modify_xml(Path(datadir / "two_failures.xml"), retest_results_passed, modified_file)

    root_el = ET.parse(modified_file).getroot()
    testsuite_el = root_el.find("testsuite")
    assert testsuite_el.attrib["failures"] == "1"

    testcases = testsuite_el.findall("testcase")
    assert testcases[1].find("failure") is None
    assert testcases[2].find("failure") is not None


def test_one_failure_one_error(datadir: Path) -> None:
    """Tests modify_xml() with that change an XML with one failure and one error"""
    retest_results_passed = {
        "test_failure_passed": TestReport(
            nodeid="test/test_flaky.py::test_failure_passed",
            outcome="passed",
            location=("test/test_flaky.py", 8, "test_failure_passed"),
            keywords={},
            longrepr=None,
            when="call",
        ),
        "test_error_passed": TestReport(
            nodeid="test/test_flaky.py::test_error_passed",
            outcome="passed",
            location=("test/test_flaky.py", 16, "test_error_passed"),
            keywords={},
            longrepr=None,
            when="call",
        ),
    }
    modified_file = datadir / "one_failure_one_error.retest.xml"
    modify_xml(
        Path(datadir / "one_failure_one_error.xml"),
        retest_results_passed,
        modified_file,
    )

    root_el = ET.parse(modified_file).getroot()
    testsuite_el = root_el.find("testsuite")
    assert testsuite_el.attrib["failures"] == "0"
    assert testsuite_el.attrib["errors"] == "0"
    assert len(list(testsuite_el.iter("failure"))) == 0
    assert len(list(testsuite_el.iter("error"))) == 0


def test_succeed_to_failure_on_retest_not_supported(datadir: Path) -> None:
    """
    For now, pytest-update-test-results is supposed to always run with `--last-failed` flag.

    It converts failed outcomes into passed, but DOES NOT convert passed test cases into
    failed ones (that could happen if `--update-xml` runs without `--last-failed`).
    """
    retest_results_mix = {
        "test_xml_first_retest_failed": TestReport(
            nodeid="test/test_flaky.py::test_xml_first_retest_failed",
            outcome="failed",
            location=("test/test_flaky.py", 8, "test_xml_first_retest_failed"),
            keywords={},
            longrepr=None,
            when="call",
        ),
        "test_xml_second_retest_failed": TestReport(
            nodeid="test/test_flaky.py::test_xml_second_retest_failed",
            outcome="failed",
            location=("test/test_flaky.py", 16, "test_xml_second_retest_failed"),
            keywords={},
            longrepr=None,
            when="call",
        ),
    }
    modified_file = datadir / "all_failed.retest.xml"
    modify_xml(Path(datadir / "no_failures.xml"), retest_results_mix, modified_file)

    root_el = ET.parse(modified_file).getroot()
    testsuite_el = root_el.find("testsuite")

    assert testsuite_el.attrib["failures"] == "0"


def test_failure_using_unittest_style(datadir: Path) -> None:
    retest_results = {
        "test_xml_failure_unittest_style": TestReport(
            nodeid="test/test_flaky.py::Test::test_xml_failure_unittest_style",
            outcome="passed",
            location=("test/test_flaky.py", 8, "Test.test_xml_failure_unittest_style"),
            keywords={},
            longrepr=None,
            when="call",
        )
    }

    modified_file = datadir / "one_failure_unittest_style.retest.xml"
    modify_xml(Path(datadir / "one_failure_unittest_style.xml"), retest_results, modified_file)

    et = ET.parse(modified_file)
    root_el = et.getroot()
    testsuite_el = root_el.find("testsuite")
    assert testsuite_el.attrib["failures"] == "0"
    assert len(list(testsuite_el.iter("failure"))) == 0


def test_duplicated_test_names(datadir: Path) -> None:
    retest_results = {
        "test_duplicated_test_names": TestReport(
            nodeid="test/test_flaky.py::Test::test_duplicated_test_names",
            outcome="passed",
            location=("test/test_flaky.py", 8, "Test.test_duplicated_test_names"),
            keywords={},
            longrepr=None,
            when="call",
        )
    }

    modified_file = datadir / "one_failure_duplicated_names.retest.xml"
    modify_xml(Path(datadir / "one_failure_duplicated_names.xml"), retest_results, modified_file)

    et = ET.parse(modified_file)
    root_el = et.getroot()
    testsuite_el = root_el.find("testsuite")
    assert testsuite_el.attrib["failures"] == "0"
    assert len(list(testsuite_el.iter("failure"))) == 0
