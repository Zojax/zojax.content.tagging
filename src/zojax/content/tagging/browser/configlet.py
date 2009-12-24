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
from zope.component import getUtility
from zope.proxy import removeAllProxies
from zope.app.intid.interfaces import IIntIds
from zojax.statusmessage.interfaces import IStatusMessage
from zojax.content.tagging.interfaces import _, IContentTaggable


class ConfigletView(object):

    def rebuild(self):
        for key, object in getUtility(IIntIds).items():
            if IContentTaggable.providedBy(object):
                self.context.update(removeAllProxies(object))

        IStatusMessage(self.request).add(_(u'Tags have been updated.'))
        self.request.response.redirect('context.html')
