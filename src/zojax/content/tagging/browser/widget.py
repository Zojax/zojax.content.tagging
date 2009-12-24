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
from zope import interface, schema, component
from zope.component import getUtility
from zope.security.proxy import removeSecurityProxy
from zope.app.component.hooks import getSite

from z3c.form import converter
from z3c.form.browser import text
from z3c.form.widget import FieldWidget
from z3c.form.interfaces import IFormLayer, IFieldWidget

from zojax.content.tagging.field import ITagsField
from zojax.content.tagging.browser.interfaces import ITagsWidget
from zojax.content.tagging.interfaces import IContentTaggingConfiglet


class TagsWidget(text.TextWidget):
    interface.implements(ITagsWidget)

    klass = u'z-widget-tags'

    def popularTags(self):
        engine = removeSecurityProxy(
            getUtility(IContentTaggingConfiglet).globalEngine)

        idx = 1
        tags = []
        for weight, tag in engine.getTagCloud(True):
            tags.append(tag)
            if idx == 10:
                break
            idx += 1

        return tags


class TagsWidgetConverter(converter.BaseDataConverter):
    component.adapts(ITagsField, TagsWidget)

    def toWidgetValue(self, value):
        """See interfaces.IDataConverter"""
        if value is self.field.missing_value:
            return u''
        return u', '.join(value)

    def toFieldValue(self, value):
        """See interfaces.IDataConverter"""
        res = []
        for tag in (v for v in (v.strip() for v in value.split(',')) if v):
            if tag not in res:
                res.append(tag)
        return tuple(res)


@interface.implementer(IFieldWidget)
@component.adapter(ITagsField, IFormLayer)
def TagsFieldWidget(field, request):
    return FieldWidget(field, TagsWidget(request))
