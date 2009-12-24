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
from zope.location import Location
from zope.component import getUtility, queryMultiAdapter
from zope.security.proxy import removeSecurityProxy
from zope.traversing.browser import absoluteURL
from zope.publisher.interfaces import NotFound
from zope.dublincore.interfaces import ICMFDublinCore
from z3c.traverser.interfaces import ITraverserPlugin
from zojax.tagging.index import TagIndex
from zojax.catalog.interfaces import ICatalog


class EngineView(object):

    def listTags(self):
        tags = []
        engine = removeSecurityProxy(self.context)
        for weight, tag in engine.getTagCloud(True):
            tags.append((tag, {'tag': tag, 'weight': '%0.2f'%(weight+100.0)}))

        tags.sort()
        return [info for tag, info in tags]


class EnginePublisher(object):
    interface.implements(ITraverserPlugin)

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self._engine = removeSecurityProxy(context)

    def publishTraverse(self, request, name):
        if name in self._engine:
            return TagWrapper(self._engine, name)

        raise NotFound(self.context, name, request)


class TagWrapper(Location):

    def __init__(self, context, name):
        self.__name__ = name
        self.__parent__ = context


class TagView(object):

    def update(self):
        ctool = getUtility(ICatalog)

        engine = removeSecurityProxy(self.context.__parent__)

        self.contents = ctool.searchResults(
            contentTagging={'any_of': (self.context.__name__,)},
            sort_on='modified', sort_order='reverse',
            indexes={'contentTagging': TagIndex(engine)},
            isDraft={'any_of': (False,)})
        self.total = len(self.contents)

    def getContents(self):
        request = self.request

        for content in self.contents:
            dc = ICMFDublinCore(content)
            parent = content.__parent__

            yield {'title': content.title,
                   'description': content.description,
                   'modified': dc.modified,
                   'url': '%s/'%absoluteURL(content, request),
                   'icon': queryMultiAdapter((content, request), name="zmi_icon"),
                   'parentTitle': getattr(parent, 'title', parent.__name__),
                   'parentDescription': getattr(parent, 'description', u''),
                   'parentURL': absoluteURL(parent, request)}
