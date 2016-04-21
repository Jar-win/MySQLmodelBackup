#!/usr/bin/env python
import MySQLdb as msd
#import json
import ast
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class Model():

	def __init__(self, **kwargs):
 	    self.host = kwargs.get('host', 'localhost')
	    self.user = kwargs.get('user', 'root')
	    self.password = kwargs.get('password', 'password')
            self.database = kwargs.get('database', '')
            self.table_name = kwargs.get('table','')
	    self.dbs = None


        def create_connection(self):
	    self.dbs = msd.connect(self.host,self.user,self.password, self.database)


	def close_connection(self):
	    self.dbs.close()


        def raw_query(self, query):
            cursor = self.dbs.cursor()
            try:
                cursor.execute(query)
                response = cursor.fetchall()
                return response
            except:
                return -1


        def push(self, **kwargs):
            table = kwargs.get('table', self.table_name)
	    cursor = self.dbs.cursor()
            try:
                del kwargs['table']
            except KeyError:
                pass
            QUERY ="INSERT INTO {} (".format(table)
            for name, value in kwargs.items():
                QUERY+=name+","
            safe_markup = '%s,'*len(kwargs.values()); safe_markup=safe_markup[:-1]
            QUERY=QUERY[:-1]+") VALUES ({})".format(safe_markup)
            try:
                cursor.execute(QUERY, (kwargs.values()))
		self.dbs.commit()
	    except :
                self.dbs.rollback()
                return -1
		

	def search(self,**kwargs):
            param = kwargs.get('param', 0)
            column = kwargs.get('search_column', '')
            table = kwargs.get('table', self.table_name)
            where = kwargs.get('where', '')
            where_value = kwargs.get('search_entity', '')
            and_clause = kwargs.get('and_clause','') 
            and_value = kwargs.get('and_value')
            like = kwargs.get('like', False)
            where_value_list = []
            where_value_list.append(where_value)

	    cursor = self.dbs.cursor()
            Query_string = "SELECT {} FROM {}  WHERE {} = %s".format(column, table, where)
            if and_clause:
                Query_string += ' AND {} = %s'.format(and_clause)
                where_value_list.append(and_value)
           
	    cursor.execute(Query_string, (where_value_list))
	    response = cursor.fetchall()

	    if param == 0 and response:
	    	response = response[0]
	    	response_list = list(response)
                return response_list
	    return response


	def update(self, **kwargs):
            update_table = kwargs.get('update_table', self.table_name)
            where_column = kwargs.get('where_column', '')           
            where_clause = kwargs.get('where_clause', '')           
            change_column = kwargs.get('change_column', '')
            change_to = kwargs.get('change_to', '')

            QUERY = "UPDATE {} SET ".format(update_table)
            for column in kwargs['change_column']:
                QUERY+=column+"=%s, "
            QUERY = QUERY[:-2]+' WHERE {}=%s'.format(where_column)
            change_to.append(where_clause)
            try:
                cursor = self.dbs.cursor()               
                cursor.execute(QUERY, (change_to))
                self.dbs.commit()
                response = cursor.fetchall()
                return response
            except:
                self.dbs.rollback()
                return -1


######################################################################################################################
#         c = Model( database='Test', table="test_table")                                                           #
#         c.create_connection()                                                                                      #
#         c.update(change_column=['alpha'], change_to=['Sharth'], where_column='id', where_clause='1')               #
#         c.push(table="test_table", alpha='); DROP TABLE `test_table`;', beta='1eebbebeb2bebebe4beebebebbeb24')     #
#         c.search(search_column='alpha, beta', table='test_table', where='id', search_entity='2')                   #
#         c.close_connection()                                                                                       #
######################################################################################################################


