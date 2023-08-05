"""
Definition of the tests for the EmojiStag module
"""
from scistag.tests.visual_test_log_scistag import VisualTestLogSciStag

test_log = VisualTestLogSciStag(test_filename=__file__)
vl = test_log.default_builder


def teardown_module(_):
    """
    Finalize the test
    """
    test_log.finalize()
