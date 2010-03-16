import zope.interface
from Products.CMFCore.utils import getToolByName

from pmr2.app.factory import NamedUtilBase
from pmr2.app.interfaces import IPMR2GlobalSettings
from pmr2.annotation.citation.interfaces import *

def getLicenses(context):
    """\
    Returns the set of license documents created for this site.
    """

    pt = getToolByName(context, 'portal_catalog')
    results = pt(state='published', portal_type='License')
    return results

def getLicenseText(context):
    """\
    Generate the correct copyright/licensing string for rendering.
    """

    unknown = 'The license information is unknown.'
    default = 'The license information can be found in '


class CitationFormatterBase(NamedUtilBase):
    """\
    The base utility that will be subclassed to enable extraction of
    citation and licensing information from its source file.
    """

    zope.interface.implements(ICitationFormat)

    def __init__(self, context):
        self.context = context

    def extract(self):
        """\
        Implement this method to extract dcterms:license from the source
        file.
        """

        raise NotImplementedError

    def __call__(self):
        """\
        Returns the dcterms:license from the file, and the absolute path
        to the locally defined license if available.
        """

        # look up the catalog for its path
        license_path = None
        dcterms_license = self.extract()

        if dcterms_license:
            pt = getToolByName(self.context, 'portal_catalog')
            results = pt(state='published', portal_type='License',
                pmr2_license_uri=dcterms_license)
            if results:
                # XXX assume first one
                # XXX there might be cases where two license objects are
                # defined with the same dcterms_license.
                license_path = results[0].getPath()
        else:
            # we didn't get one, so we check whether global settings has 
            # a default one specified.
            pmr2_settings = zope.component.getUtility(IPMR2GlobalSettings)
            citation_settings = IPluginSettings(pmr2_settings)
            license_path = citation_settings.default_license_path
            if license_path:
                dcterms_license = self.context.restrictedTraverse(
                    citation_settings.default_license_path).license_uri

        return (license_path, dcterms_license)
