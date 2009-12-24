##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
from rwproperty import setproperty, getproperty

from zope import interface, component
from zope.location import Location
from zope.proxy import removeAllProxies
from zope.dublincore.interfaces import IDCExtended

from interfaces import IContentTags, IContentTaggable


class ContentTags(Location):
    interface.implements(IContentTags)
    component.adapts(IContentTaggable)

    def __init__(self, content):
        self.content = content
        self.dc = IDCExtended(content)

    @property
    def __parent__(self):
        return self.content

    @getproperty
    def tags(self):
        return self.dc.subjects

    @setproperty
    def tags(self, value):
        if value:
            self.dc.subjects = value
        else:
            self.dc.subjects = ()
