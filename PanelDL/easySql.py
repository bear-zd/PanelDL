import pandas as pd
import numpy as np
import pymysql
from collections import defaultdict
from utils.sqlApi import mysqlConnect
import datetime
import json


class sql_query(mysqlConnect):
    def get_user_id(self, email: str, password: str):
        """
        @param email: email
        @param password: password
        @return: 返回用户的user_id / None(出现多用户或查询不到)
        """
        sql = "SELECT user_id FROM user WHERE email = \'{}\' and password = \'{}\'".format(email, password)
        # print(sql)
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

    def get_user_first_name(self, user_id: int):
        """
        @param user_id: user_id
        @return: 返回用户的first_name
        """
        sql = "SELECT first_name FROM user WHERE user_id = \'{}\'".format(user_id)
        success, results = self.select(sql)
        try:
            if success == True:
                assert (len(results) == 1)
            else:
                return None
        except:
            return None
        return results[0]['first_name']

    def get_projects_id_list(self, user_id: int):
        """
        获取用户的所有project_id
        @param user_id: user_id
        @return: project_id list / None(失败)
        """
        sql = "SELECT project_id FROM enroll_project WHERE user_id = {}".format(user_id)
        success, results = self.select(sql)
        if success == False:
            return None
        ret = []
        for dict in results:
            ret.append(dict['project_id'])
        return ret

    def get_projects_name_list(self, user_id: int):
        """
        获取用户的所有project_name
        @param user_id: user_id
        @return: project_name list / None(失败)
        """
        sql = "SELECT project_name FROM enroll_project WHERE user_id = {}".format(user_id)
        success, results = self.select(sql)
        if success == False:
            return None
        ret = []
        for dict in results:
            ret.append(dict['project_name'])
        return ret

    def get_runs_id_list(self, project_id: int):
        """
        获取project的所有run_id
        @param project_id: project_id
        @return: run_id list / None(失败)
        """
        sql = "SELECT run_id FROM enroll_run WHERE project_id = {}".format(project_id)
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
        sql = "SELECT `key`, value FROM log_data WHERE run_id = {}".format(run_id)
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

        sql = "INSERT INTO run(run_id,project_id,config,state,start_time) VALUES({},{},\'{}\',\'{}\',\'{}\')".format(run_id,
                                                                                                                 project_id,
                                                                                                                 json.dumps(config),
                                                                                                                 "RUNNING",
                                                                                                                 datetime.datetime.now())
        print(sql)
        success2, results = self.query(sql)
        success = success1 & success2
        if not success:
            print("enroll run error!")
            return None
        return run_id

    def get_step(self, run_id):
        """
        获取当前run的step记录次数
        @param run_id:
        @return: step
        """
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

    def end_run(self,project_id:int,run_id:int):
        """
        作为module的析构函数使用
        记录duration
        @param project_id: project_id
        @param run_id: run_id
        @return:
        """
        sql = 'UPDATE run SET state = "END" WHERE project_id = {} AND run_id = {}'.format(project_id, run_id)
        success1, result1 = self.query(sql)
        sql = 'SELECT start_time FROM run WHERE project_id = {} AND run_id = {}'.format(project_id, run_id)
        success2, result2 = self.select(sql)
        time_start = result2[0]["start_time"]
        duration = datetime.datetime.now() - time_start
        sql = 'UPDATE run SET duration = \'{}\' WHERE project_id = {} AND run_id = {}'.format(duration, project_id,
                                                                                              run_id)
        # print(sql)
        success3, result3 = self.query(sql)
        success = (success1 & success2 & success3)
        if not success:
            print("del error!")


if __name__ == '__main__':
    query = sql_query()
    config = {"test":100}
    query.enroll_run(user_id=-1,project_id=27,run_name="test_config_dump_4",config=config)