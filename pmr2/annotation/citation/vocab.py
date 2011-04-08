# store values reachable via restrictedTraverse
import zope.interface
import zope.component

from zope.schema.interfaces import IVocabulary, IVocabularyFactory, ISource
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from Products.CMFCore.utils import getToolByName

from pmr2.app.factory import vocab_factory
from pmr2.app.settings.interfaces import IPMR2GlobalSettings
from pmr2.app.annotation.interfaces import *
from pmr2.annotation.citation.utility import getLicenses
from pmr2.annotation.citation.interfaces import *


class CitationFormat(SimpleVocabulary):
    """
    Retrieves a list of License documents stored within the CMS.
    """

    def __init__(self, context):
        self.context = context
        try:
            # If the context passed into here is unbounded, it won't have
            # a catalog to validate against.
            values = [(i[0], i[0], i[1].title) for i in
                zope.component.getUtilitiesFor(ICitationFormat)]
        except:
            values = []
        # XXX wrong
        terms = [SimpleTerm(*v) for v in values]
        super(CitationFormat, self).__init__(terms)

    def getTerm(self, value):
        try:
            return super(CitationFormat, self).getTerm(value)
        except LookupError:
            # should log the no longer registered utility.
            return SimpleTerm(value)

CitationFormatVocabFactory = vocab_factory(CitationFormat)


class LicenseType(SimpleVocabulary):
    """
    Retrieves a list of License documents stored within the CMS.
    """

    def __init__(self, context):
        self.context = context
        self.pt = None
        try:
            ctx = self.context
            # Since this is primarily used within notes, we check to see
            # whether to pass its parent (the ExposureFile) to get the
            # list of licenses.
            # XXX might a check for IContained/ILocated(?) be better?
            if IExposureFileNote.providedBy(ctx):
                ctx = ctx.__parent__
            elif IPMR2GlobalSettings.providedBy(ctx):
                ctx = ctx.__parent__
            elif IPluginSettings.providedBy(ctx):
                ctx = ctx.__parent__.__parent__
            values = getLicenses(ctx)
        except:
            values = []
        terms = [SimpleTerm(v.getPath(), v.Title) for v in values]
        super(LicenseType, self).__init__(terms)

    def getTerm(self, value):
        try:
            return super(LicenseType, self).getTerm(value)
        except LookupError:
            # should log the lack of catalog
            return SimpleTerm(value)

LicenseTypeVocabFactory = vocab_factory(LicenseType)
