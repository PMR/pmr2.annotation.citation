from xml.sax.saxutils import escape, quoteattr
import zope.interface
from zope.app.component.hooks import getSite

from Products.CMFCore.utils import getToolByName
from Products.PortalTransforms.data import datastream

from pmr2.app.factory import NamedUtilBase
from pmr2.app.settings.interfaces import IPMR2GlobalSettings
from pmr2.annotation.citation.interfaces import *

def getLicenses(context, **kw):
    """\
    Returns the set of license documents created for this site.
    """

    base_query = {
        'review_state': 'published',
        'portal_type': 'License',
    }

    kw.update(base_query)
    try:
        pt = getToolByName(context, 'portal_catalog')
    except AttributeError:
        # we try another way...
        site = getSite()
        pt = getToolByName(site, 'portal_catalog')

    results = pt(**kw)
    return results

def getLicensePortletText(context, uri):
    """\
    Generates a brief terms of use/license description that is based on
    the input uri for use by the portlet.
    """

    if not uri:
        return u'The terms of use/license for this work is unspecified.'

    # get the URI from the object
    results = getLicenses(context, pmr2_license_uri=uri)
    license = None
    if results:
        # Assume the first one.
        license = results[0].getObject()
        if license.portlet_text:
            pt = getToolByName(input, 'portal_transforms')
            stream = datastream('license_description')
            pt.convert('safe_html', license.portlet_text, stream)
            return stream.getData()

    # template undefined, we generate one.
    # XXX ideally this should be a proper template/view.
    license_template = \
        u'The terms of use for this work and/or license this work is under ' \
         'is: <a href=%s>%s</a>.'

    title = license and license.title or escape(uri)
    return license_template % (quoteattr(uri), title)


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
            results = getLicenses(self.context, 
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
                results = getLicenses(self.context, 
                    path=citation_settings.default_license_path)
                if results:
                    dcterms_license = results[0].pmr2_license_uri

        return (license_path, dcterms_license)
