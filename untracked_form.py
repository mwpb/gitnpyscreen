import npyscreen
import sqlite_utils
import git_utils
import curses

class untracked_multiselect(npyscreen.MultiSelect):
    def set_up_handlers(self):
        super(untracked_multiselect,self).set_up_handlers()
        self.handlers.update({curses.ascii.SP:self.toggle_then_down})
    def toggle_then_down(self,input):
        self.h_select_toggle(self)
        self.h_cursor_line_down(self)
    pass

class UntrackedForm(npyscreen.ActionForm):
    def create(self,*args,**keywords):
        self.repo_path = ''
        self.repo_name = ''
        self.name = 'Untracked Files'
        self.untracked_multiselect = self.add(untracked_multiselect,name='untracked',values=[])
    def on_cancel(self):
        self.parentApp.switchFormPrevious()
    def on_ok(self):
        git_utils.track_files(self.repo_path,self.untracked_multiselect.get_selected_objects())
        file_list = [self.repo_path+i for i in self.untracked_multiselect.get_selected_objects()]
        self.parentApp.getForm('COMMIT').repo_path = self.repo_path
        self.parentApp.getForm('COMMIT').repo_name = self.repo_name
        self.parentApp.getForm('COMMIT').file_list = file_list
        self.parentApp.getForm('COMMIT').commit_message.value = ''
        self.parentApp.getForm('COMMIT').branch_selectone.values = git_utils.get_branches(self.repo_path)
        self.parentApp.getForm('COMMIT').branch_selectone.value = git_utils.get_current_branch_number(self.repo_path)
        self.parentApp.setNextForm('COMMIT')
