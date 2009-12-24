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
import time, rfc822
from zope import interface, component
from zope.component import getUtility
from zope.traversing.browser import absoluteURL
from zope.dublincore.interfaces import IDCTimes
from zope.app.component.interfaces import ISite
from zope.security.proxy import removeSecurityProxy

from zojax.tagging.index import TagIndex
from zojax.catalog.interfaces import ICatalog
from zojax.content.feeds.rss2 import RSS2Feed

from interfaces import _, ITagsRSSFeed, IContentTaggingConfiglet
from zojax.content.tagging.browser.engine import TagWrapper


class TagsRSSFeed(RSS2Feed):
    component.adapts(ISite)
    interface.implementsOnly(ITagsRSSFeed)

    name = u'tags'
    title = _(u'Tags')
    description = _(u'List of all available tags.')

    def items(self):
        request = self.request
        configlet = getUtility(IContentTaggingConfiglet)
        engine = removeSecurityProxy(configlet).globalEngine

        url = '%s/@@tags/global'%absoluteURL(self.context, request)

        for weight, tag in engine.getTagCloud(True):
            yield {
                'title': tag,
                'description': _('Total number of items for this tag is ${number}',
                                 mapping={'number': len(engine.getItems((tag,)))}),
                'guid': '%s/%s/'%(url, tag),
                'isPermaLink': True}


class TagItemsRSSFeed(RSS2Feed):
    component.adapts(TagWrapper)
    interface.implementsOnly(ITagsRSSFeed)

    name = u'content'
    title = _(u'Tag content')
    description = _(u'List of content for tag.')

    def items(self):
        request = self.request
        configlet = getUtility(IContentTaggingConfiglet)
        engine = removeSecurityProxy(configlet).globalEngine

        contents = getUtility(ICatalog).searchResults(
            contentTagging={'any_of': (self.context.__name__,)},
            sort_on='modified', sort_order='reverse',
            indexes={'contentTagging': TagIndex(engine)},
            isDraft={'any_of': (False,)})

        url = '%s/@@tags/global'%absoluteURL(self.context, request)

        for content in contents[:15]:
            yield {
                'title': content.title,
                'description': content.description,
                'guid': '%s/'%absoluteURL(content, request),
                'isPermaLink': True,
                'pubDate': rfc822.formatdate(time.mktime(
                        IDCTimes(content).modified.timetuple())),}
