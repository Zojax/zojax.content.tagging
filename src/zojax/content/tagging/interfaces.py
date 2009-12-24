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
from zope import interface, schema
from zope.i18nmessageid import MessageFactory
from zojax.widget.radio.field import RadioChoice
from zojax.content.tagging.field import TagsField
from zojax.content.feeds.interfaces import IRSS2Feed
from zojax.content.type.interfaces import IItem, IUnremoveableContent

_ = MessageFactory('zojax.content.tagging')


class IContentTags(interface.Interface):

    tags = TagsField(
        title = _('Tags'),
        description = _('Think of a tag as a simple category name. You can categorize your documents, files, and blog posts with any word or words that makes sense.'),
        required = False)


class IContentTaggable(interface.Interface):
    """Marker interface for taggable content."""


class IContentTaggingConfiglet(interface.Interface):
    """Content tagging configlet """

    globalEngine = interface.Attribute('All content types tags')

    def getEngine(content):
        """Return tagging engine for content."""

    def getContentTypeEngine(ct):
        """Return tagging engine for content type."""

    def listTaggableContentTypes():
        """Return list of taggable content types."""

    def update(content):
        """Update tags for content."""

    def remove(content):
        """Remove content from tagging engine."""


class IContentTaggingEngineType(IItem):
    """ content tagging engine type """


class IContentTaggingEngineBase(IItem):
    """Content tagging engine"""

    title = interface.Attribute('Title')

    def updateContent(content, oid, tags):
        """ update content tags """

    def removeContent(content, oid):
        """ remove content """

    def getTagCloud(reverse=False):
        """check ITaggingEngine.getTagCloud"""


class IContentTaggingEngine(IUnremoveableContent):
    """ content type engine """


class IGlobalTaggingEngine(IUnremoveableContent):
    """ global engine """


class IContentTaggingPortlet(interface.Interface):
    """ Content tagging portlet """

    label = schema.TextLine(
        title = _(u'Label'),
        required = False)

    count = schema.Int(
        title = _(u'Tags count'),
        description = _('Number of tags in portlet.'),
        default = 20,
        required = True)

    engine = RadioChoice(
        title = _(u'Tagging engine'),
        description = _(u'Select tagging enging to use in this portlet.'),
        vocabulary = 'content.tagging.egines',
        default = '',
        required = True)


class ITagsRSSFeed(IRSS2Feed):
    """ tags rss feed """
