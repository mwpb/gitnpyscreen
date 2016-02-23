import sqlite_utils
import npyscreen
import git_utils

class MyTestApp(npyscreen.NPSAppManaged):
    def onStart(self):
        npyscreen.setTheme(npyscreen.Themes.ElegantTheme)
        self.add_repo = sqlite_utils.add_repo
        self.list_repos = sqlite_utils.list_repos
        self.registerForm('MAIN',MainForm())
        self.registerForm('EDIT',EditForm())
        self.registerForm('STAGE',StageForm())
        self.registerForm('COMMIT',CommitForm())
        self.registerForm('MERGE',MergeForm())
        self.registerForm('REMOTES',RemoteForm())
        self.registerForm('CHECKOUT',CheckoutForm())

class repo_multiline(npyscreen.MultiLine):
    def display_value(self,vl):
        return "{:15} {:20} {:30} {:10} {:3} {:3}".format(vl[0],vl[2],vl[1],vl[3],vl[4],vl[5])

class stage_multiselect(npyscreen.MultiSelect):
    pass

class commit_multiselect(npyscreen.MultiSelect):
    pass

class branch_selectone(npyscreen.TitleSelectOne):
    pass

class merge_selectone(npyscreen.SelectOne):
    pass

class remote_selectone(npyscreen.SelectOne):
    pass 

class checkout_selectone(npyscreen.SelectOne):
    pass

class CheckoutForm(npyscreen.ActionForm):
    def create(self,*args,**keywords):
        self.repo_path = ''
        self.name = 'Checkout branch'
        self.new_branch = ''
        self.checkout_selectone = self.add(checkout_selectone,name='checkout',values=[])
    def on_cancel(self):
        self.parentApp.switchFormPrevious()
    def on_ok(self):
        git_utils.checkout(self.repo_path,self.checkout_selectone.get_selected_objects())
        self.parentApp.switchFormPrevious()

class RemoteForm(npyscreen.ActionForm):
    def create(self,*args,**keywords):
        self.repo_path = ''
        self.name = 'Choose remote:'
        self.remote_selectone = self.add(remote_selectone,name='remotes',values=[])
    def on_cancel(self):
        self.parentApp.switchFormPrevious()
    def on_ok(self):
        git_utils.push_remote(self.repo_path,self.remote_selectone.get_selected_objects())
        self.parentApp.switchFormPrevious()

class MergeForm(npyscreen.ActionForm):
    def create(self,*args,**keywords):
        self.repo_path = ''
        self.current_branch = git_utils.get_current_branch_name(self.repo_path)
        self.name = "Current branch is %s Choose branch to merge with:" % self.current_branch
        self.repo_name = ''
        self.branch_list = []
        self.merge_selectone = self.add(merge_selectone,name='merge',values=[])
    def on_cancel(self):
        self.parentApp.switchFormPrevious()
    def on_ok(self):
        git_utils.merge_current(self.repo_path,self.merge_selectone.values[self.merge_selectone.cursor_line])
        self.parentApp.switchFormPrevious()
 
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
        self.parentApp.switchForm('MAIN')
    
class EditForm(npyscreen.ActionForm):
    def create(self,*args,**keywords):
        self.name = "Add Repo"
        self.repo_name = self.add(npyscreen.TitleText,name='Repo Name')
        self.repo_path = self.add(npyscreen.TitleText,name='Repo Path')
    def beforeEditing(self):
        self.repo_name.value = ''
        self.repo_path.value = ''
    def set_up_handlers(self):
        super(EditForm,self).set_up_handlers()
        self.handlers.update({"q": self.do_something})
    def afterEditing(self):
        self.parentApp.add_repo(self.repo_name.value,self.repo_path.value)
        self.parentApp.setNextFormPrevious()
    def do_something(self,input):
        self.parentApp.switchForm(None)
    def on_cancel(self):
        self.parentApp.switchFormPrevious()

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
        self.add_widget(npyscreen.FixedText,editable=False,color='green',value="{:15} {:20} {:30} {:10} {:3} {:3}".format('Repo Name','Last Fetch','Repo Path','Tracking','Ahead','Behind'))
        self.repo_multiline = self.add(repo_multiline,name="{:15} {:20} {:30} {:20}".format('Repo name','Last Fetch','Repo Path','Tracking Branch'),values=sqlite_utils.list_repos(),value=0)
    def beforeEditing(self):
        self.repo_multiline.values = sqlite_utils.list_repos()
    def set_up_handlers(self):
        super(MainForm,self).set_up_handlers()
        self.handlers.update({'X':self.remove_repo,'c':self.checkout,'P':self.do_push,'r':self.on_refresh,"f":self.fetch,"m": self.merge,"q": self.exit,'a': self.edit_form,'s': self.stage})
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


if __name__ == '__main__':
    TA = MyTestApp()
    TA.run()
