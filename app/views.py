from flask import Flask, abort
from app import app
from app.models import GithubRepo
import requests
import json
import logging

log = logging.getLogger(__name__)
app.config.from_object('settings.default_settings')


# It's to small for relocation
class GitHubAPI(object):
    """It's very light GitHub api client"""
    token = app.config['TOKEN']
    username = app.config['USERNAME']
    repos_url = app.config['REPOS_URL']

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'Authorization': 'Token {}'.format(self.token)})
        self.session.headers.update({'Accept': 'application/vnd.github.v3.text-match+json'})

    def get_repo(self, owner, repo):
        url = self.repos_url.format(owner, repo)
        log.debug("Making request to github: {}".format(url))

        try:
            r = self.session.get(url,)
        except requests.exceptions.RequestException as e:
            log.debug("Request error: {}".format(e))
            return None

        if r.status_code == 401:
            return abort(403, description="Bad credentials")
        if r.status_code == 404:
            return abort(404, description="site not found, please read documentation")
        if r.status_code != 200:
            log.error("Github - Bad server response {} - {}".format(r.status_code, r.text))
            return None
        return r.text


api = GitHubAPI()


@app.route("/repositories/<string:owner>/<string:repo>", methods=['GET'])
def repo_information_view(owner, repo):

    # FIXME: github takes only slugfy owner, repo?
    raw = api.get_repo(owner, repo)
    if raw is not None:
        # TODO: add threading
        try:
            repo = from_json(raw, GithubRepo)
            return json.dumps(repo.__dict__)
        except Exception as e:
            log.error("Failed to map {0}: {1}\n".format(str(raw), str(e)))

    return abort(500, description="Something goes wrong, check applog")


@app.errorhandler(404)
def not_found(error):
    return 'site not found, please read documentation'


@app.errorhandler(500)
def internal_error(error):
    return '500 something goes wrong, check applog"'


def from_json(msg, cls, **kwargs):
    return cls.fromJson(json.loads(msg, **kwargs))
