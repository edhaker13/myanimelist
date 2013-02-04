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
import re
from requests import RequestException
from flexget.utils import json
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
    anime_map = {
        'title': 'title'
                 }

    def validator(self):
        from flexget import validator
        root = validator.factory('dict')
        root.accept('text', key='username', requried=True)
        root.accept('choice', key='list').accept_choices(['watching', 'plan to watch'])
        return root

    @cached('myanimelist', persist='2 hour')
    def on_task_input(self, task, config):
        if not 'username' in config:
            raise PluginError('Must define the list username to retrieve from MAL')
    
        username = config['username']
        
        if not 'list' in config:    
            status = 'watching'
        else:
            status = config['list']
        
        url = 'http://mal-api.com/animelist/%s' % username
        if 'password' in config:
            auth = {'username': config['username'],
                    'password': config['password']}
        entries = []
        log.verbose("Retrieving MyAnimeList on %s ."  % url)
        
        try:
            data = task.requests.get(url).json()
        except RequestException as e:
            raise PluginError('Could not retrieve list from MAL (%s)' % e.message)
        if not data:
            #check_auth()
            log.warning('No data returned from trakt.')
            return
        
        if not isinstance(data['anime'], list):
            raise PluginError('Faulty items in response: %s' % data['anime'])
        data = data['anime']
        i = 000
        for item in data:
            if item['watched_status'] == status:
                title = data[i]['title']
                entry = Entry(title=title)
                if entry.isvalid():
                    # Remove non alphanumeric and space characters
                    entry['title'] = re.sub('[^a-zA-Z0-9 ]', '', entry['title'])
                    entries.append(entry)
            i+=1
        return entries

register_plugin(MyAnimeList, 'myanimelist', api_ver=2)
