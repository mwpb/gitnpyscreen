from git import Repo
from sys import argv
import os
import datetime

def get_current_branch_number(repo_path):
    repo = Repo(repo_path)
    value = 0
    branch_list = []
    for param, head in enumerate(repo.heads):
        if head.name == repo.active_branch.name:
            value = param
    print value
    return value

def get_branches(repo_path):
    repo = Repo(repo_path)
    branch_list = []
    for head in repo.heads:
        branch_list.append(head.name)
    print branch_list
    return branch_list

def commit_files(repo_path,file_list,commit_message,commit_branch_name):
    repo = Repo(repo_path)
    repo.index.add(file_list)
    if commit_branch_name == repo.active_branch.name:
        repo.index.commit(commit_message)
    else:
        repo.index.commit(commit_message+'INTENDED BRANCH='+commit_branch_name)
        repo.head.reset('HEAD~1',working_tree=True,index=True)

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
    get_branches(repo_path)
