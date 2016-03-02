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
        self.get_branch_name = 'master'
        self.commit_message = self.add_widget(npyscreen.TitleText,use_two_lines=False,name='Commit message:')
        self.branch_list = []
        self.branch_selectone = self.add(branch_selectone,name='Currently tracking '+self.get_branch_name+'. Selecting another will reset HEAD~1 and roll back.',value=0,values=[])
    def on_cancel(self):
        self.parentApp.switchFormPrevious()
    def on_ok(self):
        commit_branch_name = ''
        for branch in self.branch_selectone.get_selected_objects():
            commit_branch_name = branch
        git_utils.commit_files(self.repo_path,self.file_list,self.commit_message.value,commit_branch_name)
        self.parentApp.switchForm('MAIN')
