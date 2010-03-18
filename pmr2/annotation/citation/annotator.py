import zope.interface
import zope.component

from pmr2.app.factory import named_factory
from pmr2.app.annotation.interfaces import IExposureFileAnnotator
from pmr2.app.annotation.interfaces import IExposureFilePostEditAnnotator
from pmr2.app.annotation.annotator import ExposureFileAnnotatorBase

from pmr2.annotation.citation.interfaces import *
from pmr2.annotation.citation.utility import getLicenses


class LicenseCitationAnnotator(ExposureFileAnnotatorBase):
    zope.interface.implements(IExposureFileAnnotator, 
                              IExposureFilePostEditAnnotator)
    title = u'License and Citation'
    label = u'Cite this model'
    description = u''

    def generate(self):
        note = self.note
        results = []

        if note.format:
            # a format is defined, we query for the selected utility to
            # generate the values below.
            u = zope.component.queryUtility(ICitationFormat, name=note.format)
            if u is None:
                # Something is wrong, either bad data or utility 
                # disappeared on us.  Fallback to the next step.
                pass
            else:
                # this may also provide the license_path if it has been
                # correctly added to the site.
                license_path, dcterms_license = u(self.context)()
                results.append(('license_path', license_path,))
                results.append(('dcterms_license', dcterms_license,))
                return results

        if note.license_path:
            license = getLicenses(self.context, path=note.license_path)
            if license:
                results.append(('dcterms_license', 
                                license[0].pmr2_license_uri,))
        return results

LicenseCitationAnnotatorFactory = named_factory(LicenseCitationAnnotator)
