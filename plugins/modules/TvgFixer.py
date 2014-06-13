# -*- coding: utf-8 -*-
from distutils import config
import xml.etree.ElementTree as ET
import os
import os.path
import config.tgvfixer

class TvgFix(object):
    def getTvg(self, tvgname, name):
        name = unicode(name, "UTF-8")
        tvgname = unicode(tvgname, "UTF-8")
        res = self.getLogo(name)
        if name in self.tvgConfig:
            res += 'tvg-name="' + self.tvgConfig[name][0] + '" tvg-id="' + self.tvgConfig[name][
                1] + '" tvg-shift="' + self.tvgConfig[name][2] + '"'
        else:
            res += 'tvg-name="' + tvgname + '"'
        res8 = res.encode("UTF-8")
        return res8

    def getLogo(self, name):
        if name in self.tvgLogoConfig:
            res = 'tvg-logo="' + self.tvgLogoConfig[name] + '" '
        else:
            res = ''
        res8 = res.encode("UTF-8")
        return res8

    def __init__(self):
        self.tvgConfig = {}
        self.tvgLogoConfig = {}
        if os.path.isfile(os.path.realpath(config.tgvfixer.tvgConfigPath)):
            tree = ET.parse(os.path.realpath(config.tgvfixer.tvgConfigPath))
            root = tree.getroot()
            for name in root.findall("channel"):
                wrongname = name.get("name")
                correctname = name.find("tvgname").text
                correcttvgid = name.find("tvgid").text
                correcttvgshift = name.find("tvgshift").text
                self.tvgConfig[wrongname] = [correctname, correcttvgid, correcttvgshift]

        if os.path.isfile(os.path.realpath(config.tgvfixer.tvgLogoConfigPath)):
            tree = ET.parse(os.path.realpath(config.tgvfixer.tvgLogoConfigPath))
            root = tree.getroot()
            for name in root.findall("channel"):
                chName = name.get("name")
                tgvLogoPath = name.find("tvglogo").text
                self.tvgLogoConfig[chName] = tgvLogoPath
