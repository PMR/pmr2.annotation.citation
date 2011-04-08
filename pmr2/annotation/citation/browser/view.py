import zope.component
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from plone.z3cform import layout
from Products.CMFCore.utils import getToolByName

from pmr2.app.settings.interfaces import IPMR2GlobalSettings
from pmr2.app.browser.layout import PlainLayoutWrapper

from pmr2.app.exposure.browser.browser import ExposureFileViewBase

from pmr2.annotation.citation.interfaces import IPluginSettings
from pmr2.annotation.citation.utility import getLicensePortletText


class LicenseCitationNote(ExposureFileViewBase):
    """\
    The source text viewer class.
    """

    template = ViewPageTemplateFile('license.pt')

    def update(self):
        self.license_uri = self.note.dcterms_license
        self.license_description = getLicensePortletText(
            self.context, self.license_uri)

    def citation_instruction(self):
        pmr2 = zope.component.getUtility(IPMR2GlobalSettings)
        settings = IPluginSettings(pmr2)
        return settings.citation_instruction

    def __call__(self):
        self.update()
        return self.template()

LicenseCitationNoteView = layout.wrap_form(LicenseCitationNote, 
    __wrapper_class=PlainLayoutWrapper)
