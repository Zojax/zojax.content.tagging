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
from zope import component
from zope.component import getUtility
from zope.proxy import removeAllProxies
from zope.app.intid.interfaces import IIntIds
from zope.app.intid.interfaces import IIntIdAddedEvent, IIntIdRemovedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

from interfaces import IContentTaggable, IContentTaggingConfiglet


@component.adapter(IContentTaggable, IIntIdAddedEvent)
def objectAdded(object, event):
    objectModified(object, event)


@component.adapter(IContentTaggable, IObjectModifiedEvent)
def objectModified(object, event):
    getUtility(IContentTaggingConfiglet).update(removeAllProxies(object))


@component.adapter(IContentTaggable, IIntIdRemovedEvent)
def objectRemoved(object, event):
    getUtility(IContentTaggingConfiglet).remove(removeAllProxies(object))
