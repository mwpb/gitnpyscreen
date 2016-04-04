import subprocess
from git import Repo
from sys import argv
import os
import sh
import datetime

def track_files(repo_path,file_list):
    git = sh.git.bake(_cwd=repo_path)
    for file_for_tracking in file_list:
        git.add(file_for_tracking)

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

def get_branches(repo_path):
    repo = Repo(repo_path)
    branch_list = []
    for head in repo.heads:
        branch_list.append(head.name)
    #print branch_list
    return branch_list

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

# Rebase workflow completely contained below
def push_remote(repo_path,remote_name):
    (remote,branch) = remote_name.split('/')
    git = sh.git.bake(_cwd=repo_path)
    git.push(remote,branch)

def get_remote_branches(repo_path):
    repo = Repo(repo_path)
    remote_branches = []
    for branch in repo.git.branch('-r').split('\n'):
        remote_branches.append(branch.strip())
    #print remote_branches
    return remote_branches

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

def untracked_files(repo_path):
    git = sh.git.bake(_cwd=repo_path)
    untracked_list = git('ls-files','.','--exclude-standard','--others').split('\n')
    return filter(bool,untracked_list)

def create_branch(repo_path,new_branch):
    git = sh.git.bake(_cwd=repo_path)
    git.checkout('-b',new_branch)
    return new_branch

def delete_branch(repo_path,branch_name):
    git = sh.git.bake(_cwd=repo_path)

def tracked_branch(repo_path,branch_name):
    git = sh.git.bake(_cwd=repo_path)
    try:
        remote_tracked = git('rev-parse','--symbolic-full-name',branch_name+'@{u}')
        return remote_tracked
    except:
        return None

def active_branch(repo_path):
    git = sh.git.bake(_cwd=repo_path)
    active_branch = git('rev-parse','--abbrev-ref','HEAD')
    return str(active_branch).strip()

def list_local_branches(repo_path):
    git = sh.git.bake(_cwd=repo_path)
    branches = git('for-each-ref',"--format='%(refname:short),%(upstream:short)'","refs/heads").splitlines()
    branches = [branch.strip("'").split(',') for branch in branches]
    return branches

def list_tracking_branches(repo_path):
    git = sh.git.bake(_cwd=repo_path)
    branches = git('for-each-ref',"--format='%(refname:short),%(upstream:short)'","refs/heads").splitlines()
    branches = [branch.strip("'").split(',') for branch in branches]
    branches = [branch for branch in branches if branch[1]!='']
    return branches

def list_remote_branches(repo_path):
    git = sh.git.bake(_cwd=repo_path)
    branches = git('for-each-ref',"--format='%(refname:short)","refs/remotes").splitlines()
    branches = [branch.strip("'") for branch in branches]
    return branches

def start_branch_track(repo_path,local_branch,remote_branch):
    git = sh.git.bake(_cwd=repo_path)
    git('branch','-u',remote_branch,local_branch)
    return True

def rebase(repo_path,local,remote):
    git = sh.git.bake(_cwd=repo_path)
    git('fetch','origin')
    try:
        git('checkout',local)
        git('merge',remote)
    except:
        return 'master merge exception'
    git('checkout',local+'-tmp')
    #try:
    #    git('rebase',local)
    #except:
    #    return 'rebase'
    #try:
    #    git('checkout',local)
    #    git('merge',local+'-tmp')
    #except:
    #    return 'Temp Merge exception'
    #git('branch','-D',local+'-tmp')
    #return 'Pull, merge and rebase completed.'

def conflict_list(repo_path):
    git = sh.git.bake(_cwd=repo_path)
    conflict_list = git('diff','--name-only','--diff-filter=U')
    return conflict_list

def rebase_continue(repo_path):
    git = sh.git.bake(_cwd=repo_path)
    git('add','.')
    try:
        output = git('rebase','--continue')
    except:
        return 

def commit_count(repo_path,base_branch):
    git = sh.git.bake(_cwd=repo_path)
    count = git('rev-list','--count','^'+base_branch,'HEAD')
    return str(count)

def ahead_count(repo_path):
    git = sh.git.bake(_cwd=repo_path)
    try:
        count = git('rev-list','--count','@{u}..')
        return str(count)
    except:
        return '0'

def rebase_exceptions(repo_path):
    git = sh.git.bake(_cwd=repo_path)
    try:
        conflicts = git('rebase','--continue').splitlines()
        return conflicts
    except:
        return 'Add or stash changes.'

def sync(repo_path,sync_state,local,remote):
    git = sh.git.bake(_cwd=repo_path)
    if sync_state == 'none':
        git('fetch','origin')
        git('checkout',local)
        try:
            git('merge',remote)
            message = git('checkout',local+'-tmp')
            return 'merge complete', message
        except ErrorReturnCode:
            message = git('checkout',local+'-tmp')
            return 'merge error', message
    if sync_state == 'merge complete':
        rebase_message = ''
        try:
            message = subprocess.check_output(['git','rebase',local],cwd=repo_path)
            return 'rebase complete', message
        except subprocess.CalledProcessError as e:
            return 'rebase in progress', e.output
    if sync_state == 'rebase in progress':
        git('add','.')
        try:
            message = git('rebase','--continue')
            return 'rebase complete', message
        except:
            message = git('rebase','--continue')
            return 'rebase in progress', message
    if sync_state == 'rebase complete':
        git('checkout',local)
        git('merge',local+'-tmp')
        message = git('branch','-D',local+'-tmp')
        return 'ready to push', message
    if sync_state == 'ready to push':
        return 'ready to push', 'ready to push'
    else:
        return 'unknown', 'none'

if __name__ == '__main__':
    #repo_path = raw_input('Please enter repo path:')
    print rebase_exceptions('/Users/mat/repo-screen/')
