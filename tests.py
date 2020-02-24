import  unittest
from unittest.mock import patch, Mock
import requests
import json

from app import app
from app.views import GitHubAPI, from_json
from app.models import GithubRepo


def test_github_life():
    response = requests.get('https://api.github.com/')
    assert_true(response.ok)


class TestIntegrations(unittest.TestCase):
    """
    Tests for api proxy.
    It's  naughty to hit github, i prefer mock
    """

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    # Github is still alive?
#     def test_home_status_code(self):
#         result = self.app.get('/')
#         self.assertEqual(result.status_code, 200)

    def test_githubrepo_object(self):
        """Object creation test"""
        o1 = GithubRepo(
             fullName="django/django",
             description="The Web framework for perfectionists with deadlines.",
             cloneUrl="https://github.com/django/django.git",
             stars=47374,
             createdAt="2012-04-28T02:47:18Z"
        )

        self.assertEqual(o1.fullName, 'django/django')
        self.assertEqual(o1.cloneUrl, 'https://github.com/django/django.git')
        self.assertEqual(o1.stars, 47374)
        self.assertEqual(o1.createdAt, "2012-04-28T02:47:18Z")

    def test_githubrepo_object_bad_date_format(self):
        """Test with bad date format"""
        with self.assertRaises(Exception) as context:
            GithubRepo(
                 fullName="django/django",
                 description="The Web framework for perfectionists with deadlines.",
                 cloneUrl="https://github.com/django/django.git",
                 stars=47374,
                 createdAt="21-11-1990"
            )
        self.assertTrue('Bad date format' in str(context.exception))

    def test_githubrepo_object_blank_name(self):
        """Test without name"""
        with self.assertRaises(Exception) as context:
            GithubRepo(
                 fullName="",
                 description="The Web framework for perfectionists with deadlines.",
                 cloneUrl="https://github.com/django/django.git",
                 stars=47374,
                 createdAt="2012-04-28T02:47:18Z"
            )
        self.assertTrue("full name can't be empty" in str(context.exception))

    def test_githubrepo_object_blank_stars(self):
        """Test without stars"""
        with self.assertRaises(Exception) as context:
            GithubRepo(
                 fullName="Test",
                 description="The Web framework for perfectionists with deadlines.",
                 cloneUrl="https://github.com/django/django.git",
                 stars='',
                 createdAt="2012-04-28T02:47:18Z"
            )
        self.assertTrue("stars must be integer" in str(context.exception))

    def test_githubrepo_object_str_stars(self):
        """Test with stars as string"""
        with self.assertRaises(Exception) as context:
            GithubRepo(
                 fullName="Test",
                 description="The Web framework for perfectionists with deadlines.",
                 cloneUrl="https://github.com/django/django.git",
                 stars='n',
                 createdAt="2012-04-28T02:47:18Z"
            )
        self.assertTrue("stars must be integer" in str(context.exception))

    @patch('app.views.GitHubAPI')
    def test_api_repos(self, MockApi):
        """Test mock api"""
        api = MockApi()

        api.get_repo.return_value = json.dumps({
             "full_name": "django/django",
             "description": "The Web framework for perfectionists with deadlines.",
             "clone_url": "https://github.com/django/django.git",
             "stargazers_count": 47374,
             "created_at": "2012-04-28T02:47:18Z"
        })

        response = api.get_repo()
        self.assertIsNotNone(response)

        repo = from_json(response, GithubRepo)
        assert type(repo) is GithubRepo
        self.assertIsNotNone(repo)


if __name__ == "__main__":
    unittest.main()
