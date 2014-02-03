# Flexget MyAnimeList Plugin http://www.flexget.com
# http://myanimelist.net
# Created by: Luis Checa <edhaker13@gmail.com>

from __future__ import unicode_literals, division, absolute_import
import logging
from flexget.utils.cached_input import cached
from flexget.plugin import register_plugin, PluginError, internet
from flexget.entry import Entry

log = logging.getLogger('myanimelist')


def parse_xml(xml):
    from xml.etree.ElementTree import fromstring
    from xml.etree.ElementTree import ParseError

    try:
        tree = fromstring(xml)
    except ParseError:
        log.error('No valid xml found: %s', xml if not xml.splitlines() else xml.splitlines()[0])
        return
    except UnicodeEncodeError as exc:
        log.error('Unhandled value while parsing xml.\n%s', exc)
        return
    return [{item.tag: item.text for item in elem} for elem in tree.findall('anime')]


def safe_username(username):
    from urllib import always_safe

    safe_string = always_safe.replace('.', '')
    safe_name = ''.join([s for s in username if s in safe_string])
    if username != safe_name:
        log.warning('username can only be made of letters, numbers and _-')
    return safe_name


def get_config(config):
    """ if config is only a username, turn into a dict """
    if isinstance(config, basestring):
        config = {'username': config}
    return config


class MyAnimeList(object):
    """A simple MyAnimeList.net input plugin for FlexGet.

    Creates an entry for each item in the current watching anime list.

    Simple Syntax:

      myanimelist: <username>

    Advanced Syntax:

      myanimelist:
        username: <value>
        list: <watching|plan to watch|completed|on-hold|dropped>
        user-agent: <whitelisted agent>

    Example:

      import_series:
        from:
          myanimelist:
            username: flexget
            list: plan to watch

    <username> is required. Anime list must be public.
    """

    API_URL = 'http://myanimelist.net/malappinfo.php?u=%s&status=all&type=anime'
    user_agent = 'api-team-692e8861471e4de2fd84f6d91d1175c0'

    schema = {
        'type': ['string', 'object'],
        'properties': {
            'username': {'type': 'string'},
            'user-agent': {'type': 'string', 'default': user_agent},
            'list': {'enum': ['watching', 'plan to watch', 'completed', 'on-hold', 'dropped'], 'default': 'watching'}
        },
        'required': ['username'],
        'additionalProperties': False
    }

    anime_map = {
        'mal_id': 'series_animedb_id',
        'title': 'series_title',
        'mal_type': 'series_type',
        'mal_image_url': 'series_image',
        'mal_episodes': 'series_episodes',
        'mal_status': 'series_status',
        'mal_my_score': 'my_score',
        'mal_my_status': 'my_status'
    }

    watched_map = {
        'watching': '1',
        'completed': '2',
        'on-hold': '3',
        'dropped': '4',
        'plan to watch': '6'
    }

    inv_watched_map = {v: k for k, v in watched_map.items()}

    type_map = {
        '1': 'TV',
        '2': 'OVA',
        '3': 'Movie',
        '4': 'Special',
        '5': 'ONA',
        '6': 'Music'
    }

    status_map = {
        '1': 'currently airing',
        '2': 'finished airing',
        '3': 'not yet aired'
    }

    @cached('myanimelist')
    @internet(log)
    def on_task_input(self, task, config):
        config = get_config(config)

        log.debug('Starting MyAnimeList plugin')
        # Retrieve username and remove invalid characters
        username = safe_username(config['username'])

        status = config.get('list', 'watching')

        url = self.API_URL % username
        log.verbose('Retrieving MyAnimeList on %s.', url)

        headers = {'User-Agent': config.get('user-agent', self.user_agent)}
        log.debug('Using %s', headers)

        resp = task.requests.get(url, headers=headers)
        if not resp or resp.status_code != 200:
            log.warning('No data returned from MyAnimeList.')
            return

        content_type = resp.headers.get('content-type')
        if content_type == 'application/xml; charset=UTF-8':
            data = parse_xml(resp.text.encode('utf-8'))
            log.debug('Parsed xml to list of dicts')
        else:
            log.warning('Content type not xml: %s' % content_type)
            data = ''

        if not isinstance(data, list):
            raise PluginError('Incompatible items in response: %r.' % data)

        entries = []
        for item in data:
            if item['my_status'] == self.watched_map.get(status):
                entry = Entry()
                entry.update_using_map(self.anime_map, item, ignore_none=True)
                mal_url = 'http://myanimelist.net/anime/%s' % entry['mal_id']
                entry['url'] = mal_url
                entry['mal_url'] = mal_url
                entry['mal_type'] = self.type_map.get(entry['mal_type'])
                entry['mal_my_status'] = self.inv_watched_map.get(entry['mal_my_status'])
                entry['mal_status'] = self.status_map.get(entry['mal_status'])
                entries.append(entry)
                log.debug('Appended entry: %s', entry.get('title'))

        log.debug('Returning %s entries', len(entries))
        return entries


register_plugin(MyAnimeList, 'myanimelist', api_ver=2)
