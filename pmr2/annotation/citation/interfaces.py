import zope.interface
import zope.schema


class ILicenseCitationNote(zope.interface.Interface):
    """\
    A note for storage of citation and licensing terms.
    """

    # citation format method?
    format = zope.schema.Choice(
        title=u'File/Citation Format',
        description=u'Select the correct method to generate the citation and '
                     'license information from the source file.  Overwrites '
                     'the values below.',
        vocabulary=u'pmr2.annotation.citation.CitationFormat',
        required=False,
    )

    license_path = zope.schema.Choice(
        title=u'License',
        description=u'The license this work is licensed under.  Will be '
                     'overwritten if Citation For is specified.',
        vocabulary=u'pmr2.annotation.citation.LicenseType',
        required=False,
    )

    dcterms_license = zope.schema.TextLine(
        title=u'dcterms:license',
        description=u'The link to the license this model is licensed under. '
                     'It is automatically assigned if one of the assignment '
                     'methods above is set.',
        required=False,
    )


class ICitationFormat(zope.interface.Interface):
    """\
    Defines a kind of citation, such as for which file type. 
    """

    title = zope.schema.TextLine(
        title=u'Title',
    )

    def extract():
        """\
        This method will extract citation and license information from
        an ExposureFile context, which provides source material.
        
        Example would include extraction of the license URI.
        """


class ILicense(zope.interface.Interface):
    """\
    """

    title = zope.schema.TextLine(
        title=u'Title',
        description=u'The title or name of this license.',
    )

    description = zope.schema.Text(
        title=u'Description',
        description=u'A brief description of this license.',
    )

    portlet_text = zope.schema.Text(
        title=u'Portlet Text',
        description=u'The text that will be shown on the sidebar for work '
                     'using this license.',
    )

    license_uri = zope.schema.TextLine(
        title=u'URI of this license',
        description=u'The URI of the official definition of this license '
                     '(e.g. http://creativecommons.org/licenses/by/3.0/). '
                     'If its official definition is this very document, '
                     'please leave this field blank.',
        required=False,
    )


class IPluginSettings(zope.interface.Interface):

    default_license_path = zope.schema.Choice(
        title=u'Default License',
        description=u'If selected, the file will be the default license for '
                     'all work within PMR2.',
        vocabulary=u'pmr2.annotation.citation.LicenseType',
        required=False,
    )

