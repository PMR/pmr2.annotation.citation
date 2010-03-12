import zope.interface
import zope.component

from pmr2.app.factory import named_factory
from pmr2.app.annotation.interfaces import IExposureFileAnnotator
from pmr2.app.annotation.interfaces import IExposureFilePostEditAnnotator
from pmr2.app.annotation.annotator import ExposureFileAnnotatorBase

from pmr2.annotation.citation.interfaces import *


class LicenseCitationAnnotator(ExposureFileAnnotatorBase):
    zope.interface.implements(IExposureFileAnnotator, 
                              IExposureFilePostEditAnnotator)
    title = u'License and Citation'
    label = u'Cite this model'
    description = u''

    def generate(self):
        note = self.note
        #format, license_path, dcterms:license
        results = []
        if note.format:
            # a format is defined, we get a utility of some sort to
            # generate the values below.
            u = zope.component.queryUtility(ICitationFormat, name=note.format)
            if u is None:
                # something is wrong...
                pass
            else:
                # this may also provide the license_path if it has been
                # correctly added to the site.
                license_path, dcterms_license = u(self.context)()
                results.append(('license_path', license_path,))
                results.append(('dcterms_license', dcterms_license,))
        elif note.license_path:
            # XXX use catalog to pick up the dcterms:license
            license = self.context.restrictedTraverse(note.license_path)
            results.append(('dcterms_license', license.license_uri,))
        return results

LicenseCitationAnnotatorFactory = named_factory(LicenseCitationAnnotator)
