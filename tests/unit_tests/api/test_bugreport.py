import json

from faf.api import BugReportSchema
from faf.domain.bugs import BugReport, BugReportTarget


def test_serializes():
    target = BugReportTarget('FAForever/api', url='http://github.com/FAForever/api', ref='develop')
    report = BugReport('Sample bug',
                       target=target,
                       description='API lacks implementation of bug reports',
                       traceback='Some traceback')

    schema = BugReportSchema()
    result, errors = schema.dump(report)
    assert not errors


def test_deserializes():
    with open('tests/data/bugs/bugreport.json') as f:
        data = json.loads(f.read())
    schema = BugReportSchema()
    result, errors = schema.load(data)
    assert result['title'] == 'Sample bug'
    assert result['target']['ref'] == 'develop'
