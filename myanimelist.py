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
from urllib import urlencode
from requests import RequestException
from flexget.utils.cached_input import cached
from flexget.plugin import register_plugin, PluginError, internet
from flexget.entry import Entry

log = logging.getLogger('myanimelist')
status_list = ['watching', 'plan to watch', 'completed', 'on-hold', 'dropped']


class MyAnimeList(object):
    """A simple MyAnimeList.net input plugin for FlexGet.

    Creates an entry for each item in the current watching anime list.

    Simple Syntax::

      myanimelist: <username>

    Advanced Syntax::

      myanimelist:
        username: <value>
        list: <value>

    Example::

      import_series:
        from:
          myanimelist:
            username: edhaker13
            list: plan to watch

    <username> is required. Anime list must be public.
    """

    def validator(self):
        from flexget import validator

        root = validator.factory()
        root.accept('text')
        advanced = root.accept('dict')
        advanced.accept('text', key='username', requried=True)
        advanced.accept('choice', key='list', requried=True).accept_choices(status_list)
        return root

    def get_config(self, config):
        # Turn into a dict with the username
        if isinstance(config, basestring):
            config = {'username': config}
        return config

    @cached('myanimelist')
    @internet(log)
    def on_task_input(self, task, config):
        config = self.get_config(config)
        if not 'username' in config:
            raise PluginError('Must define the list\'s username to retrieve.')

        # Retrieve username and urlencode it
        username = config['username']
        username = urlencode(username, 0)

        status = config.get('list', 'watching')

        url = 'http://mal-api.com/animelist/%s' % username
        log.verbose("Retrieving MyAnimeList on %r ." % url)
        entries = []

        try:
            data = task.requests.get(url).json()
        except RequestException as e:
            raise PluginError('Could not retrieve list from MyAnimeList (%s).' % e.message)
        if not data:
            log.warning('No data returned from MyAnimeList.')
            return

        if not isinstance(data['anime'], list):
            raise PluginError('Incompatible items in response: %r.' % data['anime'])
        data = data['anime']
        i = 0
        for item in data:
            if item['watched_status'] == status:
                title = data[i]['title']
                entry = Entry()
                entry['title'] = title
                entries.append(entry)

            i += 1
        return entries


register_plugin(MyAnimeList, 'myanimelist', api_ver=2)
