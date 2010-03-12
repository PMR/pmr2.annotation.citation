import unittest

from zope.testing import doctestunit, doctest
from zope.component import testing
from Testing import ZopeTestCase as ztc

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from Products.PloneTestCase.layer import onsetup

from pmr2.annotation.citation.tests import base

def test_suite():
    return unittest.TestSuite([

        # Content tests.
        ztc.ZopeDocFileSuite(
            'README.txt', package='pmr2.annotation.citation',
            test_class=ptc.FunctionalTestCase,
            optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
        ),

        # Content tests.
        ztc.ZopeDocFileSuite(
            'utility.txt', package='pmr2.annotation.citation',
            test_class=ptc.FunctionalTestCase,
            optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
        ),

    ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
