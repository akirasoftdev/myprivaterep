# -*- coding: utf-8 -*-
import re


class AddressParser(object):

    @classmethod
    def parse(cls, address):
        r = re.compile("^([^市区]*市)([^市区]*区).*$")
        m = r.search(address)
        if m is not None:
            return m.group(1) + m.group(2)
        r = re.compile("^([^区郡市]*[区|郡|市]).*")
        m = r.search(address)
        if m is not None:
            return m.group(1)

        r = re.compile("(.*[町|村]).*")
        m = r.search(address)
        if m is not None:
            return m.group(1)
        raise Exception(address)

    @classmethod
    def parse_town(cls, address):
        address = re.compile(u"[０-９]+丁目$").sub('', address)
        address = re.compile(u"^大字").sub('', address)
        address = re.compile(u"下宮田$").sub('', address)
        address = re.compile(u"上宮田$").sub('', address)
        address = re.compile(u"西通$").sub('', address)
        address = re.compile(u"字谷戸田上$").sub('', address)
        address = re.compile(u"(.+)イ$").sub(u'\\1', address)

        return address
        raise Exception(address)