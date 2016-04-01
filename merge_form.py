import npyscreen
import sqlite_utils
import git_utils
import time

class merge_selectone(npyscreen.SelectOne):
    pass

class merge_fixedText(npyscreen.FixedText):
    pass

class MergeForm(npyscreen.ActionForm):
    def create(self,*args,**keywords):
        self.repo_path = ''
        self.repo_name = ''
        self.branch_list = []
        self.merge_fixedText = self.add(merge_fixedText,value='Select branch to rebase over:')
        self.merge_selectone = self.add(merge_selectone,name='merge',values=[])
    def beforeEditing(self):
        self.merge_selectone.values = git_utils.list_tracking_branches(self.repo_path)
    def on_cancel(self):
        self.parentApp.switchFormPrevious()
    def on_ok(self):
        try:
            git_utils.fetch(repo_path)
            message = git_utils.rebase(self.repo_path,'master')
        except:
            message = git_utils.rebase_continue(self.repo_path,[])
            npyscreen.notify('rebase problem',title='Conflicts')
            time.sleep(2)
        self.parentApp.switchFormPrevious()
