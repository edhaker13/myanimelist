from __future__ import unicode_literals, division, absolute_import
import logging
import re
import urllib
from requests import RequestException
from flexget.utils.cached_input import cached
from flexget.plugin import register_plugin, PluginError
from flexget.entry import Entry

log = logging.getLogger('myanimelist')

class SearchMAL(object):
    def validator(self):
        from flexget import validator
        root = validator.factory('dict')
        root.accept('text', key='search', requried=True)
        return root

    @cached('myanimelist', persist='1 hour')
    def search(self, task, config):
        if not 'search' in config:
            raise PluginError('Must define a search query before searching')
        query = config['search']
        query = urllib.urlencode(query, 0)
        url = 'http://mal-api.com/anime/search?q=%s' % query
        entries = []
        log.verbose("Searching MyAnimeList for %s ."  % query)
        try:
            data = task.requests.get(url).json()
        except RequestException as e:
            raise PluginError('Could not retrieve query from MAL (%s)' % e.message)
        if not data:
            #check_auth()
            log.warning('No data returned from MAL.')
            return
        
        if not isinstance(data['anime'], list):
            raise PluginError('Faulty items in response: %s' % data['anime'])
        data = data['anime']
        i = 0
        for item in data:
            if isinstance(item['id'], int):
                title = data[i]['title']
                entry = Entry()
                # Remove non alphanumeric and space characters
                title = re.sub('[^a-zA-Z0-9 \d\.]', '', title)
                entry['title'] = title
                entries.append(entry)
                i+=1
        return entries

register_plugin(SearchMAL, 'myanimelist', api_ver=2)
