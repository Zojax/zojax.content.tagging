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
from zope.component import getUtility
from zope.security.proxy import removeSecurityProxy
from zope.traversing.browser import absoluteURL
from zope.app.component.hooks import getSite

from interfaces import IContentTaggingPortlet, IContentTaggingConfiglet


class ContentTaggingPortlet(object):
    interface.implements(IContentTaggingPortlet)

    engine = None
    engineObject = None
    siteUrl = None

    def listTags(self):
        idx = 0
        tags = []
        engine = removeSecurityProxy(self.engineObject)
        for weight, tag in engine.getTagCloud(True):
            weight = weight+100.0
            tags.append({'tag': tag, 'weight': '%0.2f'%weight, 'wvalue': weight})
            if idx == self.count:
                break
            idx += 1

        return tags

    def isAvailable(self):
        return self.engineObject is not None

    def update(self):
        configlet = getUtility(IContentTaggingConfiglet)

        engineObject = None
        if self.engine:
            engineObject = configlet.get(self.engine)

        if engineObject is None:
            engineObject = configlet.globalEngine
            self.engine = engineObject.__name__

        self.engineObject = engineObject
        self.siteUrl = absoluteURL(getSite(), self.request)

        super(ContentTaggingPortlet, self).update()
