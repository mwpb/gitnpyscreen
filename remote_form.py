import npyscreen
import sqlite_utils
import git_utils

class remote_selectone(npyscreen.SelectOne):
    pass 

class RemoteForm(npyscreen.ActionForm):
    def create(self,*args,**keywords):
        self.repo_path = ''
        self.name = 'Choose remote:'
        self.remote_selectone = self.add(remote_selectone,name='remotes',values=[])
    def on_cancel(self):
        self.parentApp.switchFormPrevious()
    def on_ok(self):
        git_utils.push_remote(self.repo_path,self.remote_selectone.get_selected_objects()[0])
        self.parentApp.switchFormPrevious()
