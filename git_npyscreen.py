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

class repo_multiline(npyscreen.MultiLine):
    def display_value(self,vl):
        return "{:10} {:20} {:10}".format(vl[0],vl[2],vl[1])

class stage_multiselect(npyscreen.MultiSelect):
    pass

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

class StageForm(npyscreen.Form):
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
    def afterEditing(self):
        self.parentApp.setNextFormPrevious()

class MainForm(npyscreen.ActionFormMinimal):
    def create(self,*args,**keywords):
        self.name = "Repos"
        self.repo_multiline = self.add(repo_multiline,name='repos',values=sqlite_utils.list_repos(),value=0)
    def set_up_handlers(self):
        super(MainForm,self).set_up_handlers()
        self.handlers.update({"q": self.exit,'a': self.edit_form,'s': self.stage})
    #def afterEditing(self):
        #self.parentApp.setNextForm(None)
    def stage(self,input):
        self.parentApp.getForm('STAGE').name = "Staging area for %s" % str(self.repo_multiline.values[self.repo_multiline.cursor_line][0])
        self.parentApp.getForm('STAGE').stage_multiselect.values=sqlite_utils.get_modified_files(str(self.repo_multiline.values[self.repo_multiline.cursor_line][1]))
        self.parentApp.switchForm('STAGE')
    def on_ok(self):
        self.parentApp.switchForm(None)
    def exit(self,input):
        self.parentApp.switchForm(None)
    def edit_form(self,input):
        self.parentApp.switchForm('EDIT')

if __name__ == '__main__':
    TA = MyTestApp()
    TA.run()
