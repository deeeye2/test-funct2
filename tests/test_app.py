import unittest
from app import app

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_calculate_success(self):
        response = self.app.post('/calculate', json={
            'numPods': 2,
            'numReplicas': 2,
            'cpuPerPod': 500,
            'memoryPerPod': 512,
            'haLevel': 'basic',
            'storageReq': 50,
            'networkTraffic': 1,
            'cloudProvider': 'any'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('provider', response.json)

    def test_calculate_failure(self):
        response = self.app.post('/calculate', json={
            'numPods': 0,  # Invalid input to simulate failure
            'numReplicas': 0,
            'cpuPerPod': 0,
            'memoryPerPod': 0,
            'haLevel': 'basic',
            'storageReq': 0,
            'networkTraffic': 0,
            'cloudProvider': 'any'
        })
        self.assertEqual(response.status_code, 500)
        self.assertIn('error', response.json)

if __name__ == '__main__':
    unittest.main()
