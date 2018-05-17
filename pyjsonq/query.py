import json
import os
import copy
import math

from .matcher import Matcher


class JsonQ(object):
    """Query over Json file"""

    def __init__(self, file_path="", data={}):
        """
        :@param file_path: Set main json file path
        :@type file_path: string
        """
        if file_path != "":
            self.from_file(file_path)

        if data:
            self.__parse_json_data(data)

        self.__reset_queries()
        self._matcher = Matcher()

    def __reset_queries(self):
        """Reset previous query data"""

        self._queries = []
        self._current_query_index = 0

    def __parse_json_data(self, data):
        """Process Json data

        :@param data
        :@type data: json/dict

        :throws TypeError
        """
        if isinstance(data, dict) or isinstance(data, list):
            self._raw_data = data
            self._json_data = copy.deepcopy(self._raw_data)
        else:
            raise TypeError("Provided Data is not json")

    def __parse_json_file(self, file_path):
        """Process Json file data

        :@param file_path
        :@type file_path: string

        :@throws IOError
        """
        if file_path == '' or os.path.splitext(file_path)[1] != '.json':
            raise IOError('Invalid Json file')

        with open(file_path) as json_file:
            self._raw_data = json.load(json_file)

        self._json_data = copy.deepcopy(self._raw_data)

    def __get_value_from_data(self, key, data):
        """Find value from json data

        :@pram key
        :@type: string

        :@pram data
        :@type data: dict

        :@return object
        :@throws KeyError
        """
        if key.isdigit():
            return data[int(key)]

        if key not in data:
            raise KeyError("Key not exists")

        return data.get(key)

    def get(self):
        """Getting prepared data

        :@return object
        """
        self.__prepare()
        return self._json_data

    def from_file(self, file_path):
        """Set main json file path

        :@param file_path
        :@type file_path: string

        :@throws FileNotFoundError
        """
        self.__parse_json_file(file_path)
        return self

    def at(self, root):
        """Set root where PyJsonq start to prepare

        :@param root
        :@type root: string

        :@return self
        :@throws KeyError
        """
        leafs = root.strip(" ").split('.')
        for leaf in leafs:
            if leaf:
                self._json_data = self.__get_value_from_data(leaf, self._json_data)
        return self

    def clone(self):
        """Clone the exact same copy of the current object instance."""
        return copy.deepcopy(self._json_data)

    def reset(self, data={}):
        """JsonQuery object cen be reset to new data

        according to given data or previously given raw Json data

        :@param data: {}
        :@type data: json/dict

        :@return self
        """
        if data and (isinstance(data, dict) or isinstance(data, list)):
            self._json_data = data
        else:
            self._json_data = copy.deepcopy(self._raw_data)

        self.__reset_queries()
        return self

    def __store_query(self, query_items):
        """Make where clause

        :@param query_items
        :@type query_items: dict
        """
        temp_index = self._current_query_index
        if len(self._queries) - 1 < temp_index:
            self._queries.append([])

        self._queries[temp_index].append(query_items)

    def __prepare(self):
        """Prepare query result"""

        if len(self._queries) > 0:
            self.__execute_queries()
            self.__reset_queries()

    def __execute_queries(self):
        """Execute all condition and filter result data"""

        def func(item):
            or_check = False
            for queries in self._queries:
                and_check = True
                for query in queries:
                    and_check &= self._matcher._match(
                        item.get(query.get('key'), None),
                        query.get('operator'),
                        query.get('value')
                    )
                or_check |= and_check
            return or_check

        self._json_data = list(filter(lambda item: func(item), self._json_data))

    # ---------- Query Methods ------------- #

    def where(self, key, operator, value):
        """Make where clause

        :@param key
        :@param operator
        :@param value
        :@type key,operator,value: string

        :@return self
        """
        self.__store_query({"key": key, "operator": operator, "value": value})
        return self

    def or_where(self, key, operator, value):
        """Make or_where clause

        :@param key
        :@param operator
        :@param value
        :@type key, operator, value: string

        :@return self
        """
        if len(self._queries) > 0:
            self._current_query_index += 1
        self.__store_query({"key": key, "operator": operator, "value": value})
        return self

    def where_in(self, key, value):
        """Make where_in clause

        :@param key
        :@param value
        :@type key, value: string

        :@return self
        """
        self.where(key, 'in', value)
        return self

    def where_not_in(self, key, value):
        """Make where_not_in clause

        :@param key
        :@param value
        :@type key, value: string

        :@return self
        """
        self.where(key, 'notin', value)
        return self

    def where_null(self, key):
        """Make where_null clause

        :@param key
        :@type key: string

        :@return self
        """
        self.where(key, '=', 'None')
        return self

    def where_not_null(self, key):
        """Make where_not_null clause

        :@param key
        :@type key: string

        :@return self
        """
        self.where(key, '!=', 'None')
        return self

    def where_start_with(self, key, value):
        """Make where_start_with clause

        :@param key
        :@param value
        :@type key,value: string

        :@return self
        """
        self.where(key, 'startswith', value)
        return self

    def where_end_with(self, key, value):
        """Make where_ends_with clause.

        :@param key
        :@param value
        :@type key,value: string

        :@return self
        """
        self.where(key, 'endswith', value)
        return self

    def where_contains(self, key, value):
        """Make where_contains clause.

        :@param key
        :@param value
        :@type key,value: string

        :@return self
        """
        self.where(key, 'contains', value)
        return self

    # ---------- Aggregate Methods ------------- #

    def count(self):
        """Getting the size of the collection

        :@return int
        """
        self.__prepare()
        return len(self._json_data)

    def size(self):
        """Getting the size of the collection

        :@return int
        """
        self.__prepare()
        return len(self._json_data)

    def first(self):
        """Getting the first element of the collection otherwise None

        :@return object
        """
        self.__prepare()
        return self._json_data[0] if self.count() > 0 else None

    def last(self):
        """Getting the last element of the collection otherwise None

        :@return object
        """
        self.__prepare()
        return self._json_data[-1] if self.count() > 0 else None

    def nth(self, index):
        """Getting the nth element of the collection

        :@param index
        :@type index: int

        :@return object
        """
        self.__prepare()
        return None if self.count() < math.fabs(index) else self._json_data[index]

    def sum(self, property):
        """Getting the sum according to the given property

        :@param property
        :@type property: string

        :@return int/float
        """
        self.__prepare()
        total = 0
        for i in self._json_data:
            total += i.get(property)

        return total

    def max(self, property):
        """Getting the maximum value from the prepared data

        :@param property
        :@type property: string

        :@return object
        :@throws KeyError
        """
        self.__prepare()
        try:
            return max(self._json_data, key=lambda x: x[property]).get(property)
        except KeyError:
            raise KeyError("Key is not exists")

    def min(self, property):
        """Getting the minimum value from the prepared data

        :@param property
        :@type property: string

        :@return object
        :@throws KeyError
        """
        self.__prepare()
        try:
            return min(self._json_data, key=lambda x: x[property]).get(property)
        except KeyError:
            raise KeyError("Key is not exists")

    def avg(self, property):
        """Getting average according to given property

        :@param property
        :@type property: string

        :@return average: int/float
        """
        self.__prepare()
        return self.sum(property) / self.count()

    def chunk(self, size=0):
        """Group the resulted collection to multiple chunk

        :@param size: 0
        :@type size: integer

        :@return Chunked List
        """

        if size == 0:
            raise ValueError('Invalid chunk size')

        self.__prepare()
        _new_content = []

        while(len(self._json_data) > 0):
            _new_content.append(self._json_data[0:size])
            self._json_data = self._json_data[size:]

        self._json_data = _new_content

        return self._json_data

    def group_by(self, property):
        """Getting the grouped result by the given property

        :@param property
        :@type property: string

        :@return self
        """
        self.__prepare()
        group_data = {}
        for data in self._json_data:
            if data[property] not in group_data:
                group_data[data[property]] = []
            group_data[data[property]].append(data)
        self._json_data = group_data

        return self

    def sort(self, order="asc"):
        """Getting the sorted result of the given list

        :@param order: "asc"
        :@type order: string

        :@return self
        """
        self.__prepare()
        if isinstance(self._json_data, list):
            if order == "asc":
                self._json_data = sorted(self._json_data)
            else:
                self._json_data = sorted(self._json_data, reverse=True)

        return self

    def sort_by(self, property, order="asc"):
        """Getting the sorted result by the given property

        :@param property, order: "asc"
        :@type property, order: string

        :@return self
        """
        self.__prepare()
        if isinstance(self._json_data, list):
            if order == "asc":
                self._json_data = sorted(
                    self._json_data,
                    key=lambda x: x.get(property)
                )
            else:
                self._json_data = sorted(
                    self._json_data,
                    key=lambda x: x.get(property),
                    reverse=True
                )

        return self
