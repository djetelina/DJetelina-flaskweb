import requests
import requests_cache
from datetime import datetime


def fetch_commits(repo_name):
    """
    Cached commits from GitHub API

    :return:    JSON with commits api
    """
    requests_cache.install_cache('commits_cache', expires_after=60 * 15)
    r = requests.get('https://api.github.com/repos/iScrE4m/{}/commits'.format(repo_name)).json()
    return r


class Commits:
    """
    Object holding information about a commit, called with name of a repository

    Get commit information by calling Commits.list[x].var
    x = 0 will get the newest and 14 the oldest
    """

    def __init__(self, repo_name):
        self.commits = fetch_commits(repo_name)
        self.list = [self.parse_commit(x) for x in range(0, 15)]

    def parse_commit(self, number):
        try:
            date = self.commits[number]['commit']['author']['date']
            message = self.commits[number]['commit']['message']
        except IndexError:
            return Commit("2037-07-31T00:00:00Z", "Error parsing commit")
        return Commit(date, message)


class Commit:
    """
    Information about a commit

    self.date       string with date like 2016-07-12T19:26:15Z
    self.datetime   datetime object
    self.message    commit message
    """

    def __init__(self, date, message):
        self.date = date
        self.datetime = datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
        self.message = message
