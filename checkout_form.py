import npyscreen
import sqlite_utils
import git_utils
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


