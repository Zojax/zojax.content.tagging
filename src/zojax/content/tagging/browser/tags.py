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
from zope.app.component.hooks import getSite
from zope.component import getUtility, queryMultiAdapter
from zope.proxy import removeAllProxies
from zope.location import LocationProxy
from zope.publisher.interfaces import NotFound
from zope.schema.interfaces import IVocabularyFactory
from zope.traversing.browser import absoluteURL

from zojax.content.tagging.interfaces import IContentTaggingConfiglet, IContentTags


class TagsWorkspace(object):

    def update(self):
        if self.request._traversed_names[-1] != '':
            self.request._traversed_names.append('')

        self.voc = getUtility(
            IVocabularyFactory, 'content.tagging.egines')(self.context)

        super(TagsWorkspace, self).update()

    def publishTraverse(self, request, name):
        view = queryMultiAdapter((self, request), name=name)
        if view is not None:
            return view

        configlet = getUtility(IContentTaggingConfiglet)

        if name == 'global':
            engine = configlet.globalEngine
        else:
            engine = configlet.get(name)

        if engine is not None:
            return LocationProxy(engine, self, name)

        raise NotFound(self, name, request)


class Tags(object):

    def update(self):
        self.tags = IContentTags(self.context).tags
        self.site_url = absoluteURL(getSite(), self.request)

    def isAvailable(self):
        return bool(self.tags)
