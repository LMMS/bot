import json

from flask import Flask
from flask import request

from common.GithubHelper import GithubHelper
from common.PullRequestLinkComment import PullRequestLinkComment
from resolvers.Appveyor import Appveyor
from resolvers.CircleCi import CircleCI
from settings import settings

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

    pull_request = GithubHelper(settings=settings.github).find_pr_from_commit(json_data['repository']['full_name'],
                                                                              json_data['commit']['sha'])

    if pull_request is None:
        return "Could not find a pull request for this sha"

    resolver = None
    url = json_data['target_url']
    for resolver_cls in resolvers:
        if resolver_cls.is_resolver_url(url):
            resolver = resolver_cls(url=url)
            break

    if resolver is None:
        return "Can't find resolver for {}".format(url)

    build_result = resolver.create_build_result(settings.platforms)
    if not build_result:
        return "Could not find any artifact"

    pr_comment = PullRequestLinkComment(settings)
    pr_comment.update_or_create_links_comment(pull_request, build_result)

    return 'Success'
