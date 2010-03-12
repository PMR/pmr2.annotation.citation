import zope.component
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from plone.z3cform import layout

from pmr2.app.browser.layout import PlainLayoutWrapper
from pmr2.app.browser.exposure import ExposureFileViewBase


class LicenseCitationNote(ExposureFileViewBase):
    """\
    The source text viewer class.
    """

LicenseCitationNoteView = layout.wrap_form(LicenseCitationNote, 
    __wrapper_class=PlainLayoutWrapper)
