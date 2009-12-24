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
from zope import interface
from zope.i18n import translate
from zope.location import Location
from zope.component import queryUtility
from zojax.tagging.engine import TaggingEngine
from zojax.content.type.interfaces import IContentType

from interfaces import _
from interfaces import IGlobalTaggingEngine
from interfaces import IContentTaggingEngine
from interfaces import IContentTaggingEngineBase


class ContentTaggingEngineBase(TaggingEngine, Location):
    interface.implements(IContentTaggingEngineBase)

    @property
    def description(self):
        return translate(
            u'Total items: ${items}, total tags: ${tags}',
            'zojax.content.tagging',
            mapping={'items': self.itemsCount, 'tags':self.tagsCount})

    def updateContent(self, content, oid, tags):
        self.update(oid, tags)

    def removeContent(self, content, oid):
        self.remove(oid)


class GlobalTaggingEngine(ContentTaggingEngineBase):
    interface.implements(IGlobalTaggingEngine)

    title = _(u'All tags')


class ContentTaggingEngine(ContentTaggingEngineBase):
    interface.implements(IContentTaggingEngine)

    def __init__(self, ct):
        self.contenttype = ct
        super(ContentTaggingEngine, self).__init__()

    @property
    def title(self):
        ct = queryUtility(IContentType, name=self.contenttype)
        if ct is not None:
            return translate('Tags for: ', 'zojax.content.tagging') + \
                translate(ct.title)
        else:
            return u'Tags for: %s'%self.contenttype

    def updateContent(self, content, oid, tags):
        if IContentType(content).name == self.contenttype:
            self.update(oid, tags)
