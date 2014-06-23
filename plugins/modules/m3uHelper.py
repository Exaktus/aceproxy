# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re


class m3uItem(object):
    extinf_regex = re.compile(ur'#EXTINF:([^\s,]*)')
    tvgname_regex = re.compile(ur'tvg-name=\"([^"]*)\"')
    tvglogo_regex = re.compile(ur'tvg-logo=\"([^"]*)\"')
    tvgid_regex = re.compile(ur'tvg-id=\"([^"]*)\"')
    grouptitle_regex = re.compile(ur'group-title=\"([^"]*)\"')
    tvgshift_regex = re.compile(ur'tvg-shift=\"([^"]*)\"')
    audiotrack_regex = re.compile(ur'audio-track=\"([^"]*)\"')
    name_regex = re.compile(ur',(.*)$')

    @staticmethod
    def fromArray(array):
        mItem = m3uItem('', decode_utf8(array.get('url')))
        mItem.name = decode_utf8(array.get('name'))
        mItem.grouptitle = decode_utf8(array.get('group', ''))
        mItem.tvname = decode_utf8(array.get('tvg', ''))
        return mItem

    def __init__(self, extinf, path):
        extinf = decode_utf8(extinf)
        path = decode_utf8(path)
        self.url = path
        self.head = firstOrNone(re.findall(m3uItem.extinf_regex, extinf))
        self.name = firstOrNone(re.findall(m3uItem.name_regex, extinf))
        self.audiotrack = firstOrNone(re.findall(m3uItem.audiotrack_regex, extinf))
        self.tvgname = firstOrNone(re.findall(m3uItem.tvgname_regex, extinf))
        self.tvglogo = firstOrNone(re.findall(m3uItem.tvglogo_regex, extinf))
        self.grouptitle = firstOrNone(re.findall(m3uItem.grouptitle_regex, extinf))
        self.tvgshift = firstOrNone(re.findall(m3uItem.tvgshift_regex, extinf))
        self.tvgid = firstOrNone(re.findall(m3uItem.tvgid_regex, extinf))
        if self.head is None:
            self.head = '-1'

    def getExtInf(self):
        result = u'#EXTINF:' + self.head
        if self.audiotrack is not None:
            result += u' audio-track="' + self.audiotrack + '"'
        if self.tvgname is not None:
            result += u' tvg-name="' + decode_utf8(self.tvgname) + '"'
        if self.tvglogo is not None:
            result += u' tvg-logo="' + self.tvglogo + '"'
        if self.grouptitle is not None:
            result += u' group-title="' + decode_utf8(self.grouptitle) + '"'
        if self.tvgshift is not None:
            result += u' tvg-shift="' + self.tvgshift + '"'
        if self.tvgid is not None and self.tvgid != '0':
            result += u' tvg-id="' + decode_utf8(self.tvgid) + '"'
        result += u',' + decode_utf8(self.name)
        return result


def firstOrNone(itms):
    if not itms:
        return None
    else:
        return itms[0]


def decode_utf8(string):
    if isinstance(string, unicode):
        return string
    if isinstance(string, str):
        for encoding in (('utf-8',), ('windows-1252',), ('utf-8', 'ignore')):
            try:
                return string.decode(*encoding)
            except:
                pass
        return string  # Don't know how to handle it...
    return unicode(string, 'utf-8')