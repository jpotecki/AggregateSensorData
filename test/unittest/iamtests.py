import unittest, os, sys, json, logging
from troposphere.iam import Role
testdir = os.path.dirname(__file__)
configdir = '../../config'
config = os.path.join(testdir, configdir)
sys.path.insert(0, os.path.abspath(config))
import Gamma.iam as gamma
import PROD.iam as prod

class checkIam(unittest.TestCase):
    def test_checkGamma(self):
        # simply call the function, if it succeeds
        iam = gamma.get_iam("GammaTest")
        self.assertTrue(isinstance(iam, Role))
        
    def test_checkProd(self):
        iam = prod.get_iam("PRODTest")
        self.assertTrue(isinstance(iam, Role))

if __name__ == "__main__":
    unittest.main()
