import npyscreen
import sqlite_utils
import git_utils

class repo_multiline(npyscreen.MultiLine):
    def display_value(self,vl):
        return "{:15} {:30} {:15} {:9}".format(vl[0],vl[1],vl[2],vl[3])

class bindings_pager(npyscreen.Pager):
    pass

class MainForm(npyscreen.ActionForm):
    def create(self,*args,**keywords):
        self.name = "Repos"
        self.bindings_string='''
        u - stage Untracked files
        t - stage Tracked files
        r - Rebase tmp branch over local branch
        a - push files that are Ahead of remote (displays origin master at moment)
        + - add repo
        - - remove repo under cursor
        q - quit
        '''
        self.bindings_list = self.bindings_string.split('\n')
        self.add_widget(npyscreen.FixedText,editable=False,color='green',value="{:15} {:30} {:15} {:7}".format('Repo Name','Repo Path','Checked Out','u/t/r/a'))
        self.repo_multiline = self.add(repo_multiline,name="repos",values=sqlite_utils.list_repos(),value=0,max_height=10)
        self.bindings_pager = self.add(bindings_pager,name='bindings',values=self.bindings_list)
    def beforeEditing(self):
        self.repo_multiline.values = sqlite_utils.list_repos()
    def set_up_handlers(self):
        super(MainForm,self).set_up_handlers()
        self.handlers.update({'b':self.branch,'u':self.untracked_files,'-':self.remove_repo,'c':self.checkout,'a':self.do_push,'r':self.on_refresh,"f":self.fetch,"r": self.rebase,"q": self.exit,'+': self.edit_form,'t':self.stage})
    #def afterEditing(self):
        #self.parentApp.setNextForm(None)
    def branch(self,input):
        self.parentApp.getForm('BRANCH').repo_path = self.repo_multiline.values[self.repo_multiline.cursor_line][1]
        self.parentApp.switchForm('BRANCH')
    def stage(self,input):
        self.parentApp.getForm('STAGE').name = "Staging area for %s" % str(self.repo_multiline.values[self.repo_multiline.cursor_line][0])
        self.parentApp.getForm('STAGE').repo_name = self.repo_multiline.values[self.repo_multiline.cursor_line][0]
        self.parentApp.getForm('STAGE').repo_path = self.repo_multiline.values[self.repo_multiline.cursor_line][1]
        self.parentApp.getForm('STAGE').stage_multiselect.value = []
        self.parentApp.getForm('STAGE').stage_multiselect.values=sqlite_utils.get_modified_files(str(self.repo_multiline.values[self.repo_multiline.cursor_line][1]))
        self.parentApp.switchForm('STAGE')
    def on_ok(self):
        self.parentApp.switchForm(None)
    def on_cancel(self):
        self.parentApp.switchForm(None)
    def exit(self,input):
        self.parentApp.switchForm(None)
    def edit_form(self,input):
        self.parentApp.switchForm('EDIT')
    def rebase(self,*args,**keywords):
        self.parentApp.getForm('MERGE').sync_stage = 'none'
        self.parentApp.getForm('MERGE').output_pager.values = ['none','waiting for output...']
        self.parentApp.getForm('MERGE').repo_name = self.repo_multiline.values[self.repo_multiline.cursor_line][0]
        self.parentApp.getForm('MERGE').repo_path = self.repo_multiline.values[self.repo_multiline.cursor_line][1]
        self.parentApp.switchForm('MERGE')
    def fetch(self,*args,**keywords):
        git_utils.git_fetch(self.repo_multiline.values[self.repo_multiline.cursor_line][1])
        self.repo_multiline.values = sqlite_utils.list_repos()
        self.repo_multiline.display()
        self.DISPLAY()
    def on_refresh(self,*args,**keywords):
        self.repo_multiline.display()
        self.DISPLAY()
    def do_push(self,*args,**keywords):
        self.parentApp.getForm('REMOTES').repo_path = self.repo_multiline.values[self.repo_multiline.cursor_line][1]
        self.parentApp.getForm('REMOTES').remote_selectone.values = git_utils.get_remote_branches(self.repo_multiline.values[self.repo_multiline.cursor_line][1])
        self.parentApp.switchForm('REMOTES')        
    def checkout(self,*args,**keywords):
        self.parentApp.getForm('CHECKOUT').repo_path = self.repo_multiline.values[self.repo_multiline.cursor_line][1]
        self.parentApp.getForm('CHECKOUT').checkout_selectone.values = git_utils.get_branches(self.repo_multiline.values[self.repo_multiline.cursor_line][1])
        self.parentApp.switchForm('CHECKOUT')        
    def remove_repo(self,*args,**keywords):
        sqlite_utils.delete_repo(self.repo_multiline.values[self.repo_multiline.cursor_line][0])
        self.beforeEditing()
        self.repo_multiline.display()
        self.DISPLAY()
    def untracked_files(self,*args,**keywords):
        self.parentApp.getForm('UNTRACKED').repo_name = self.repo_multiline.values[self.repo_multiline.cursor_line][0]
        self.parentApp.getForm('UNTRACKED').untracked_multiselect.values = git_utils.untracked_files(self.repo_multiline.values[self.repo_multiline.cursor_line][1])
        self.parentApp.getForm('UNTRACKED').repo_path = self.repo_multiline.values[self.repo_multiline.cursor_line][1]
        self.parentApp.switchForm('UNTRACKED')
