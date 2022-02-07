import pandas as pd
import numpy as np
import pymysql
from collections import defaultdict
from utils.sqlApi import mysqlConnect
import datetime


class sql_query(mysqlConnect):
    def get_user_id(self, email: str, password: str):
        """
        @param email: email
        @param password: password
        @return: 返回用户的user_id / None(出现多用户或查询不到)
        """
        sql = "SELECT user_id FROM user WHERE email = \'{}\' and password = \'{}\'".format(email, password)
        print(sql)
        success, results = self.select(sql)
        try:
            if success == True:
                assert (len(results) == 1)
            else:
                return None
        except:
            # print("one email has multiple users")
            return None
        # print("return user_id:")
        return results[0]['user_id']

    def get_projects_id_list(self, user_id: int):
        """
        获取用户的所有project_id
        @param user_id: user_id
        @return: project_id list / None(失败)
        """
        sql = "SELECT project_id FROM enroll_project WHERE user_id = {}".format(str(user_id))
        success, results = self.select(sql)
        if success == False:
            return None
        ret = []
        for dict in results:
            ret.append(dict['project_id'])
            # print("return project_id:")
        return ret

    def get_runs_id_list(self, project_id: int):
        """
        获取project的所有run_id
        @param project_id: project_id
        @return: run_id list / None(失败)
        """
        sql = "SELECT run_id FROM enroll_run WHERE project_id = {}".format(str(project_id))
        success, results = self.select(sql)
        if success == False:
            return None
        ret = []
        for dict in results:
            ret.append(dict['run_id'])
            # print("return run_id:")
        return ret

    def get_log(self, run_id: int):
        """
        获取某次run的所有log信息
        @param run_id: run_id
        @return: defaultdict(list) / None(没有相应run_id)
        """
        sql = "SELECT `key`, value FROM log_data WHERE run_id = {}".format(str(run_id))
        success, results = self.select(sql)
        if success == False:
            return None
        dict = defaultdict(list)
        for dic in results:
            dict[dic['key']].append(dic['value'])
        return dict

    def get_available(self, name):
        """
        @param name: 可选字段为user_id , project_id , run_id
        @return: 返回为分配的相应字段/None(fail)
        """
        name = "available_" + name
        sql = "SELECT {} FROM available".format(name)
        success1, result = self.select(sql)
        sql = "UPDATE available SET {} = {} + 1".format(name, name)
        success2, update_result = self.query(sql)
        if not (success1 & success2):
            print("get available error!")
            return None
        return result[0][name]

    def enroll_project(self, user_id: int, project_name: str):
        """
        根据user_id与project_name创建一个全新的project
        涉及到enroll_project与project两张表的改动
        @param user_id: user_id
        @param project_name: project_name
        @return: project_id / None(失败）
        """
        project_id = self.get_available("project_id")
        sql = 'INSERT INTO enroll_project(project_create_date,project_name,project_id,user_id) VALUES (\'{}\',\'{}\',{},{})'.format(
            datetime.datetime.now().date(), project_name, project_id, user_id)
        success1, results = self.query(sql)
        sql = 'INSERT INTO project(project_id,project_name,user_id,total_run) VALUES ({},\'{}\',{},{})'.format(
            project_id, project_name, user_id, 0)
        success2, results = self.query(sql)
        success = success1 & success2
        if not success:
            print("enroll project error!")
            return None
        return project_id

    def touch_project(self, user_id: int, project_name: str):
        """
        原理类似于touch，当不存在该项目时将新建该项目，返回值为该项目的id
        @param user_id:
        @param project_name:
        @return: project_id / None(fail)
        """
        sql = "SELECT project_id FROM enroll_project WHERE user_id = {} AND project_name = \'{}\'".format(str(user_id),
                                                                                                          str(project_name))
        success, results = self.select(sql)
        print(success, results)
        if not success:
            return None
        return results[0]["project_id"] if len(results) != 0 else self.enroll_project(user_id, project_name)

    def enroll_run(self, user_id: int, project_id: int, run_name: str, config: str = "NULL"):
        """
        注册一项新的run
        改动enroll_run与run两张表
        @param user_id:
        @param project_id:
        @param run_name:
        @param config:
        @return: run_id / None(fail)
        """
        run_id = self.get_available("run_id")
        sql = "INSERT INTO enroll_run(user_id,project_id,run_create_date,run_name,run_id) VALUES({},{},\'{}\',\'{}\',{})".format(
            user_id, project_id, datetime.datetime.now(), run_name, run_id)
        success1, results = self.query(sql)

        sql = "INSERT INTO run(run_id,project_id,config,state,start_time) VALUES({},{},{},\'{}\',\'{}\')".format(run_id,
                                                                                                                 project_id,
                                                                                                                 config,
                                                                                                                 "RUNNING",
                                                                                                                 datetime.datetime.now())
        success2, results = self.query(sql)
        success = success1 & success2
        if not success:
            print("enroll run error!")
            return None
        return run_id

    def get_step(self, run_id):
        sql = 'SELECT step FROM run WHERE run_id = {}'.format(str(run_id))
        success1, result = self.select(sql)
        sql = 'UPDATE run SET step = step + 1 where run_id = {}'.format(str(run_id))
        success2, result2 = self.query(sql)
        return result[0]['step']

    def log(self, run_id: int, dic: dict):
        step = self.get_step(run_id)
        data = datetime.datetime.now()
        for key, value in dic.items():
            sql = 'INSERT INTO log_data(run_id,`key`,log_date,`value`,step) VALUES({},\'{}\',\'{}\',{},{})'.format(
                run_id, key, data, value, step)
            print(sql)
            success, result = self.query(sql)
            if not success:
                print("log error!")



