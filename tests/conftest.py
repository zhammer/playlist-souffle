import pytest

HAMMER_EMOJI = '\U0001f528 '

def pytest_addoption(parser):
    """Turn on hammertime pytest display with --hammertime."""
    group = parser.getgroup('hammertime')
    group.addoption('--hammertime', action='store_true',
                    help='display "{}" instead of "." for passed tests'.format(HAMMER_EMOJI))

def pytest_report_teststatus(report):
    """Turn '.' success char into hammer emoji."""
    if pytest.config.getoption('hammertime'):
        if report.when == 'call' and report.outcome == 'passed':
            return (report.outcome, HAMMER_EMOJI, 'PASSED')
