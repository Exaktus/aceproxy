# coding=utf-8
from modules.PluginInterface import AceProxyPlugin
from modules.m3uHelper import m3uItem
from modules import PlaylistSorter
from config import jplaylist
import urllib2
import re


class Jplaylist(AceProxyPlugin):
    handlers = ('jplaylist', )

    def __init__(self, AceConfig, AceStuff):
        if AceConfig.httphost == '0.0.0.0':
            self.hosttmpl = '127.0.0.1'
        else:
            self.hosttmpl = AceConfig.httphost
        self.hosttmpl += ':'+str(AceConfig.httpport)
        pass

    def handle(self, connection):
        connection.send_response(200)
        connection.end_headers()
        idLst = []
        nameLst = []
        tvgnameLst = []
        items = []
        head = ''
        for ur in jplaylist.urls:
            ur = ur.replace('{AceProxy}', self.hosttmpl)
            plsrc = urllib2.urlopen(ur, timeout=10).read()
            if head == '':
                head += re.findall(re.compile(ur'(#EXTM3U.*$)', re.MULTILINE), plsrc)[0]
            nitems = re.finditer(ur'(?P<extinf>#EXTINF:.*)\n(?P<url>.*)$', plsrc, re.MULTILINE)
            for it in nitems:
                nch = m3uItem(it.groupdict()['extinf'], it.groupdict()['url'])
                new = False
                if nch.tvgid and not nch.tvgid in idLst:
                    new = True
                    idLst.append(nch.tvgid)
                if nch.name and not nch.name in nameLst:
                    new = True
                    nameLst.append(nch.name)
                if nch.name and not nch.tvgname in tvgnameLst:
                    new = True
                    tvgnameLst.append(nch.tvgname)
                if new:
                    items.append(nch)
        result = head
        for item in PlaylistSorter.sortPlaylist(items):
            result += u'\n' + item.getExtInf() + u'\n' + item.url
        connection.wfile.write(result.encode('utf-8'))