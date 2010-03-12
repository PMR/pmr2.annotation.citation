import zope.interface
import zope.component
from zope.schema import fieldproperty
from Products.Archetypes import atapi
from Products.ATContentTypes.atct import ATBTreeFolder
from Products.ATContentTypes.atct import ATDocument
from Products.CMFCore.permissions import View

from pmr2.annotation.citation.interfaces import ILicense


# XXX rather than defining a new archetype, use annotation.
# use annotation to attach to an existing page
# the license annotation view is only enabled for specific folders
#

class License(ATDocument):
    """\
    Generic object within an exposure that represents a file in the
    workspace, and as an anchor for adapted content.
    """

    zope.interface.implements(ILicense)

    # Provided by Archetype
    # title = fieldproperty.FieldProperty(ILicense['title'])
    # description = fieldproperty.FieldProperty(ILicense['description'])

    license_uri = fieldproperty.FieldProperty(ILicense['license_uri'])

# type registration
atapi.registerType(License, 'pmr2.annotation.citation')

def catalog_content(obj, event):
    # for the subscriber event.
    obj.reindexObject()
