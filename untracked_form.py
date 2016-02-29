import npyscreen
import sqlite_utils
import git_utils

class untracked_multiselect(npyscreen.MultiSelect):
    pass

class UntrackedForm(npyscreen.ActionForm):
    def create(self,*args,**keywords):
        self.repo_path = ''
        self.name = 'Untracked Files'
        self.untracked_multiselect = self.add(untracked_multiselect,name='untracked',values=[])
    def on_cancel(self):
        self.parentApp.switchFormPrevious()
    def on_ok(self):
        git_utils.track_files(self.repo_path,self.untracked_multiselect.get_selected_objects())
        self.parentApp.switchForm('MAIN')
