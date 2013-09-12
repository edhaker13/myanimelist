from __future__ import unicode_literals, division, absolute_import
import logging
from tests import FlexGetBase
from nose.plugins.attrib import attr


__author__ = 'edhaker13'

log = logging.getLogger('TestSearchMyAnimeList')


class TestSearchMyAnimeList(FlexGetBase):
    __yaml__ = """
        tasks:
          test:
            search_myanimelist: Free!
          test_list:
            search_myanimelist:
              - Free!
              - Clannad Movie
    """

    def _assert_entry(self, entry, values):
        keys = {'mal_id', 'title', 'description', 'mal_type', 'mal_episodes', 'mal_image_url', 'url'}
        for key in keys:
            entry_value = entry.get(key)
            input_value = values.get(key)

            assert entry_value == input_value

            log.info('Entry[%s]: %r == %r' % (key, entry_value, input_value))

    @attr(online=True)
    def test_simple(self):
        self.execute_task('test')
        entry0 = self.task.entries[0]
        values0 = {
            'mal_id': 18507,
            'title': 'Free!',
            'description': 'The story revolves around Haruka Nanase, a boy who has always loved to be immersed in water'
                           ', and to swim in it. Before graduating from elementary school, he participated in a '
                           'swimming tournament along...',
            'mal_type': 'TV',
            'mal_image_url': 'http://cdn.myanimelist.net/images/anime/6/51107.jpg',
            'mal_episodes': 12,
            'url': 'http://myanimelist.net/anime/18507',
            'mal_url': 'http://myanimelist.net/anime/18507'
        }
        self._assert_entry(entry0, values0)
        entry1 = self.task.entries[1]
        values1 = {
            'mal_id': 19671,
            'title': 'Free! Specials',
            'description': 'Specials bundled with the DVD/BDs.',
            'mal_type': 'Special',
            'mal_image_url': 'http://cdn.myanimelist.net/images/anime/3/53643.jpg',
            'mal_episodes': 0,
            'url': 'http://myanimelist.net/anime/19671',
            'mal_url': 'http://myanimelist.net/anime/19671'
        }
        self._assert_entry(entry1, values1)

    @attr(online=True)
    def test_list(self):
        self.execute_task('test_list')
        entry0 = self.task.entries[0]
        values0 = {
            'mal_id': 18507,
            'title': 'Free!',
            'description': 'The story revolves around Haruka Nanase, a boy who has always loved to be immersed in water'
                           ', and to swim in it. Before graduating from elementary school, he participated in a '
                           'swimming tournament along...',
            'mal_type': 'TV',
            'mal_image_url': 'http://cdn.myanimelist.net/images/anime/6/51107.jpg',
            'mal_episodes': 12,
            'url': 'http://myanimelist.net/anime/18507',
            'mal_url': 'http://myanimelist.net/anime/18507'
        }
        self._assert_entry(entry0, values0)
        entry1 = self.task.entries[1]
        values1 = {
            'mal_id': 19671,
            'title': 'Free! Specials',
            'description': 'Specials bundled with the DVD/BDs.',
            'mal_type': 'Special',
            'mal_image_url': 'http://cdn.myanimelist.net/images/anime/3/53643.jpg',
            'mal_episodes': 0,
            'url': 'http://myanimelist.net/anime/19671',
            'mal_url': 'http://myanimelist.net/anime/19671'
        }
        self._assert_entry(entry1, values1)
        entry2 = self.task.entries[2]
        values2 = {
            'mal_id': 1723,
            'title': 'Clannad Movie',
            'description': 'Clannad is set in a high-school located in some Japanese town. Okazaki Tomoya is a '
                           'third-year student who doesn\'t take his studies seriously. Always late for class, '
                           'he\'s seen as a delinquent by the rest of his classmates who are busy preparing for '
                           'their entrance examinations. Needless to say, he hasn\'t too many close friends '
                           'either.<br><br>\nTomoya seems not to mind too - until one day he meets a girl, '
                           'Furukawa Nagisa, who is left alone without friends on this school, because everybody '
                           'she knew already graduated. What a clumsy girl, he thinks at first. But he can\'t leave '
                           'her alone and so, while helping her, he meets a few other girls from his school. Although '
                           'he doesn\'t care much about them at first, he soon opens his heart to them as they get '
                           'to know each other better.<br><br>\n(Source: AniDB)',
            'mal_type': 'Movie',
            'mal_image_url': 'http://cdn.myanimelist.net/images/anime/6/7643.jpg',
            'mal_episodes': 1,
            'url': 'http://myanimelist.net/anime/1723',
            'mal_url': 'http://myanimelist.net/anime/1723'
        }
        self._assert_entry(entry2, values2)