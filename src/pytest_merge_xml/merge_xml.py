import xml.etree.ElementTree as Et
from pathlib import Path
from typing import Dict

from _pytest.reports import TestReport


def modify_xml(original_xml: Path, retest_results: Dict[str, TestReport], new_xml: Path) -> None:
    tree = Et.parse(original_xml)
    root = tree.getroot()
    testsuite = root.find("testsuite")
    failure_count = int(testsuite.attrib['failures'])

    results_passed = [
        result.location[2] for result in retest_results.values() if result.outcome == 'passed'
    ]

    for testcase in testsuite:
        testcase_name = testcase.attrib['name']  # 'test_xml_one_failed_two_passed'
        for failure in testcase.findall("failure"):
            print(testcase_name, results_passed)
            if testcase_name in results_passed:
                failure_count -= 1
                testcase.remove(failure)

    testsuite.attrib['failures'] = str(failure_count)
    tree.write(new_xml, encoding='utf-8', xml_declaration=True)
