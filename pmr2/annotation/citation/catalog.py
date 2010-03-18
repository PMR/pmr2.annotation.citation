import zope.interface
from plone.indexer import indexer
from Products.CMFCore.utils import getToolByName

from pmr2.app.interfaces import IExposureSourceAdapter, IPMR2KeywordProvider

from pmr2.annotation.citation.interfaces import *

# Apply to all exposure objects

@indexer(ILicense)
def license_uri(context):
    if context.license_uri:
        return context.license_uri
    return unicode(context.absolute_url())
