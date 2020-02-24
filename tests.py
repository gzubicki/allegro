import  unittest
from unittest.mock import patch, Mock
import requests

from app import app
# from app import views
from app.views import GitHubAPI


def test_github_life():
    response = requests.get('https://api.github.com/')
    assert_true(response.ok)


# Github api mock
class TestIntegrations(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_home_status_code(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/')

        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    @patch('app.views.GitHubAPI')
    def test_api_repos(self, MockApi):
        api = MockApi()

        api.get_repo.return_value = [
         {
             "fullName": "django/django",
             "description": "The Web framework for perfectionists with deadlines.",
             "cloneUrl": "https://github.com/django/django.git",
             "stars": 47374,
             "createdAt": "2012-04-28T02:47:18Z"
        }
        ]

        response = api.get_repo()
        self.assertIsNotNone(response)
        self.assertIsInstance(response[0], dict)
        print(response)
#         assert MockApi is GitHubAPI


if __name__ == "__main__":
    unittest.main()
