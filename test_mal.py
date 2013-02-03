from __future__ import unicode_literals, division, absolute_import
from tests import FlexGetBase


class TestMAL(FlexGetBase):
    
    __yaml__ = """
        tasks:
          test:
            mock:                 # let's use this plugin to create test data
              - {title: 'foobar'} # we can omit url if we do not care about it, in this case mock will add random url
            import_series:
                from:
                    myanimelist:
                        username: edhaker13   # our plugin
    """
    
    def test_feature(self):
        # run the task
        self.execute_task('test')
        assert False, 'incomplete tests' # causes test to fail and log to be displayed