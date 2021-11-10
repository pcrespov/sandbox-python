from github import Github
import os




g = Github(os.environ["GITHUB_TOKEN"])

u = g.get_user()

u2 = g.get_user("pcrespov")
assert u