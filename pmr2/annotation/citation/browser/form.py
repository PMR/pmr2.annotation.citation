import zope.component
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from plone.z3cform import layout
from plone.app.z3cform.wysiwyg.widget import WysiwygFieldWidget
import z3c.form
from z3c.form.interfaces import INPUT_MODE

from pmr2.app.browser import form
from pmr2.app.browser.layout import PlainLayoutWrapper
from pmr2.app.browser.interfaces import IObjectIdMixin

from pmr2.app.exposure.browser import ExposureFileViewBase

from pmr2.annotation.citation.interfaces import ILicense
from pmr2.annotation.citation.content import License


class LicenseAddForm(form.AddForm):
    """\
    The source text viewer class.
    """

    clsobj = License
    fields = \
        z3c.form.field.Fields(IObjectIdMixin).select(
            'id',
        ) + \
        z3c.form.field.Fields(ILicense).select(
            'title',
            'license_uri',
            'portlet_text',
        )
    fields['portlet_text'].widgetFactory[INPUT_MODE] = WysiwygFieldWidget

    def add_data(self, ctxobj):
        ctxobj.setTitle(self._data['title'])
        ctxobj.license_uri = self._data['license_uri']

LicenseAddFormView = layout.wrap_form(LicenseAddForm, 
    __wrapper_class=PlainLayoutWrapper)


class LicenseEditForm(form.EditForm):
    """\
    The source text viewer class.
    """

    fields = z3c.form.field.Fields(ILicense).select(
        'license_uri',
        'portlet_text',
    )
    fields['portlet_text'].widgetFactory[INPUT_MODE] = WysiwygFieldWidget

LicenseEditFormView = layout.wrap_form(LicenseEditForm, 
    __wrapper_class=PlainLayoutWrapper)


class LicenseCitationNote(ExposureFileViewBase):
    """\
    The citation viewer.
    """

LicenseCitationNoteView = layout.wrap_form(LicenseCitationNote, 
    __wrapper_class=PlainLayoutWrapper)
