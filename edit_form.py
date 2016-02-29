import npyscreen
import sqlite_utils
import git_utils
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
