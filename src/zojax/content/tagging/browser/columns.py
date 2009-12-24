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
from zope.interface import Interface
from zope.app.component.hooks import getSite
from zope.traversing.browser import absoluteURL
from zope.app.pagetemplate import ViewPageTemplateFile

from zojax.table.column import Column
from zojax.content.table.interfaces import IContentsTable
from zojax.content.tagging.interfaces import _, IContentTags


class TagsColumn(Column):
    component.adapts(Interface, Interface, IContentsTable)

    weight = 100

    name = 'tags'
    title = _('Tags')
    cssClass = 'ctb-tags'

    template = ViewPageTemplateFile('columntags.pt')

    def query(self, default=None):
        if 'siteUrl' not in self.globalenviron:
            self.globalenviron['siteUrl'] = absoluteURL(getSite(), self.request)

        url = self.globalenviron['siteUrl']

        tags = []
        tagging = IContentTags(self.content, None)
        if tagging is not None:
            tagsurl = '%s/@@tags/global'%self.globalenviron['siteUrl']
            for tag in tagging.tags:
                tags.append((tag, '%s/%s/'%(tagsurl, tag)))

        return tags
