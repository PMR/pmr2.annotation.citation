from Products.CMFPlone import interfaces as plone_interfaces
from Products import GenericSetup
from Products.CMFCore import utils as cmfutils
from Products.Archetypes import atapi
from Products.CMFCore.permissions import \
    AddPortalContent as ADD_CONTENT_PERMISSION
from Products.PluggableAuthService.PluggableAuthService import \
    registerMultiPlugin

def initialize(context):
    """Initializer called when used as a Zope 2 product."""

    from pmr2.app import content

    content_types, constructors, ftis = atapi.process_types(atapi.listTypes('pmr2.annotation.citation'), 'pmr2.annotation.citation')

    cmfutils.ContentInit(
        'pmr2.annotation.citation Content',
        content_types = content_types,
        permission = ADD_CONTENT_PERMISSION,
        extra_constructors = constructors,
        fti = ftis,
        ).initialize(context)

from z3c.form.field import Fields
from z3c.form.interfaces import INPUT_MODE
from plone.app.z3cform.wysiwyg.widget import WysiwygFieldWidget

from pmr2.app.annotation import note_factory
from pmr2.app.settings import settings_factory
from pmr2.annotation.citation.interfaces import IPluginSettings
from note import *

LicenseCitationNoteFactory = note_factory(LicenseCitationNote,
                                          'license_citation')

fields = Fields(IPluginSettings, prefix='license_citation')
fields['license_citation.citation_instruction'].widgetFactory[INPUT_MODE] = \
    WysiwygFieldWidget

PluginSettingsFactory = settings_factory(PluginSettings, 
                                         'license_citation',
                                         u'License and Citation Settings',
                                         fields,)
