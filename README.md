# Repo-screen

A curses front-end to git.
Designed to see status of multiple repositories at a glance.

Release 0.3.0. 
Now single database is stored at '~/.config/repo-screen/repoDatabase.db'.

Release 0.2.0.
Can now merge but no conflict resolution.

## Dependencies
See requirements.txt for precise version numbers.
Then 
    
    pip install -r requirements.txt 

should install the right dependencies.

###npyscreen
http://npyscreen.readthedocs.org/example-addressbk.html?highlight=recordlist

    pip install npyscreen

###gitpython
http://gitpython.readthedocs.org/en/stable/

    pip install gitpython

### python sh
https://amoffat.github.io/sh/

    pip install sh

##Also uses

###sqlite3 python module
https://docs.python.org/2/library/sqlite3.html

