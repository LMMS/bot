import json

from flask import Flask
from flask import request

import settings
from common.GithubHelper import GithubHelper
from common.PullRequestLinkComment import PullRequestLinkComment
from resolvers.Appveyor import Appveyor
from resolvers.CircleCi import CircleCI

app = Flask(__name__)

resolvers = [
    Appveyor,
    CircleCI
]


@app.route('/', methods=['POST'])
def main():
    json_data = json.loads(request.data.decode('utf-8'))

    if json_data.get('state', '') != 'success':
        return "state is not success"

    github_helper = GithubHelper(settings=settings)
    pull_request = github_helper.find_pr_from_commit(json_data['repository']['full_name'],
                                                     json_data['commit']['sha'])

    if pull_request is None:
        return "Could not find a pull request for this sha"

    resolver = None
    # TODO: Maybe switch to context instead of target url.
    url = json_data['target_url']
    for resolver_cls in resolvers:
        if resolver_cls.is_resolver_url(url):
            resolver = resolver_cls(url=url)
            break

    if resolver is None:
        return "Can't find resolver for {}".format(url)

    artifacts_urls = resolver.artifacts_urls()
    if not artifacts_urls:
        return "Could not find any artifact"

    pr_comment = PullRequestLinkComment(settings)
    pr_comment.update_or_create_links_comment(pull_request, artifacts_urls)

    return 'Success'
