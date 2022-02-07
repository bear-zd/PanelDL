from easySql import *
import datetime

class PanelDL():
    def __init__(self):
        self.config = None
        self.project_id = None
        self.user_id = None
        self.run_id = None
        self.sql = sql_query()
        self.ok = False

    def login(self,email,password):
        """
        @param email: 用户的邮箱
        @param password: 用户的密码
        """
        user_id = self.sql.get_user_id(email,password)
        if user_id == None:
            print("login error!")
        else:
            print("login success!")
            self.user_id = user_id


    def init(self, project:str = "uncategorized",config:str = "NULL", run_name:str = None):
        """
        @param project: 工程名称
        @param config: 单次训练config
        @param run_name: run名称
        """
        self.project_id = self.sql.touch_project(self.user_id,project)
        self.run_id = self.sql.enroll_run(self.user_id,self.project_id,run_name,config)
        if self.project_id != None and self.run_id != None:
            self.ok = True
        print("self.ok:",self.ok)


    def log(self,log_dic:dict):
        self.sql.log(self.run_id,log_dic)


if __name__ == '__main__':
    PD = PanelDL()
    PD.login("root","root")
    PD.init(run_name="TEST3")
    PD.log({"train_acc":0.94,"val_acc":0.23})
    PD.log({"train_acc": 0.94, "val_acc": 0.23})