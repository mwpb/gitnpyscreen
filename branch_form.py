import npyscreen
import git_utils

class local_selectone(npyscreen.SelectOne):
    pass

class remote_selectone(npyscreen.SelectOne):
    pass

class BranchForm(npyscreen.ActionForm):
    def create(self,*args,**keywords):
        self.repo_path = ''
        self.local_selectone = self.add(local_selectone,max_height=10)
        self.remote_selectone = self.add(remote_selectone,max_height=10)
    def beforeEditing(self):
        self.local_selectone.values = git_utils.list_local_branches(self.repo_path)
        self.remote_selectone.values = git_utils.list_remote_branches(self.repo_path)
    def on_cancel(self):
        self.parentApp.switchFormPrevious()
    def on_ok(self):
        git_utils.start_branch_track(self.repo_path,self.local_selectone.values[self.local_selectone.cursor_line][0],self.remote_selectone.values[self.remote_selectone.cursor_line])
        self.parentApp.switchFormPrevious()
