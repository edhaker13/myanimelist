# Flexget MyAnimeList Plugin
# http://www.flexget.com
# http://myanimelist.net
# Created by: Luis Checa <edhaker13@gmail.com>
# Inspired by the plugin from fuzzylights' repo
# https://bitbucket.org/fuzzylights/plugins-for-flexget/wiki/Home
# the trakt import series plugin for syntax and features
# http://github.com/Flexget/Flexget/blob/master/flexget/plugins/input/trakt_list.py
# and the BeatifulSoup Documentation (it's for bs3)
# http://www.crummy.com/software/BeautifulSoup/bs3/documentation.html
from __future__ import unicode_literals, division, absolute_import
import logging
from flexget.utils.cached_input import cached
from flexget.plugin import register_plugin, PluginError, internet
from flexget.entry import Entry

log = logging.getLogger('myanimelist')


class MyAnimeList(object):
    """A simple MyAnimeList.net input plugin for FlexGet.

    Creates an entry for each item in the current watching anime list.

    Simple Syntax::

      myanimelist: <username>

    Advanced Syntax::

      myanimelist:
        username: <value>
        list: <watching|plan to watch|completed|on-hold|dropped>

    Example::

      import_series:
        from:
          myanimelist:
            username: flexget
            list: plan to watch

    <username> is required. Anime list must be public.
    """
    schema = {
        'type': ['string', 'object'],
        'properties': {
            'username': {'type': 'string'},
            'list': {'enum': ['watching', 'plan to watch', 'completed', 'on-hold', 'dropped'], 'default': 'watching'}
        },
        'required': ['username'],
        'additionalProperties': False
    }

    anime_map = {
        'mal_id': 'id',
        'title': 'title',
        'mal_type': 'type',
        'mal_image_url': 'image_url',
        'mal_episodes': 'episodes',
        'mal_status': 'status',
        'mal_user_score': 'score',
        'mal_watched_status': 'watched_status'
    }

    def safe_username(self, username):
        from urllib import always_safe

        safe_string = always_safe.replace('.', '')
        safe_username = ''.join([s for s in username if s in safe_string])
        if username != safe_username:
            log.warning('username can only be made of letters, numbers and _-')
        return safe_username

    def get_config(self, config):
        # Turn into a dict with the username
        if isinstance(config, basestring):
            config = {'username': config}
        return config

    @cached('myanimelist')
    @internet(log)
    def on_task_input(self, task, config):
        config = self.get_config(config)

        log.debug('Starting MyAnimeList plugin')
        # Retrieve username and remove invalid characters
        username = config['username']
        username = self.safe_username(username)

        status = config.get('list', 'watching')

        url = 'http://mal-api.com/animelist/%s' % username
        log.verbose("Retrieving MyAnimeList on %r ." % url)
        entries = []

        data = task.requests.get(url).json()
        if not data:
            log.warning('No data returned from MyAnimeList.')
            return

        if not isinstance(data['anime'], list):
            raise PluginError('Incompatible items in response: %r.' % data['anime'])
        data = data['anime']
        for item in data:
            if item['watched_status'] == status:
                entry = Entry()
                entry.update_using_map(self.anime_map, item, ignore_none=True)
                mal_url = 'http://myanimelist.net/anime/%s' % item['id']
                entry['url'] = mal_url
                entry['mal_url'] = mal_url
                entries.append(entry)

        return entries


register_plugin(MyAnimeList, 'myanimelist', api_ver=2)
