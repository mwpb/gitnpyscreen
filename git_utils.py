from git import Repo
from sys import argv
import os
import datetime

def commit_files(repo_path,file_list,commit_message):
    repo = Repo(repo_path)
    repo.index.add(file_list)
    repo.index.commit(commit_message)

def get_modified_files(repo_path):
    repo = Repo(repo_path)
    modified_files = []
    for file in repo.index.diff(None):
        lines = str(file).split('\n')
        modified_files.append(lines[0])
    print modified_files
    return modified_files

def get_staged_files(repo_path):
    repo = Repo(repo_path)
    staged_files = []
    for file in repo.index.diff('Head'):
        lines = str(file).split('\n')
        staged_files.append(lines[0])
    print staged_files
    return staged_files

def get_commits(repo_path):
    repo = Repo(repo_path)
    commits_ahead = []
    for commit in repo.iter_commits('origin/master..master'):
        commits_ahead.append(commit.message)
    print commits_ahead
    return commits_ahead

def repo_last_fetch_time(repo_path):
    t = os.path.getmtime(repo_path+'.git/FETCH_HEAD')
    print datetime.datetime.fromtimestamp(t)
    return datetime.datetime.fromtimestamp(t)

if __name__ == '__main__':
    script, repo_path = argv
    get_modified_files(repo_path)
    get_staged_files(repo_path)
    get_commits(repo_path)
    repo_last_fetch_time(repo_path)
