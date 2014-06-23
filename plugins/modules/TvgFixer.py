# -*- coding: utf-8 -*-
from distutils import config
import xml.etree.ElementTree as ET
import os
import os.path

import config.tgvfixer
import m3uHelper


class TvgFix(object):
    def fixm3u(self, item):
        itemName=m3uHelper.decode_utf8(item.name)
        if itemName in self.tvgConfig:
            item.tvgname = m3uHelper.decode_utf8(self.tvgConfig[itemName][0])
            item.tvgid = m3uHelper.decode_utf8(self.tvgConfig[itemName][1])
            item.tvgshift = m3uHelper.decode_utf8(self.tvgConfig[itemName][2])
        if itemName in self.tvgLogoConfig:
            item.tvglogo = m3uHelper.decode_utf8(self.tvgLogoConfig[itemName])
        return item

    def __init__(self):
        self.tvgConfig = {}
        self.tvgLogoConfig = {}
        if os.path.isfile(os.path.realpath(config.tgvfixer.tvgConfigPath)):
            tree = ET.parse(os.path.realpath(config.tgvfixer.tvgConfigPath))
            root = tree.getroot()
            for name in root.findall("channel"):
                wrongname = m3uHelper.decode_utf8(name.get("name"))
                correctname = m3uHelper.decode_utf8(name.find("tvgname").text)
                correcttvgid = m3uHelper.decode_utf8(name.find("tvgid").text)
                correcttvgshift = m3uHelper.decode_utf8(name.find("tvgshift").text)
                self.tvgConfig[wrongname] = [correctname, correcttvgid, correcttvgshift]

        if os.path.isfile(os.path.realpath(config.tgvfixer.tvgLogoConfigPath)):
            tree = ET.parse(os.path.realpath(config.tgvfixer.tvgLogoConfigPath))
            root = tree.getroot()
            for name in root.findall("channel"):
                chName = m3uHelper.decode_utf8(name.get("name"))
                tgvLogoPath = m3uHelper.decode_utf8(name.find("tvglogo").text)
                self.tvgLogoConfig[chName] = tgvLogoPath