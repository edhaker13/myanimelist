from __future__ import unicode_literals, division, absolute_import
import logging
from urllib import urlencode
from flexget.utils.cached_input import cached
from flexget.plugin import register_plugin, PluginError, internet
from flexget.entry import Entry

log = logging.getLogger('search_myanimelist')


class SearchMyAnimeList(object):
    """A simple search MyAnimeList.net input plugin for FlexGet.

    Creates an entry for each item found by the queries.

    Simple Syntax::

      search_myanimelist: <query>

    List Sysntax::

      search_myanimelist:
        - <query1>
        - <query2>

    Example::

      import_series:
        from:
          search_myanimelist: Free!
    """
    anime_map = {
        'mal_id': 'id',
        'title': 'title',
        'description': 'synopsis',
        'mal_type': 'type',
        'mal_episodes': 'episodes'
    }

    def validator(self):
        from flexget import validator

        root = validator.factory()
        root.accept('text')
        bundle = root.accept('list')
        bundle.accept('text')
        return root

    def get_config(self, config):
        # if it's just one string turn into single list
        if isinstance(config, basestring):
            config = [config]
        return config

    @cached('search_myanimelist')
    @internet(log)
    def on_task_input(self, task, config):
        queries = self.get_config(config)
        entries = []
        for query in queries:
            query = urlencode({'q': query, '': ''})
            url = 'http://mal-api.com/anime/search?%s' % query
            log.verbose("Searching MyAnimeList for %s ." % query)
            data = task.requests.get(url).json()
            if not data:
                log.warning('No data returned from MyAnimeList.')
                return None
            if not isinstance(data, list):
                raise PluginError('Faulty items in response: %s' % data)
            for item in data:
                entry = Entry()
                entry.update_using_map(self.anime_map, item)
                entry['mal_image_url'] = item['image_url'].replace('t.jpg', '.jpg')
                mal_url = 'http://myanimelist.net/anime/%s' % item['id']
                entry['url'] = mal_url
                entry['mal_url'] = mal_url
                entries.append(entry)
        return entries


register_plugin(SearchMyAnimeList, 'search_myanimelist', api_ver=2)
