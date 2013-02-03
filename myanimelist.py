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

import logging
from flexget.utils.soup import get_soup
from flexget.utils.tools import urlopener
from flexget.utils.cached_input import cached
from flexget.plugin import register_plugin, PluginError
from flexget.entry import Entry

log = logging.getLogger('myanimelist')

class MyAnimeList(object):
    """A simple MyAnimeList.net input plugin for FlexGet.
       Creates an entry for each item in the current watching anime list.

    Syntax:

    myanimelist:
      username: <value>

    Example:

      import_series:
        from:
          myanimelist:
            username: 'your username'

    Option username are required. Anime list must be public.
    """

    def validator(self):
        from flexget import validator
        root = validator.factory('dict')
        root.accept('text', key='username', requried=True)
        return root

    @cached('myanimelist', persist='2 hour')
    def on_task_input(self, task, config):
        url_params = config.copy()
        if 'username' in config:
            url_params['username'] = config['username']
            url_params['section'] = 'watching'
            url_params['sort'] = 'by name'
        else:
            raise PluginError('Must define the list username to retrieve from MAL')

        url = 'http://myanimelist.net/animelist/'
        if url_params['username']:
            url+= config['username']
        if url_params['section'] == 'watching':
            url+='&status=1'
        if url_params['sort'] == 'by name':
            url+='&order=1'

        entries = []
        log.verbose("Retrieving MyAnimeList on %s ."  % url)
        
        page = urlopener(url, log)
        soup = get_soup(page)

        if soup.div('', "badresult"):
            raise PluginError('Anime list isn\'t public.')
        for a in soup.find_all('a', 'animetitle'):
            title = a.span.string.replace('.', '').replace('-', ' ')
            entry= Entry()
            entry['title'] = title
            entries.append(entry)
            return entries

register_plugin(MyAnimeList, 'myanimelist', api_ver=2)
