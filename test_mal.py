from __future__ import unicode_literals, division, absolute_import
from tests import FlexGetBase
from nose.plugins.attrib import attr

class TestMAL(FlexGetBase):
    
    __yaml__ = """
        tasks:
          test:
            myanimelist:
              username: edhaker13
              list: plan to watch   # our plugin
    """
    @attr(online=True)
    def test_input(self):
        # run the task
        self.execute_task('test')
        assert False, 'incomplete tests' # causes test to fail and log to be displayed
        #assert entry['title']='Neon Genesis Evangelion The End of Evangelion'
        