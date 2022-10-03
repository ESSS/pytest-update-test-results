from pathlib import Path
from typing import Dict

from _pytest.reports import TestReport

from src.pytest_merge_xml.merge_xml import modify_xml


class XMLReport:

    def __init__(self, original_xmlfile: Path):
        self.reports: Dict[TestReport] = {}
        self.original_xmlfile = original_xmlfile

    def pytest_runtest_logreport(self, report):
        if report.when == "call":
            self.reports[report.nodeid] = report

    def pytest_sessionfinish(self, session, exitstatus):
        modify_xml(Path(self.original_xmlfile), self.reports, Path(f"{self.original_xmlfile}.ovrw"))


def pytest_addoption(parser):
    # pytest has a note to keep conftest.py at the root dir in order to load added options.
    # http://pytest.org/latest/plugins.html?highlight=hooks#plugin-discovery-order-at-tool-startup
    parser.addoption(
        "--mergexml",
        action="store",
        help="Enable original xml overwrite based on flaky tests rerun results",
    )


def pytest_configure(config):
    original_xmlfile = config.getoption("--mergexml")
    # report = XMLReport(Path('src/pytest_merge_xml/failure.xml'))
    report = XMLReport(Path(original_xmlfile))
    config.pluginmanager.register(report)
