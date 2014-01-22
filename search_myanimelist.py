from __future__ import unicode_literals, division, absolute_import
import logging
from flexget.utils.cached_input import cached
from flexget.plugin import register_plugin, PluginError, internet
from flexget.entry import Entry

log = logging.getLogger('search_myanimelist')


def parse_xml(xml):
    from xml.etree.ElementTree import fromstring
    from xml.etree.ElementTree import ParseError

    try:
        tree = fromstring(xml)
    except ParseError:
        return
    return [{item.tag: item.text for item in elem} for elem in tree.findall('entry')]


def safe_username(username):
    from urllib import always_safe

    safe_string = always_safe.replace('.', '')
    safe_name = ''.join([s for s in username if s in safe_string])
    if username != safe_name:
        log.warning('username can only be made of letters, numbers and _-')
    return safe_name


def get_config(config):
    """ if config is a single string turn into a list """
    if isinstance(config, basestring):
        config = [config]
    return config


class SearchMyAnimeList(object):
    """ A simple search MyAnimeList.net input plugin for FlexGet.

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

    API_URL = 'http://myanimelist.net/api/anime/search.xml'
    user_agent = 'api-team-692e8861471e4de2fd84f6d91d1175c0'

    anime_map = {
        'mal_id': 'id',
        'title': 'title',
        'description': 'synopsis',
        'mal_type': 'type',
        'mal_episodes': 'episodes',
        'mal_status': 'status',
        'mal_image_url': 'image'
    }

    def validator(self):
        from flexget import validator

        root = validator.factory()
        root.accept('text')
        bundle = root.accept('list')
        bundle.accept('text')
        return root

    @cached('search_myanimelist')
    @internet(log)
    def on_task_input(self, task, config):
        queries = get_config(config)
        session = task.requests
        session.auth = ('flexget', 'flexget')
        session.headers.update({'User-Agent': self.user_agent})
        entries = []
        for query in queries:
            params = {'q': query}
            url = self.API_URL

            resp = session.get(url, params=params)
            log.verbose("Searching MyAnimeList on %s" % resp.url)
            if not resp or resp.status_code != 200:
                log.warning('No data returned from MyAnimeList')
                return

            content_type = resp.headers['content-type']
            if content_type == 'text/html; charset=UTF-8':
                data = parse_xml(resp.text)
            else:
                log.warning('Content type not recognized: %s' % content_type)
                data = ''

            if not isinstance(data, list) or not data:
                raise PluginError('Faulty items in response: %r' % data)

            for item in data:
                entry = Entry()
                entry.update_using_map(self.anime_map, item)
                entry['mal_image_url'] = entry['mal_image_url'].replace('t.jpg', '.jpg')
                mal_url = 'http://myanimelist.net/anime/%s' % item['id']
                entry['url'] = mal_url
                entry['mal_url'] = mal_url
                entry['mal_status'] = entry['mal_status'].lower()
                entries.append(entry)
        return entries


register_plugin(SearchMyAnimeList, 'search_myanimelist', api_ver=2)
