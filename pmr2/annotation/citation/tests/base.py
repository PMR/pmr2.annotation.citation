from Testing import ZopeTestCase as ztc
from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase.layer import onsetup, onteardown
from Products.PloneTestCase import PloneTestCase as ptc

@onsetup
def setup():
    import pmr2.annotation.citation
    fiveconfigure.debug_mode = True
    zcml.load_config('configure.zcml', pmr2.annotation.citation)
    fiveconfigure.debug_mode = False
    ztc.installPackage('pmr2.annotation.citation')

@onteardown
def teardown():
    pass

setup()
teardown()
ptc.setupPloneSite(products=('pmr2.annotation.citation', 'pmr2.app'))
