# -*- coding: utf-8 -*-
'''
Playlist Generator
This module can generate .m3u playlists with tv guide
and groups
'''
import re
import urllib2

import TvgFixer
import m3uHelper
from modules import PlaylistSorter


class PlaylistGenerator(object):
    m3uheader = \
        '#EXTM3U url-tvg="http://www.teleguide.info/download/new3/jtv.zip"\n'

    def __init__(self):
        self.itemlist = list()
        self.tvgfixer = TvgFixer.TvgFix()

    def addItem(self, item):
        self.itemlist.append(m3uHelper.m3uItem.fromArray(item))

    def exportm3u(self, hostport, add_ts=False):
        '''
        Exports m3u playlist
        '''
        itemlist = PlaylistGenerator.m3uheader
        if add_ts:
            # Adding ts:// after http:// for some players
            hostport = 'ts://' + hostport

        for item in PlaylistSorter.sortPlaylist(self.itemlist):
            if not item.tvgname:
                item.tvgname = item.name.replace(' ', '_')
            # For .acelive and .torrent
            item.url = re.sub('^(http.+)$', lambda match: 'http://' + hostport + '/torrent/' + \
                                                          urllib2.quote(match.group(0), '') + '/stream.mp4',
                              item.url,
                              flags=re.MULTILINE)
            # For PIDs
            item.url = re.sub('^(acestream://)?(?P<pid>[0-9a-f]{40})$',
                              'http://' + hostport + '/pid/\\g<pid>/stream.mp4',
                              item.url, flags=re.MULTILINE)

            item = self.tvgfixer.fixm3u(item)

            itemlist += item.getExtInf() + u"\n" + item.url + u"\n"

        return itemlist
