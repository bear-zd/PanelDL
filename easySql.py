import pandas as pd
import numpy as np
import pymysql
from collections import defaultdict
from PanelDL.utils.sqlApi import mysqlConnect
import datetime

class sql_query(mysqlConnect):
    def get_user_id(self, email:str, password:str):
        sql = "SELECT user_id FROM user WHERE email = \'{}\' and password = {}".format(email,password)
        success , results = self.select(sql)
        #print("results:",results)
        try:
            if success == True:
                assert(len(results) == 1)
            else:
                return None
        except:
            #print("one email has multiple users")
            return None
        #print("return user_id:")
        return results[0]['user_id']

    def get_projects_id_list(self, user_id:int):
        sql = "SELECT project_id FROM enroll_project WHERE user_id = {}".format(str(user_id))
        results = self.select(sql)
        if results[0 == True]:
            results = results[1]
        else:
            return None
        ret = []
        for dict in results :
           ret.append(dict['project_id']) 
        print("return project_id:")
        return ret
    
    def get_runs_id_list(self, project_id:int):
        sql = "SELECT run_id FROM enroll_run WHERE project_id = {}".format(str(project_id))
        results = self.select(sql)
        if results[0 == True]:
            results = results[1]
        else:
            return None
        ret = []
        for dict in results :
           ret.append(dict['run_id']) 
        print("return run_id:")
        return ret


    def get_log(self, run_id:int):
        sql = "SELECT `key`, value FROM log_data WHERE run_id = {}".format(str(run_id))
        results = self.select(sql)
        if results[0 == True]:
            results = results[1]
        else:
            return None
        dict = defaultdict(list)
        for dic in results:
            dict[dic['key']].append(dic['value'])
        return dict

    def get_available(self,name):
        """
        @param name: 可选字段为user_id , project_id , run_id
        @return: 返回为分配的相应字段/None(fail)
        """
        name = "available_"+name
        sql = "SELECT {} FROM available".format(name)
        success1,result = self.select(sql)
        sql = "UPDATE available SET {} = {} + 1".format(name,name)
        success2,update_result = self.query(sql)
        if not (success1 & success2):
            print("get available error!")
            return None
        return result[0][name]


    def enroll_project(self,user_id:int,project_name:str):
        """
        根据user_id与project_name创建一个全新的project
        涉及到enroll_project与project两张表的改动
        @param user_id: user_id
        @param project_name: project_name
        @return: project_id / None(失败）
        """
        project_id = self.get_available("project_id")
        sql = 'INSERT INTO enroll_project(project_create_date,project_name,project_id,user_id) VALUES (\'{}\',\'{}\',{},{})'.format(datetime.datetime.now().date(),project_name,project_id,user_id)
        success1 , results = self.query(sql)
        sql = 'INSERT INTO project(project_id,project_name,user_id,total_run) VALUES ({},\'{}\',{},{})'.format(project_id,project_name,user_id,0)
        success2 , results = self.query(sql)
        success = success1&success2
        if not success:
            print("enroll project error!")
            return None
        return project_id


    def touch_project(self,user_id:int,project_name:str):
        """
        原理类似于touch，当不存在该项目时将新建该项目，返回值为该项目的id
        @param user_id:
        @param project_name:
        @return: project_id / None(fail)
        """
        sql = "SELECT project_id FROM enroll_project WHERE user_id = {} AND project_name = \'{}\'".format(str(user_id),str(project_name))
        success , results = self.select(sql)
        print(success,results)
        if not success:
            return None
        return results[0]["project_id"] if len(results) != 0 else self.enroll_project(user_id,project_name)


if __name__ == '__main__':
    query = sql_query()
    print(query.touch_project(-1,"d"))