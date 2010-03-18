from zope import schema
from zope.formlib import form
from zope.interface import implements
import zope.component
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFCore.utils import getToolByName

from pmr2.app.interfaces import *
from pmr2.app.content.interfaces import *
from pmr2.app.annotation.factory import has_note
from pmr2.annotation.citation.utility import getLicensePortletText


class ILicensePortlet(IPortletDataProvider):
    """\
    Exposure Information portlet.
    """


class Assignment(base.Assignment):
    implements(ILicensePortlet)

    def __init__(self):
        pass

    @property
    def title(self):
        return _(u'License')


class Renderer(base.Renderer):
    _template = ViewPageTemplateFile('license.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)
        self.title = u'License'

    @property
    def license(self):
        # doing this to avoid accidentally annotate.
        uri = None
        if self.available:
            note = zope.component.queryAdapter(self.context, 
                name='license_citation')
            if note:
                uri = note.dcterms_license
        return getLicensePortletText(self.context, uri)

    @property
    def available(self):
        return has_note(self.context, 'license_citation')

    def render(self):
        return self._template()


class AddForm(base.AddForm):
    form_fields = form.Fields(ILicensePortlet)
    label = _(u"Add PMR2 License Portlet")
    description = _(u"This portlet displays License information from the Citation/License note.")

    def create(self, data):
        return Assignment()


class EditForm(base.EditForm):
    form_fields = form.Fields(ILicensePortlet)
    label = _(u"Edit Exposure Source Portlet")
    description = _(u"This portlet displays curation information about an Exposure, but using PMR1 style.")

