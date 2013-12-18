from __future__ import unicode_literals, division, absolute_import
import logging
from nose.plugins.attrib import attr
from tests import FlexGetBase

__author__ = 'edhaker13'

log = logging.getLogger('TestMyAnimeList')


class TestMyAnimeList(FlexGetBase):
    __yaml__ = """
        tasks:
          test_default:
            myanimelist: flexget
          test_partial:
            myanimelist:
              username: flexget
          test_watching:
            myanimelist:
              username: flexget
              list: watching
          test_plantowatch:
            myanimelist:
              username: flexget
              list: plan to watch
          test_completed:
            myanimelist:
              username: flexget
              list: completed
          test_onhold:
            myanimelist:
             username: flexget
             list: on-hold
          test_dropped:
            myanimelist:
             username: flexget
             list: dropped
    """

    def _assert_entry(self, entry, values):
        keys = {'mal_id', 'title', 'mal_type', 'mal_image_url', 'mal_episodes', 'mal_status', 'mal_my_score',
                'mal_my_status', 'url', 'mal_url'}
        for key in keys:
            entry_value = entry.get(key)
            input_value = values.get(key)

            assert entry_value == input_value

            log.info('Entry[%s]: %r == %r' % (key, entry_value, input_value))

    @attr(online=True)
    def test_default(self):
        self.execute_task('test_default')
        log.debug('List of entries: %s' % [e['title'] for e in self.task.entries])
        entry0 = self.task.entries[0]
        values0 = {
            'mal_id': '9253',
            'title': 'Steins;Gate',
            'mal_type': 'TV',
            'mal_image_url': 'http://cdn.myanimelist.net/images/anime/11/41011.jpg',
            'mal_episodes': '24',
            'mal_status': 'finished airing',
            'mal_my_score': '0',
            'mal_my_status': 'watching',
            'url': 'http://myanimelist.net/anime/9253',
            'mal_url': 'http://myanimelist.net/anime/9253'
        }
        self._assert_entry(entry0, values0)

        entry1 = self.task.entries[1]
        values1 = {
            'mal_id': '18507',
            'title': 'Free!',
            'mal_type': 'TV',
            'mal_image_url': 'http://cdn.myanimelist.net/images/anime/6/51107.jpg',
            'mal_episodes': '12',
            'mal_status': 'finished airing',
            'mal_my_score': '7',
            'mal_my_status': 'watching',
            'url': 'http://myanimelist.net/anime/18507',
            'mal_url': 'http://myanimelist.net/anime/18507',
        }
        self._assert_entry(entry1, values1)
        log.debug('Default test completed succesfully')

    @attr(online=True)
    def test_partial(self):
        self.execute_task('test_partial')
        log.debug('List of entries: %s' % [e['title'] for e in self.task.entries])
        entry0 = self.task.entries[0]
        values0 = {
            'mal_id': '9253',
            'title': 'Steins;Gate',
            'mal_type': 'TV',
            'mal_image_url': 'http://cdn.myanimelist.net/images/anime/11/41011.jpg',
            'mal_episodes': '24',
            'mal_status': 'finished airing',
            'mal_my_score': '0',
            'mal_my_status': 'watching',
            'url': 'http://myanimelist.net/anime/9253',
            'mal_url': 'http://myanimelist.net/anime/9253'
        }
        self._assert_entry(entry0, values0)

        entry1 = self.task.entries[1]
        values1 = {
            'mal_id': '18507',
            'title': 'Free!',
            'mal_type': 'TV',
            'mal_image_url': 'http://cdn.myanimelist.net/images/anime/6/51107.jpg',
            'mal_episodes': '12',
            'mal_status': 'finished airing',
            'mal_my_score': '7',
            'mal_my_status': 'watching',
            'url': 'http://myanimelist.net/anime/18507',
            'mal_url': 'http://myanimelist.net/anime/18507',
        }
        self._assert_entry(entry1, values1)
        log.debug('Default test completed succesfully')

    @attr(online=True)
    def test_watching(self):
        self.execute_task('test_watching')
        entry0 = self.task.entries[0]
        values0 = {
            'mal_id': '9253',
            'title': 'Steins;Gate',
            'mal_type': 'TV',
            'mal_image_url': 'http://cdn.myanimelist.net/images/anime/11/41011.jpg',
            'mal_episodes': '24',
            'mal_status': 'finished airing',
            'mal_my_score': '0',
            'mal_my_status': 'watching',
            'url': 'http://myanimelist.net/anime/9253',
            'mal_url': 'http://myanimelist.net/anime/9253'
        }
        self._assert_entry(entry0, values0)

        entry1 = self.task.entries[1]
        values1 = {
            'mal_id': '18507',
            'title': 'Free!',
            'mal_type': 'TV',
            'mal_image_url': 'http://cdn.myanimelist.net/images/anime/6/51107.jpg',
            'mal_episodes': '12',
            'mal_status': 'finished airing',
            'mal_my_score': '7',
            'mal_my_status': 'watching',
            'url': 'http://myanimelist.net/anime/18507',
            'mal_url': 'http://myanimelist.net/anime/18507'
        }
        self._assert_entry(entry1, values1)
        log.debug('Watching test completed succesfully')

    @attr(online=True)
    def test_plantowatch(self):
        self.execute_task('test_plantowatch')
        entry0 = self.task.entries[0]
        values0 = {
            'mal_id': '2167',
            'title': 'Clannad',
            'mal_type': 'TV',
            'mal_image_url': 'http://cdn.myanimelist.net/images/anime/13/8498.jpg',
            'mal_episodes': '23',
            'mal_status': 'finished airing',
            'mal_my_score': '0',
            'mal_my_status': 'plan to watch',
            'url': 'http://myanimelist.net/anime/2167',
            'mal_url': 'http://myanimelist.net/anime/2167'
        }
        self._assert_entry(entry0, values0)

        entry1 = self.task.entries[1]
        values1 = {
            'mal_id': '4224',
            'title': 'Toradora!',
            'mal_type': 'TV',
            'mal_image_url': 'http://cdn.myanimelist.net/images/anime/5/22125.jpg',
            'mal_episodes': '25',
            'mal_status': 'finished airing',
            'mal_my_score': '0',
            'mal_my_status': 'plan to watch',
            'url': 'http://myanimelist.net/anime/4224',
            'mal_url': 'http://myanimelist.net/anime/4224'
        }
        self._assert_entry(entry1, values1)
        log.debug('Plan to watch test completed succesfully')

    @attr(online=True)
    def test_completed(self):
        self.execute_task('test_completed')
        entry0 = self.task.entries[0]
        values0 = {
            'mal_id': '2993',
            'title': 'Rosario to Vampire',
            'mal_type': 'TV',
            'mal_image_url': 'http://cdn.myanimelist.net/images/anime/3/25062.jpg',
            'mal_episodes': '13',
            'mal_status': 'finished airing',
            'mal_my_score': '0',
            'mal_my_status': 'completed',
            'url': 'http://myanimelist.net/anime/2993',
            'mal_url': 'http://myanimelist.net/anime/2993'
        }
        self._assert_entry(entry0, values0)

        entry1 = self.task.entries[1]
        values1 = {
            'mal_id': '11933',
            'title': 'Oda Nobuna no Yabou',
            'mal_type': 'TV',
            'mal_image_url': 'http://cdn.myanimelist.net/images/anime/11/39249.jpg',
            'mal_episodes': '12',
            'mal_status': 'finished airing',
            'mal_my_score': '0',
            'mal_my_status': 'completed',
            'url': 'http://myanimelist.net/anime/11933',
            'mal_url': 'http://myanimelist.net/anime/11933'
        }
        self._assert_entry(entry1, values1)
        log.debug('Completed test completed succesfully')

    @attr(online=True)
    def test_onhold(self):
        self.execute_task('test_onhold')
        entry0 = self.task.entries[0]
        values0 = {
            'mal_id': '1579',
            'title': 'Kiniro no Corda: Primo Passo',
            'mal_type': 'TV',
            'mal_image_url': 'http://cdn.myanimelist.net/images/anime/9/7228.jpg',
            'mal_episodes': '25',
            'mal_status': 'finished airing',
            'mal_my_score': '0',
            'mal_my_status': 'on-hold',
            'url': 'http://myanimelist.net/anime/1579',
            'mal_url': 'http://myanimelist.net/anime/1579'
        }
        self._assert_entry(entry0, values0)

        entry1 = self.task.entries[1]
        values1 = {
            'mal_id': '5114',
            'title': 'Fullmetal Alchemist: Brotherhood',
            'mal_type': 'TV',
            'mal_image_url': 'http://cdn.myanimelist.net/images/anime/5/47421.jpg',
            'mal_episodes': '64',
            'mal_status': 'finished airing',
            'mal_my_score': '0',
            'mal_my_status': 'on-hold',
            'url': 'http://myanimelist.net/anime/5114',
            'mal_url': 'http://myanimelist.net/anime/5114'
        }
        self._assert_entry(entry1, values1)
        log.debug('Onhold test completed succesfully')

    @attr(online=True)
    def test_dropped(self):
        self.execute_task('test_dropped')
        entry0 = self.task.entries[0]
        values0 = {
            'mal_id': '4181',
            'title': 'Clannad: After Story',
            'mal_type': 'TV',
            'mal_image_url': 'http://cdn.myanimelist.net/images/anime/13/24647.jpg',
            'mal_episodes': '24',
            'mal_status': 'finished airing',
            'mal_my_score': '0',
            'mal_my_status': 'dropped',
            'url': 'http://myanimelist.net/anime/4181',
            'mal_url': 'http://myanimelist.net/anime/4181'
        }
        self._assert_entry(entry0, values0)

        entry1 = self.task.entries[1]
        values1 = {
            'mal_id': '5682',
            'title': 'Phantom: Requiem for the Phantom',
            'mal_type': 'TV',
            'mal_image_url': 'http://cdn.myanimelist.net/images/anime/8/22470.jpg',
            'mal_episodes': '26',
            'mal_status': 'finished airing',
            'mal_my_score': '0',
            'mal_my_status': 'dropped',
            'url': 'http://myanimelist.net/anime/5682',
            'mal_url': 'http://myanimelist.net/anime/5682'
        }
        self._assert_entry(entry1, values1)
        log.debug('Dropped test completed succesfully')
