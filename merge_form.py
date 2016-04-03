import npyscreen
import sqlite_utils
import git_utils
import subprocess

class output_pager(npyscreen.Pager):
    pass

class merge_selectone(npyscreen.SelectOne):
    pass

class merge_fixedText(npyscreen.FixedText):
    pass

class MergeForm(npyscreen.ActionForm):
    def create(self,*args,**keywords):
        self.repo_path = ''
        self.repo_name = ''
        self.sync_state = 'none'
        self.branch_list = []
        self.merge_fixedText = self.add(merge_fixedText,editable=False,value='Select branch to rebase over :')
        self.merge_selectone = self.add(merge_selectone,name='merge',values=[],max_height=10)
        self.output_pager = self.add(output_pager,name='Output:',values=[self.sync_state,'waiting for output...'])
    def beforeEditing(self):
        self.merge_selectone.values = git_utils.list_tracking_branches(self.repo_path)
    def on_cancel(self):
        self.parentApp.switchFormPrevious()
    def on_ok(self):
        local = str(self.merge_selectone.get_selected_objects()[0][0])
        remote = str(self.merge_selectone.get_selected_objects()[0][1])
        output, message = git_utils.sync(self.repo_path,self.sync_state,local,remote)
        self.parentApp.getForm('MERGE').sync_state = output
        self.parentApp.getForm('MERGE').output_pager.values = [self.sync_state]+message.splitlines()
        if self.sync_state == 'ready to push':
            self.parentApp.switchForm('MAIN')
        else:
            self.parentApp.switchForm('MERGE')
