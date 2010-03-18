=====================================
Citation and License Display for PMR2
=====================================

Since PMR2 is primarily used as a platform to distribute models, these
work are almost always under some sort of copyright.  Most cases at the
moment the models are going to be placed under the various Creative 
Commons license types, but in the future there may be other licenses
that will need to be supported.

To facilitate this, we will have Licence document types, it will be
registered as a Archetype so it can be queried via the catalog.  This
will be important as users will be able to add their own licenses using
the standard Plone editors, and then be approved for usage via standard
workflow states.

Do note, these work as a form of templates to generate the correct
copyright and license text for the result documents.

We first add a couple licenses using its add form.
::

    >>> import zope.component
    >>> from Products.ATContentTypes.content.folder import ATFolder
    >>> from pmr2.app.tests.base import TestRequest
    >>> from pmr2.annotation.citation.browser import form
    >>> lid = 'licenses'
    >>> self.portal[lid] = ATFolder(lid)
    >>> licenses = self.portal.licenses
    >>> request = TestRequest(
    ...     form={
    ...         'form.widgets.id': u'test_license',
    ...         'form.widgets.title': u'Test License',
    ...         'form.widgets.license_uri': u'http://example.com/license',
    ...         'form.buttons.add': 1,
    ...     })
    >>> testform = form.LicenseAddForm(licenses, request)
    >>> result = testform()
    >>> tl = licenses['test_license']
    >>> tl
    <License ...>
    >>> tl.license_uri
    u'http://example.com/license'
    >>> lid2 = 'licenses2'
    >>> self.portal[lid2] = ATFolder(lid2)
    >>> licenses = self.portal.licenses
    >>> request = TestRequest(
    ...     form={
    ...         'form.widgets.id': u'test_license_2',
    ...         'form.widgets.title': u'Test License 2',
    ...         'form.widgets.license_uri': u'http://example.com/license_2',
    ...         'form.buttons.add': 1,
    ...     })
    >>> testform = form.LicenseAddForm(licenses, request)
    >>> result = testform()
    >>> tl2 = licenses['test_license_2']
    >>> tl2
    <License ...>
    >>> tl2.license_uri
    u'http://example.com/license_2'

Now that we have a license defined for use, an ExposureFile and note can
be created.  We test the form to see that the selection box has the
above license as an available choice.
::

    >>> from pmr2.app.content import ExposureFile
    >>> from pmr2.app.browser.exposure import ExposureFileNoteEditForm
    >>> self.portal.f = ExposureFile('f')
    >>> filectx = self.portal.f
    >>> request = TestRequest()
    >>> view = ExposureFileNoteEditForm(filectx, request)
    >>> view.traverse_subpath = ['license_citation']
    >>> result = view()

The actual path must not be rendered in the output, but the title is
used as both token and value.  This is dependent on the vocab 
definition.
::

    >>> u'/plone/licenses/test_license' in result
    False
    >>> u'Test License' in result
    True

Now we use the annotator form to assign the license to the note attached
to the file.
::

    >>> from pmr2.app.browser.exposure import ExposureFileNoteEditForm
    >>> from pmr2.app.annotation.interfaces import IExposureFileNote
    >>> request = TestRequest(
    ...     form={
    ...         'form.widgets.format': [],
    ...         'form.widgets.license_path': [u'Test License'],
    ...         'form.widgets.dcterms_license': u'',
    ...         'form.buttons.apply': 1,
    ...     })
    >>> view = ExposureFileNoteEditForm(filectx, request)
    >>> view.traverse_subpath = ['license_citation']
    >>> result = view()
    >>> 'updated' in result
    True

The values must match.  Note that the path and not the token value is
stored within the note.
::

    >>> note = zope.component.queryAdapter(filectx, name='license_citation')
    >>> note.license_path
    '/plone/licenses/test_license'
    >>> note.dcterms_license
    u'http://example.com/license'

When revisiting that form, the values should have been selected.
::

    >>> request = TestRequest()
    >>> view = ExposureFileNoteEditForm(filectx, request)
    >>> view.traverse_subpath = ['license_citation']
    >>> result = view()
    >>> 'selected="selected">Test License' in result
    True

Of course, there will be cases where the license information is
provided by the source file (in the dcterms:license node within the
file).  Modules can implement their own CitationFormatter utilities to
extract the license information.  These extractors will be user
selectable as they will determine the file/metadata format.

As we are working with a standalone file, no data is provided so the
method within the defined extraction demo classes method will return a 
dummy license string.
::

    >>> from pmr2.annotation.citation.utility import CitationFormatterBase
    >>> from pmr2.annotation.citation.interfaces import ICitationFormat
    >>> class TestCitationFormatterOne(CitationFormatterBase):
    ...     title = 'Test Format One'
    ...     def extract(self):
    ...         return u'http://example.com/null'
    ... 
    >>> class TestCitationFormatterTwo(CitationFormatterBase):
    ...     title = 'Test Format Two'
    ...     def extract(self):
    ...         return u'http://example.com/license'
    ...
    >>> sm = self.portal.getSiteManager()
    >>> sm.registerUtility(TestCitationFormatterOne, ICitationFormat,
    ...     name='citation_one')
    >>> sm.registerUtility(TestCitationFormatterTwo, ICitationFormat,
    ...     name='citation_two')

After they are registered, we can render the edit form.  Those utlities 
should now be selectable by the form.
::

    >>> request = TestRequest()
    >>> view = ExposureFileNoteEditForm(filectx, request)
    >>> view.traverse_subpath = ['license_citation']
    >>> result = view()
    >>> u'Test Format One' in result
    True
    >>> u'Test Format Two' in result
    True

If we select the first format, it returns a license that has not been
added to the portal.  It should now null the already set license_path,
and assign dcterms_license to the new uri.
::

    >>> request = TestRequest(
    ...     form={
    ...         'form.widgets.format': [u'citation_one'],
    ...         'form.widgets.license_path': [u'Test License'],
    ...         'form.widgets.dcterms_license': u'',
    ...         'form.buttons.apply': 1,
    ...     })
    >>> view = ExposureFileNoteEditForm(filectx, request)
    >>> view.traverse_subpath = ['license_citation']
    >>> result = view()
    >>> note = zope.component.queryAdapter(filectx, name='license_citation')
    >>> note.format
    u'citation_one'
    >>> note.license_path is None
    True
    >>> note.dcterms_license
    u'http://example.com/null'

The second first format should set the path and all related values.
::

    >>> request = TestRequest(
    ...     form={
    ...         'form.widgets.format': [u'citation_two'],
    ...         'form.widgets.license_path': [u'Test License'],
    ...         'form.widgets.dcterms_license': u'',
    ...         'form.buttons.apply': 1,
    ...     })
    >>> view = ExposureFileNoteEditForm(filectx, request)
    >>> view.traverse_subpath = ['license_citation']
    >>> result = view()
    >>> note = zope.component.queryAdapter(filectx, name='license_citation')
    >>> note.format
    u'citation_two'
    >>> note.license_path
    '/plone/licenses/test_license'
    >>> note.dcterms_license
    u'http://example.com/license'

---------------
Plugin Settings
---------------

This plugin provides the ability to store default settings via the
pluggable PMR2 settings infrastructure.
::

    >>> from pmr2.app.browser.settings import PMR2GlobalSettingsEditForm
    >>> from pmr2.app.tests.base import TestRequest
    >>> from pmr2.app.tests.browser import GroupTemplate
    >>> request = TestRequest()
    >>> f = PMR2GlobalSettingsEditForm(self.portal, request)
    >>> f.template = GroupTemplate(f)
    >>> result = f()
    >>> 'license_citation.default_license_path' in result
    True
    >>> u'Test License' in result
    True
    >>> u'Test License 2' in result
    True

We should be able to use this form, which provides a list of available
licenses, to define the default license we want to use.  However, we
won't test the functionality of the form itself since there are likely
other fields registered, we are going to change the settings manually.
::

    >>> from pmr2.app.interfaces import IPMR2GlobalSettings
    >>> from pmr2.annotation.citation.interfaces import IPluginSettings
    >>> pmr2_settings = zope.component.getUtility(IPMR2GlobalSettings)
    >>> citation_settings = IPluginSettings(pmr2_settings)
    >>> citation_settings.default_license_path = \
    ...     '/plone/licenses/test_license_2'

We should be able to register a formatter that returns no address, and
the default address be assigned.
::

    >>> class TestCitationFormatterThree(CitationFormatterBase):
    ...     title = 'Test Format One'
    ...     def extract(self):
    ...         return None
    ... 
    >>> sm.registerUtility(TestCitationFormatterThree, ICitationFormat,
    ...     name='citation_three')

Then we use this new formatter.
::

    >>> request = TestRequest(
    ...     form={
    ...         'form.widgets.format': [u'citation_three'],
    ...         'form.widgets.license_path': [],
    ...         'form.widgets.dcterms_license': u'',
    ...         'form.buttons.apply': 1,
    ...     })
    >>> view = ExposureFileNoteEditForm(filectx, request)
    >>> view.traverse_subpath = ['license_citation']
    >>> result = view()
    >>> note = zope.component.queryAdapter(filectx, name='license_citation')
    >>> note.format
    u'citation_three'
    >>> note.license_path
    '/plone/licenses/test_license_2'
    >>> note.dcterms_license
    u'http://example.com/license_2'
