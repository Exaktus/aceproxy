# -*- coding: utf-8 -*-
'''
Playlist Generator
This module can generate .m3u playlists with tv guide
and groups
'''
import re
import urllib2
import TvgFixer

class PlaylistGenerator(object):

    m3uheader = \
        '#EXTM3U url-tvg="http://www.teleguide.info/download/new3/jtv.zip"\n'
    m3uchanneltemplate = \
        '#EXTINF:-1 group-title="%s" %s,%s\n%s\n'

    def __init__(self):
        self.itemlist = list()
        self.tvgfixer = TvgFixer.TvgFix()

    def addItem(self, itemdict):
        '''
        Adds item to the list
        itemdict is a dictionary with the following fields:
            name - item name
            url - item URL
            tvg - item JTV name (optional)
            group - item playlist group (optional)
        '''
        self.itemlist.append(itemdict)

    def generatem3uline(self, item):
        '''
        Generates EXTINF line with url
        '''
        return PlaylistGenerator.m3uchanneltemplate % (
            item.get('group', ''), self.tvgfixer.getTvg(item.get('tvg', ''),item.get('name')),
            item.get('name'), item.get('url'))

    def exportm3u(self, hostport, add_ts=False):
        '''
        Exports m3u playlist
        '''
        itemlist = PlaylistGenerator.m3uheader
        if add_ts:
                # Adding ts:// after http:// for some players
                hostport = 'ts://' + hostport

        for item in self.itemlist:
            item['tvg'] = item.get('tvg', '') if item.get('tvg') else \
                item.get('name').replace(' ', '_')
            # For .acelive and .torrent
            item['url'] = re.sub('^(http.+)$', lambda match: 'http://' + hostport + '/torrent/' + \
                             urllib2.quote(match.group(0), '') + '/stream.mp4', item['url'],
                                   flags=re.MULTILINE)
            # For PIDs
            item['url'] = re.sub('^(acestream://)?(?P<pid>[0-9a-f]{40})$', 'http://' + hostport + '/pid/\\g<pid>/stream.mp4',
                                    item['url'], flags=re.MULTILINE)

            itemlist += self.generatem3uline(item)

        return itemlist
