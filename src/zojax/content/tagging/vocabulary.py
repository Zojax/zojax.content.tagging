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
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from zope.schema.interfaces import IVocabulary, IVocabularyFactory

from interfaces import IContentTaggingConfiglet


class Vocabulary(SimpleVocabulary):

    def getTerm(self, value):
        try:
            return self.by_value[value]
        except KeyError:
            return self.by_value[self.by_value.keys()[0]]


class TaggingEnginesVocabulary(object):
    interface.implements(IVocabularyFactory)

    def __call__(self, context):
        configlet = getUtility(IContentTaggingConfiglet)

        engines = {}
        for engine in configlet.contentTypesEngines():
            engines[engine.__name__] = engine

        for name, engine in configlet.items():
            if name not in engines and name != 'global':
                engines[name] = engine

        terms = []
        for name, engine in engines.items():
            term = SimpleTerm(name, name, engine.title)
            term.description = engine.description
            terms.append((engine.title, name, term))
        terms.sort()

        engine = configlet.globalEngine
        default = SimpleTerm('global', 'global', engine.title)
        default.description = engine.description

        return Vocabulary([default] + [term for t,n,term in terms])
