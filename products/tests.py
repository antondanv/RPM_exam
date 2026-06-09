from urllib import response

from django.test import TestCase, Client

# Create your tests here.
class HealpthCheckTest(TestCase):
    def test_ping_endpoint(self):
        client = Client()
        response = client.get('/ping/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'ok'})