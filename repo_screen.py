import npyscreen
from main_form import *
from edit_form import *
from stage_form import *
from commit_form import *
from merge_form import *
from remote_form import *
from checkout_form import *
from untracked_form import *
import sqlite_utils
import git_utils

class MyTestApp(npyscreen.NPSAppManaged):
    def onStart(self):
        npyscreen.setTheme(npyscreen.Themes.ElegantTheme)
        #self.add_repo = sqlite_utils.add_repo
        #self.list_repos = sqlite_utils.list_repos
        self.registerForm('MAIN',MainForm())
        self.registerForm('EDIT',EditForm())
        self.registerForm('STAGE',StageForm())
        self.registerForm('COMMIT',CommitForm())
        self.registerForm('MERGE',MergeForm())
        self.registerForm('REMOTES',RemoteForm())
        self.registerForm('CHECKOUT',CheckoutForm())
        self.registerForm('UNTRACKED',UntrackedForm())

if __name__ == '__main__':
    TA = MyTestApp()
    TA.run()
