import unittest
from app import create_app

class TestAppConfigs(unittest.TestCase):
    """
    This class tests app configuration settings
    """

    def test_DefaultConfig(self):
        """Tests the default configuration settings """
        app = create_app("production")
        self.tester = app.test_client(self)
        self.assertEqual(True, app.config['JSONIFY_PRETTYPRINT_REGULAR'])
        self.assertTrue('http://127.0.0.1:5000/', app.config["SERVER_NAME"])

    def test_productionConfig(self):
        """Tests the production configuration settings """
        app = create_app("production")
        self.tester = app.test_client(self)
        self.assertEqual(False, app.config['DEBUG'])

    def test_TestingConfig(self):
        """Tests the Testing configuration settings """
        app = create_app("testing")
        self.tester = app.test_client(self)
        self.assertEqual(True, app.config['DEBUG'])

    def test_DevelopmentConfig(self):
        app = create_app("development")
        self.tester = app.test_client(self)
        self.assertEqual(True, app.config['DEBUG'])
