from Products.PloneTestCase.layer import onsetup, onteardown
from pmr2.app.tests import base

@onsetup
def setup():
    import pmr2.annotation.citation
    fiveconfigure.debug_mode = True
    zcml.load_config('configure.zcml', pmr2.annotation.citation)
    fiveconfigure.debug_mode = False
    base.ztc.installPackage('pmr2.annotation.citation')

base.ptc.setupPloneSite(products=('pmr2.annotation.citation',))
