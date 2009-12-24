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
from zope import interface, event
from zope.component import getUtility, getUtilitiesFor
from zope.app.intid.interfaces import IIntIds
from zope.dublincore.interfaces import ICMFDublinCore
from zope.lifecycleevent import ObjectCreatedEvent
from zojax.content.type.interfaces import IContentType
from zojax.content.type.configlet import ContentContainerConfiglet

from interfaces import _
from interfaces import IContentTags, IContentTaggingConfiglet, IContentTaggable
from engine import GlobalTaggingEngine, ContentTaggingEngine


class ContentTaggingConfiglet(ContentContainerConfiglet):
    interface.implements(IContentTaggingConfiglet)

    title = _('Content tagging')

    @property
    def globalEngine(self):
        if 'global' not in self:
            globalEngine = GlobalTaggingEngine()
            event.notify(ObjectCreatedEvent(globalEngine))
            self['global'] = globalEngine

        return self['global']

    def contentTypesEngines(self):
        for name, ct in getUtilitiesFor(IContentType):
            if IContentTaggable.implementedBy(ct.klass):
                yield self.engingForContentType(ct)

    def engineForContent(self, content):
        return self.engingForContentType(IContentType(content))

    def engingForContentType(self, ct):
        if ct.name not in self:
            engine = ContentTaggingEngine(ct.name)
            event.notify(ObjectCreatedEvent(engine))
            self[ct.name] = engine

        return self[ct.name]

    def update(self, content):
        oid = getUtility(IIntIds).queryId(content)
        if not oid:
            return

        tags = self._normalize(IContentTags(content).tags)

        # default and content type engines
        engines = [self.globalEngine, self.engineForContent(content)]

        for name, engine in self.items():
            engine.updateContent(content, oid, tags)

    def remove(self, content):
        oid = getUtility(IIntIds).queryId(content)
        if not oid:
            return

        for name, engine in self.items():
            engine.removeContent(content, oid)

    def _normalize(self, cttags):
        tags = []

        for tag in cttags:
            tag = tag.lower().strip()
            if tag:
                tags.append(tag)

        return tags
