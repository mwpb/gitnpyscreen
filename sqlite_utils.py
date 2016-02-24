from sys import argv
from git_utils import *
import sqlite3

def add_repo(repo_name,repo_path):
    db = sqlite3.connect('test.db')
    c = db.cursor()
    c.execute("INSERT INTO repos(repo_name,repo_path) VALUES(?,?)",(repo_name,repo_path))
    db.commit()
    c.close()

#def __init__(filename):
#    db = sqlite3.connect('test.db')
#    c = db.cursor()
#    c.execute("CREATE TABLE IF NOT EXISTS repos (repo_name text,repo_path text)")
#    db.commit()
#    c.close()

def delete_repo(repo_name):
    db = sqlite3.connect('test.db')
    c = db.cursor()
    c.execute("DELETE FROM repos where repo_name=?",(repo_name,))
    db.commit()
    c.close()

def get_repo(repo_name):
    db = sqlite3.connect('test.db')
    c = db.cursor()
    c.execute("select %s from repos" % repo_name)
    repo_list = c.fetchall()
    new_list = []
    for row in repo_list:
        row = row+(str(repo_last_fetch_time(row[1])),)
        new_list.append(row)
    c.close()
    return new_list

def list_repos():
    db = sqlite3.connect('test.db')
    c = db.cursor()
    c.execute("select * from repos")
    repo_list = c.fetchall()
    new_list = []
    for row in repo_list:
        star = '*'
        file_statuses = str(len(untracked_files(row[1])))+'/'+str(len(get_modified_files(row[1])))+'/'+str(len(get_staged_files(row[1])))+'/'+str(len(get_commits(row[1])))
        row = row+(str(repo_last_fetch_time(row[1])),)+(str(get_active_branch(row[1])),)+(file_statuses,)+('('+str(len(get_commits_behind(row[1])))+')',)
        new_list.append(row)
    c.close()
    print new_list
    return new_list

if __name__ == '__main__':
    repo_name = raw_input('enter repo name: ')
    #repo_path = raw_input('enter repo path: ')
    #add_repo(repo_name,repo_path)
    #list_repos()
    delete_repo(repo_name)
