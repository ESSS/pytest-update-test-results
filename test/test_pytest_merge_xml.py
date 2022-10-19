from pathlib import Path

from _pytest.reports import TestReport
from pytest_merge_xml.merge_xml import modify_xml
from pytest_regressions.file_regression import FileRegressionFixture


def test_xml_one_failed_two_passed(
    datadir: Path, file_regression: FileRegressionFixture
) -> None:
    """Tests modify_xml() with list of previously failing flaky test
    results that are now passing, and expects the xml to be overwritten
    with the new result."""
    #  'location', 'keywords', 'longrepr', and 'when'
    retest_results_passed = {
        "test_xml_one_failed_two_passed": TestReport(
            nodeid="test/test_pytest_merge_xml.py::test_xml_one_failed_two_passed",
            outcome="passed",
            location=(
                "test/test_pytest_merge_xml.py",
                9,
                "test_xml_one_failed_two_passed",
            ),
            keywords={},
            longrepr=None,
            when="call",
        ),
        "test_xml_two_failed_one_passed": TestReport(
            nodeid="test/test_pytest_merge_xml.py::test_xml_two_failed_one_passed",
            outcome="passed",
            location=(
                "test/test_pytest_merge_xml.py",
                49,
                "test_xml_two_failed_one_passed",
            ),
            keywords="",
            longrepr=None,
            when="call",
        ),
        "test_xml_three_failed_zero_passed": TestReport(
            nodeid="test/test_pytest_merge_xml.py::test_xml_three_failed_zero_passed",
            outcome="failed",
            location=(
                "test/test_pytest_merge_xml.py",
                88,
                "test_xml_three_failed_zero_passed",
            ),
            keywords="",
            longrepr=None,
            when="call",
        ),
    }
    obtained_file = datadir / "failure_tmp.xml"
    modify_xml(Path(datadir / "failure.xml"), retest_results_passed, obtained_file)
    file_regression.check(obtained_file.read_text(), extension=".xml")


def test_xml_two_failed_one_passed(
    datadir: Path, file_regression: FileRegressionFixture
) -> None:
    """Tests modify_xml() with list of flaky test results, with some
    still not passing, and expects the xml to be overwritten for the
    passing tests."""
    retest_results_some_passing = {
        "test_xml_one_failed_two_passed": TestReport(
            nodeid="test/test_pytest_merge_xml.py::test_xml_one_failed_two_passed",
            outcome="failed",
            location=(
                "test/test_pytest_merge_xml.py",
                9,
                "test_xml_one_failed_two_passed",
            ),
            keywords={},
            longrepr=None,
            when="call",
        ),
        "test_xml_two_failed_one_passed": TestReport(
            nodeid="test/test_pytest_merge_xml.py::test_xml_two_failed_one_passed",
            outcome="passed",
            location=(
                "test/test_pytest_merge_xml.py",
                49,
                "test_xml_two_failed_one_passed",
            ),
            keywords="",
            longrepr=None,
            when="call",
        ),
        "test_xml_three_failed_zero_passed": TestReport(
            nodeid="test/test_pytest_merge_xml.py::test_xml_three_failed_zero_passed",
            outcome="failed",
            location=(
                "test/test_pytest_merge_xml.py",
                88,
                "test_xml_three_failed_zero_passed",
            ),
            keywords="",
            longrepr=None,
            when="call",
        ),
    }
    obtained_file = datadir / "failure_tmp.xml"
    modify_xml(
        Path(datadir / "failure.xml"), retest_results_some_passing, obtained_file
    )
    file_regression.check(obtained_file.read_text(), extension=".xml")


def test_xml_three_failed_zero_passed(
    datadir: Path, file_regression: FileRegressionFixture
) -> None:
    """Tests modify_xml() with list of flaky test results, with some
    still not passing, and expects the xml to be overwritten for the
    passing tests."""
    retest_results_mix = {
        "test_xml_one_failed_two_passed": TestReport(
            nodeid="test/test_pytest_merge_xml.py::test_xml_one_failed_two_passed",
            outcome="failed",
            location=(
                "test/test_pytest_merge_xml.py",
                9,
                "test_xml_one_failed_two_passed",
            ),
            keywords={},
            longrepr=None,
            when="call",
        ),
        "test_xml_two_failed_one_passed": TestReport(
            nodeid="test/test_pytest_merge_xml.py::test_xml_two_failed_one_passed",
            outcome="failed",
            location=(
                "test/test_pytest_merge_xml.py",
                49,
                "test_xml_two_failed_one_passed",
            ),
            keywords="",
            longrepr=None,
            when="call",
        ),
        "test_xml_three_failed_zero_passed": TestReport(
            nodeid="test/test_pytest_merge_xml.py::test_xml_three_failed_zero_passed",
            outcome="failed",
            location=(
                "test/test_pytest_merge_xml.py",
                88,
                "test_xml_three_failed_zero_passed",
            ),
            keywords="",
            longrepr=None,
            when="call",
        ),
    }
    obtained_file = datadir / "failure_tmp.xml"
    modify_xml(Path(datadir / "failure.xml"), retest_results_mix, obtained_file)
    file_regression.check(obtained_file.read_text(), extension=".xml")
