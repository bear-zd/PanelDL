import pandas as pd
import numpy as np
import pymysql
from collections import defaultdict
from PanelDL.utils.sqlApi import mysqlConnect

class sql_query(mysqlConnect):
    # def __init__(self):
    #     self.conn = pymysql.connect(**Config)
    #     self.cursor = self.conn.cursor()

    # def __del__(self):
    #     self.cursor.close()
    #     self.conn.close()

    def get_user_id(self, email:str):
        sql = "SELECT user_id FROM user WHERE email = \'{}\'".format(email)
        # self.cursor.execute(sql)
        # results = self.cursor.fetchall()
        results = self.select(sql)
        try:
            if results[0] == True:
                results = results[1][0]
                assert(len(results) == 1)
            else:
                return None
        except:
            print("one email has multiple users")
        print("return user_id:")
        return results['user_id']

    def get_projects_id(self, user_id:int):
        sql = "SELECT project_id FROM enroll_project WHERE user_id = {}".format(str(user_id))
        # self.cursor.execute(sql)
        # results = self.cursor.fetchall()
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
    
    def get_runs_id(self, project_id:int):
        sql = "SELECT run_id FROM enroll_run WHERE project_id = {}".format(str(project_id))
        # self.cursor.execute(sql)
        # results = self.cursor.fetchall()
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
        # self.cursor.execute(sql)
        # results = self.cursor.fetchall()
        results = self.select(sql)
        if results[0 == True]:
            results = results[1]
        else:
            return None
        # results =np.array(results) 
        # dict = defaultdict(list)
        # for i in results:
        #     dict[i[0]].append(float(i[1]))
        # return dict
        dict = defaultdict(list)
        for dic in results:
            dict[dic['key']].append(dic['value'])
        return dict


if __name__ == '__main__':
    query = sql_query()
    print(query.get_user_id('3'))
    print(query.get_projects_id(4))
    print(query.get_runs_id(1))
    print(query.get_log(1))
