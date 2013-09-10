from __future__ import unicode_literals, division, absolute_import
import logging
from urllib import urlencode
from requests import RequestException
from flexget.utils.cached_input import cached
from flexget.plugin import register_plugin, PluginError, internet
from flexget.entry import Entry

log = logging.getLogger('search_myanimelist')


class MyAnimeListSearch(object):
    """A simple search MyAnimeList.net input plugin for FlexGet.

    Creates an entry for each item found by the queries.

    Simple Syntax::

      search_myanimelist: <query>

    List Sysntax::

      search_myanimelist:
        - <query1>
        - <query2>.

    Example::

      import_series:
        from:
          search_myanimelist: Free!
    """

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
            query = urlencode(query, 0)
            url = 'http://mal-api.com/anime/search?q=%s' % query
            log.verbose("Searching MyAnimeList for %s ." % query)
            try:
                data = task.requests.get(url).json()
            except RequestException as e:
                raise PluginError('Could not retrieve query from MAL (%s)' % e.message)
            if not data:
                log.warning('No data returned from MAL.')
                return None

            if not isinstance(data['anime'], list):
                raise PluginError('Faulty items in response: %s' % data['anime'])
                # reduces list nesting
            data = data['anime']
            # JSON indexing starts at 0
            i = 0
            for item in data:
                if isinstance(item['id'], int):
                    title = data[i]['title']
                    entry = Entry()
                    entry['title'] = title
                    entries.append(entry)
                    i += 1
        return entries


register_plugin(MyAnimeListSearch, 'search_myanimelist', api_ver=2)
