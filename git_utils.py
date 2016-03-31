from git import Repo
from sys import argv
import os
import sh
import datetime

def untracked_files(repo_path):
    git = sh.git.bake(_cwd=repo_path)
    untracked_list = git('ls-files','.','--exclude-standard','--others').split('\n')
    #print filter(bool,untracked_list)
    return filter(bool,untracked_list)

def track_files(repo_path,file_list):
    git = sh.git.bake(_cwd=repo_path)
    for file_for_tracking in file_list:
        git.add(file_for_tracking)

def push_remote(repo_path,remote_name):
    (remote,branch) = remote_name.split('/')
    git = sh.git.bake(_cwd=repo_path)
    git.push(remote,branch)

def checkout(repo_path,new_branch):
    git = sh.git.bake(_cwd=repo_path)
    git.checkout(new_branch)

def git_fetch(repo_path):
    git = sh.git.bake(_cwd=repo_path)
    git.fetch('-p')

def get_active_branch(repo_path):
    git = sh.git.bake(_cwd=repo_path)
    active_branch = git('rev-parse','--abbrev-ref','HEAD')
    #print repo.active_branch.name
    return active_branch

def merge_current(repo_path,branch_name):
    git = sh.git.bake(_cwd=repo_path)
    git.merge(branch_name)

def get_current_branch_number(repo_path):
    repo = Repo(repo_path)
    value = 0
    branch_list = []
    for param, head in enumerate(repo.heads):
        if head.name == repo.active_branch.name:
            value = param
    #print value
    return value

def get_remote_branches(repo_path):
    repo = Repo(repo_path)
    remote_branches = []
    for branch in repo.git.branch('-r').split('\n'):
        remote_branches.append(branch.strip())
    #print remote_branches
    return remote_branches

def get_branches(repo_path):
    repo = Repo(repo_path)
    branch_list = []
    for head in repo.heads:
        branch_list.append(head.name)
    #print branch_list
    return branch_list

def commit_files(repo_path,file_list,commit_message):
    git = sh.git.bake(_cwd=repo_path)
    for commit_file in file_list:
        git.add('-u',commit_file)
    git.commit('-m',commit_message)

def get_modified_files(repo_path):
    print repo_path
    repo = Repo(repo_path)
    modified_files = []
    for file in repo.index.diff(None):
        lines = str(file).split('\n')
        modified_files.append(lines[0])
    #print modified_files
    return modified_files

def get_staged_files(repo_path):
    git = sh.git.bake(_cwd=repo_path)
    repo = Repo(repo_path)
    staged_files = []
    for file in repo.index.diff('Head'):
        lines = str(file).split('\n')
        staged_files.append(lines[0])
    #print staged_files
    return staged_files

def get_commits(repo_path):
    repo = Repo(repo_path)
    commits_ahead = []
    for commit in repo.iter_commits('origin/master..master'):
        commits_ahead.append(commit.message)
    #print commits_ahead
    return commits_ahead

def get_commits_behind(repo_path):
    repo = Repo(repo_path)
    commits_behind = []
    for commit in repo.iter_commits('master..origin/master'):
        commits_behind.append(commit.message)
    #print commits_behind
    return commits_behind

def repo_last_fetch_time(repo_path):
    try:
        t = os.path.getmtime(repo_path+'.git/FETCH_HEAD')
        #print datetime.datetime.fromtimestamp(t)
        return datetime.datetime.fromtimestamp(t)
    except:
        #print 'No FETCH_HEAD'
        return 'No FETCH_HEAD'

def create_temp_branch(repo_path):
    git = sh.git.bake(_cwd=repo_path)
    git.checkout('-b','temp')
    return 'temp'

def delete_branch(repo_path,branch_name):
    git = sh.git.bake(_cwd=repo_path)

def tracked_branch(repo_path,branch_name):
    git = sh.git.bake(_cwd=repo_path)
    try:
        remote_tracked = git('rev-parse','--symbolic-full-name',branch_name+'@{u}')
    except:
        return None
    return remote_tracked

def active_branch(repo_path):
    git = sh.git.bake(_cwd=repo_path)
    active_branch = git('rev-parse','--abbrev-ref','HEAD')
    return active_branch

if __name__ == '__main__':
    repo_path = raw_input('Please enter repo path:')
    active_branch = active_branch(repo_path)
    tracked_branch = tracked_branch(repo_path,'temp')
    print tracked_branch
    #print 'modified files'
    #get_modified_files(repo_path)
    #print 'staged files'
    #get_staged_files(repo_path)
    #print 'commits ahead'
    #get_commits(repo_path)
    #print 'commits behind'
    #get_commits_behind(repo_path)
    #print 'last fetch time'
    #repo_last_fetch_time(repo_path)
    #print 'list of local branches'
    #get_branches(repo_path)
    #print 'list of remote branches'
    #get_remote_branches(repo_path)
