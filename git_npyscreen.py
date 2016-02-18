import sqlite_utils
import npyscreen
import git_utils

class MyTestApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.add_repo = sqlite_utils.add_repo
        self.list_repos = sqlite_utils.list_repos
        self.registerForm('MAIN',MainForm())
        self.registerForm('EDIT',EditForm())
        self.registerForm('STAGE',StageForm())
        self.registerForm('COMMIT',CommitForm())
        self.registerForm('MERGE',MergeForm())

class repo_multiline(npyscreen.MultiLine):
    def display_value(self,vl):
        return "{:10} {:20} {:10}".format(vl[0],vl[2],vl[1])

class stage_multiselect(npyscreen.MultiSelect):
    pass

class commit_multiselect(npyscreen.MultiSelect):
    pass

class branch_selectone(npyscreen.SelectOne):
    pass

class merge_selectone(npyscreen.SelectOne):
    pass

class MergeForm(npyscreen.ActionForm):
    def create(self,*args,**keywords):
        self.repo_path = ''
        self.current_branch = git_utils.get_current_branch_name(self.repo_path)
        self.name = "Current branch is %s Choose branch to merge with:" % self.current_branch
        self.repo_name = ''
        self.branch_list = []
        self.merge_selectone = self.add(merge_selectone,name='merge',values=[])
    #def set_up_handlers(self):
        #super(EditForm,self).set_up_handlers()
        #self.handlers.update({})
    def on_cancel(self):
        self.parentApp.switchFormPrevious()
    def on_ok(self):
        git_utils.merge_current(self.repo_path,self.merge_selectone.values[self.merge_selectone.cursor_line])
        #self.parentApp.getForm('STAGE').name = self.commit_message.value
        #git_utils.commit_files(self.repo_path,self.file_list,self.commit_message.value)
        #git_utils.commit_files(self.repo_path,self.file_list,self.commit_selectone.values[self.commit_selectone.cursor_line][0])
        self.parentApp.switchFormPrevious()
 
#class CommitListForm(npyscreen.ActionForm):
#    def create(self,*args,**keywords):
#        self.name = 'List of commits not yet merged:'
#        self.repo_name = ''
#        self.repo_path = ''
#        self.commit_multiselect = self.add(commit_multiselect,name='commit',value=0)
#    def on_cancel(self):
#        self.parentApp.setNextFormPrevious()
#    def on_ok(self):
#        commit_list = []
#        for commit in self.commit_multiselect.get_selected_objects():
#            commit_list.append(commit)
#        self.parentApp.getForm('MERGE').merge_selectone.values=git_utils.get_branches(self.repo_path)
#        self.parentApp.getForm('MERGE').repo_path = self.repo_path
#        self.parentApp.getForm('MERGE').repo_name = self.repo_name
#        self.parentApp.getForm('MERGE').file_list = commit_list
#        self.parentApp.setNextForm('MERGE')

class CommitForm(npyscreen.ActionForm):
    def create(self,*args,**keywords):
        self.name = "Choose old commit or press n to create new:"
        self.repo_name = ''
        self.repo_path = ''
        self.file_list = ''
        self.get_branch_name = 'master'
        self.commit_message = self.add(npyscreen.TitleText,name='Commit message: ')
        self.branch_list = []
        self.add(npyscreen.TitleText,value="The current branch is selected. If this commit is intended for another branch specify it here. In that case I'll do the commit but then perform a git reset HEAD~1 and roll back the working tree and index. Then you can pick up the pieces from git reflog.")
        self.branch_selectone = self.add(branch_selectone,name='merge',value=0,values=[])
    #def set_up_handlers(self):
        #super(EditForm,self).set_up_handlers()
        #self.handlers.update({"m": self.merge})
    def on_cancel(self):
        self.parentApp.switchFormPrevious()
    def on_ok(self):
        #self.parentApp.getForm('STAGE').name = self.commit_message.value
        commit_branch_name = ''
        for branch in self.branch_selectone.get_selected_objects():
            commit_branch_name = branch
        git_utils.commit_files(self.repo_path,self.file_list,self.commit_message.value,commit_branch_name)
        #git_utils.commit_files(self.repo_path,self.file_list,self.commit_selectone.values[self.commit_selectone.cursor_line][0])
        self.parentApp.switchFormPrevious()
    
class EditForm(npyscreen.Form):
    def create(self,*args,**keywords):
        self.name = "Add Repo"
        self.repo_name = self.add(npyscreen.TitleText,name='Repo Name')
        self.repo_path = self.add(npyscreen.TitleText,name='Repo Path')
    def set_up_handlers(self):
        super(EditForm,self).set_up_handlers()
        self.handlers.update({"q": self.do_something})
    def afterEditing(self):
        self.parentApp.add_repo(self.repo_name.value,self.repo_path.value)
        self.parentApp.setNextFormPrevious()
    def do_something(self,input):
        self.parentApp.switchForm(None)

class StageForm(npyscreen.ActionForm):
    def create(self,*args,**keywords):
        self.name = "Staging Area"
        self.repo_name = ''
        self.repo_path = ''
        self.stage_multiselect = self.add(stage_multiselect,name='stage',value=0)
    def set_up_handlers(self):
        super(StageForm,self).set_up_handlers()
        self.handlers.update({"q": self.previous_form})
    def previous_form(self,input):
        self.parentApp.switchFormPrevious()
    def on_cancel(self):
        self.parentApp.setNextFormPrevious()
    def on_ok(self):
        file_list = []
        for modified_file in self.stage_multiselect.get_selected_objects():
            full_path = self.repo_path+modified_file
            file_list.append(full_path)
        #self.parentApp.getForm('COMMIT').commit_selectone.values=sqlite_utils.get_commits(self.repo_path)
        self.parentApp.getForm('COMMIT').repo_path = self.repo_path
        self.parentApp.getForm('COMMIT').repo_name = self.repo_name
        self.parentApp.getForm('COMMIT').file_list = file_list
        self.parentApp.getForm('COMMIT').branch_selectone.values = git_utils.get_branches(self.repo_path)
        self.parentApp.getForm('COMMIT').branch_selectone.value = git_utils.get_current_branch_number(self.repo_path)
        self.parentApp.setNextForm('COMMIT')

class MainForm(npyscreen.ActionForm):
    def create(self,*args,**keywords):
        self.name = "Repos"
        self.repo_multiline = self.add(repo_multiline,name='repos',values=sqlite_utils.list_repos(),value=0)
    def set_up_handlers(self):
        super(MainForm,self).set_up_handlers()
        self.handlers.update({'r':self.on_refresh,"f":self.fetch,"m": self.merge,"q": self.exit,'a': self.edit_form,'s': self.stage})
    #def afterEditing(self):
        #self.parentApp.setNextForm(None)
    def stage(self,input):
        self.parentApp.getForm('STAGE').name = "Staging area for %s" % str(self.repo_multiline.values[self.repo_multiline.cursor_line][0])
        self.parentApp.getForm('STAGE').repo_name = self.repo_multiline.values[self.repo_multiline.cursor_line][0]
        self.parentApp.getForm('STAGE').repo_path = self.repo_multiline.values[self.repo_multiline.cursor_line][1]
        self.parentApp.getForm('STAGE').stage_multiselect.values=sqlite_utils.get_modified_files(str(self.repo_multiline.values[self.repo_multiline.cursor_line][1]))
        self.parentApp.switchForm('STAGE')
    def on_ok(self):
        self.parentApp.switchForm(None)
    def exit(self,input):
        self.parentApp.switchForm(None)
    def edit_form(self,input):
        self.parentApp.switchForm('EDIT')
    def merge(self,*args,**keywords):
        self.parentApp.getForm('MERGE').merge_selectone.values = git_utils.get_branches(self.repo_multiline.values[self.repo_multiline.cursor_line][1])+git_utils.get_remote_branches(self.repo_multiline.values[self.repo_multiline.cursor_line][1])
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

if __name__ == '__main__':
    TA = MyTestApp()
    TA.run()
