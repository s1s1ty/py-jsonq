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
        :@type query_items: dict
        """
        temp_index = self._current_query_index
        if len(self._queries)-1 < temp_index:
            self._queries.append([])
        self._queries[temp_index].append(query_items)

    def __prepare(self):
        """
        :prepare query result
        """
        if len(self._queries) > 0:
            self.__execute_queries()
            self.__reset_queries()

    def __execute_queries(self):
        """
        :execute all condition and filter result data
        """
        def func(item):
            or_check = False
            for queries in self._queries:
                and_check = True
                for query in queries:
                    and_check &= self._helper._match(
                        item.get(query.get('key'), None),
                        query.get('operator'),
                        query.get('value')
                    )
                or_check |= and_check
            return or_check

        self._json_data = list(filter(lambda item: func(item), self._json_data))

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
        self._current_query_index += 1
        self.__store_query({"key": key, "operator": operator, "value": value})
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
        self.where(key, 'notin', value)
        return self

    def where_null(self, key):
        """
        :make where_null clause
        :@param key
        :@type key: string

        :@return self
        """
        self.where(key, '=', 'None')
        return self

    def where_not_null(self, key):
        """
        :make where_not_null clause
        :@param key
        :@type key: string

        :@return self
        """
        self.where(key, '!=', 'None')
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

    def where_end_with(self, key, value):
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
