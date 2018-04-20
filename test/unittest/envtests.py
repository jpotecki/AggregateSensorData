import unittest, os, sys, json, logging
testdir = os.path.dirname(__file__)
configdir = '../../config'
config = os.path.join(testdir, configdir)
sys.path.insert(0, os.path.abspath(config))
import Gamma.env as gamma
import PROD.env as prod

class checkIam(unittest.TestCase):
    def test_checkGamma(self):
        # simply call the function, if it succeeds
        env = gamma.get_env()
        self.assertTrue(isinstance(env, dict))
        self.assertIn("bucket", env)
        self.assertIn("table", env)

    def test_checkProd(self):
        env = prod.get_env()
        self.assertTrue(isinstance(env, dict))
        self.assertIn("bucket", env)
        self.assertIn("table", env)

if __name__ == "__main__":
    unittest.main()
