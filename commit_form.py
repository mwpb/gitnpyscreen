import npyscreen
import sqlite_utils
import git_utils

class commit_multiselect(npyscreen.MultiSelect):
    pass

class branch_selectone(npyscreen.TitleSelectOne):
    pass

class CommitForm(npyscreen.ActionForm):
    def create(self,*args,**keywords):
        self.name = "Commit message and branch confirmation"
        self.repo_name = ''
        self.repo_path = ''
        self.file_list = ''
        self.active_branch = ''
        self.commit_message = self.add_widget(npyscreen.TitleText,use_two_lines=False,name='Commit message:')
        self.branch_list = []
        self.branch_selectone = self.add(branch_selectone,name='Currently tracking '+self.active_branch+'. Selecting another will reset HEAD~1 and roll back.',value=0,values=[])
    def beforeEditing(self):
        self.active_branch = git_utils.active_branch(self.repo_name)
    def on_cancel(self):
        self.parentApp.switchFormPrevious()
    def on_ok(self):
        if git_utils.tracked_branch(self.active_branch,self.active_branch) != None:
            git_utils.create_branch(self.repo_path,self.active_branch+'-temp')
        git_utils.commit_files(self.repo_path,self.file_list,self.commit_message.value)
        self.parentApp.switchForm('MAIN')
