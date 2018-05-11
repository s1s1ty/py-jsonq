import json
import os
import copy

from .helper import Helper


class JsonQuery(object):
    """Query over Json file"""

    def __init__(self, file_path=""):
        """
        :@param file_path: Set main json file path
        :@type file_path: string
        """
        if file_path != "":
            self.set_path(file_path)

        self.__reset_queries()
        self._helper = Helper()

    def __reset_queries(self):
        """
        :Reset previous query data
        """
        self._queries = [];
        self._current_query_index = 0;

    def __parse_json_file(self, file_path):
        """
        :Process Json file data
        :@param file_path
        :@type file_path: string

        :@throws FileNotFoundError
        """
        if file_path == '' or os.path.splitext(file_path)[1] != '.json':
            raise FileNotFoundError('Json file not found')

        with open(file_path) as json_file:
            self._raw_data = json.load(json_file)

        self._json_data = copy.deepcopy(self._raw_data)

    def __get_value_from_data(self, key, data):
        """
        :Find value from json data
        :@pram key
        :@type: string

        :@pram data
        :@type data: dict

        :@return object value
        :@throws KeyError
        """
        if key not in data:
            raise KeyError("Key not exists")
        return data.get(key)

    def get(self):
        """
        :Getting prepared data
        :@return object
        """
        self.__prepare()
        return self._json_data

    def set_path(self, file_path):
        """
        :Set main json file path
        :@param file_path
        :@type file_path: string

        :@throws FileNotFoundError
        """
        self.__parse_json_file(file_path)
        return self

    def at(self, root):
        """
        :Set root where PyJsonq start to prepare
        :@param root
        :@type root: string

        :@return self
        :@throws KeyError
        """
        leafs = root.strip(" ").split('.')

        for leaf in leafs:
            self._json_data = self.__get_value_from_data(leaf, self._json_data)
        return self

    def __store_query(self, query_items):
        """
        :make where clause
        :@param query_items
        :@type query_items: list
        """
        index = self._current_query_index
        self._queries[index].append(query_items)

    def __prepare(self):
        """
        :prepare query result
        """
        if len(self._queries) > 0:
            self.__execute_queries()
            self.__reset_queries()

    def __execute_queries(self):
        pass

    # ---------- Query Methods ------------- #

    def where(self, key, operator, value):
        """
        :make where clause
        :@param key
        :@param operator
        :@param value
        :@type key,operator,value: string

        :@return self
        """
        self.__store_query({"key": key, "operator": operator, "value": value})
        return self

    def or_where(self, key, operator, value):
        """
        :make or_where clause
        :@param key
        :@param operator
        :@param value
        :@type key, operator, value: string

        :@return self
        """
        self.where(key)
        return self

    def where_in(self, key, value):
        """
        :make where_in clause
        :@param key
        :@param value
        :@type key, value: string

        :@return self
        """
        self.where(key, 'in', value)
        return self

    def where_not_in(self, key, value):
        """
        :make where_not_in clause
        :@param key
        :@param value
        :@type key, value: string

        :@return self
        """
        self.where(key, 'in', value)
        return self

    def where_null(self, key):
        """
        :make where_null clause
        :@param key
        :@type key: string

        :@return self
        """
        self.where(key, 'null')
        return self

    def where_not_null(self, key):
        """
        :make where_not_null clause
        :@param key
        :@type key: string

        :@return self
        """
        self.where(key, 'notnull')
        return self

    def where_start_with(self, key, value):
        """
        :make where_start_with clause
        :@param key
        :@param value
        :@type key,value: string

        :@return self
        """
        self.where(key, 'startswith', value)
        return self

    def where_ends_with(self, key, value):
        """
        :make where_ends_with clause
        :@param key
        :@param value
        :@type key,value: string

        :@return self
        """
        self.where(key, 'endswith', value)
        return self

    def where_contains(self, key, value):
        """
        :make where_contains clause
        :@param key
        :@param value
        :@type key,value: string

        :@return self
        """
        self.where(key, 'contains', value)
        return self
