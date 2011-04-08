from persistent import Persistent
import zope.interface
import zope.component
from zope.schema import fieldproperty
from zope.app.container.contained import Contained

from pmr2.app.settings.interfaces import IPMR2GlobalSettings
from pmr2.app.settings import settings_factory

from pmr2.app.annotation.note import RawTextNote
from pmr2.app.annotation.note import ExposureFileNoteBase
from pmr2.app.annotation.note import ExposureFileEditableNoteBase

from pmr2.annotation.citation.interfaces import *


class LicenseCitationNote(ExposureFileEditableNoteBase):
    """\
    Points to the OpenCell session attached to this file.
    """

    zope.interface.implements(ILicenseCitationNote)
    format = fieldproperty.FieldProperty(ILicenseCitationNote['format'])
    license_path = fieldproperty.FieldProperty(ILicenseCitationNote['license_path'])
    dcterms_license = fieldproperty.FieldProperty(ILicenseCitationNote['dcterms_license'])


class PluginSettings(Persistent, Contained):
    zope.interface.implements(IPluginSettings)
    zope.component.adapts(IPMR2GlobalSettings)
    #title = u'Citation and Annotation Settings'
    default_license_path = zope.schema.fieldproperty.FieldProperty(
        IPluginSettings['default_license_path'])
    citation_instruction = zope.schema.fieldproperty.FieldProperty(
        IPluginSettings['citation_instruction'])
