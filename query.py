import json
import os
import copy

from .helper import Helper


class JsonQuery(object):
    """Query over Json file"""

    def __init__(self, file_path=""):
        """
        * Set main json file path
        * @param "" file_path
        """
        if file_path != "":
            self.set_path(file_path)

        self._reset_queries()
        self._helper = Helper()

    def _reset_queries(self):
        """
        * complete me
        """
        self._queries = [];
        self._current_query_index = 0;

    def _parse_json_file(self, file_path):
        """
        * Process Json file data
        * @param file_path
        * @throws FileNotFoundError
        """
        if file_path == '' or os.path.splitext(file_path)[1] != '.json':
            raise FileNotFoundError('Json file not found')

        with open(file_path) as json_file:
            self._raw_data = json.load(json_file)

        self._json_data = copy.deepcopy(self._raw_data)

    def _get_value(self, key, data):
        """
        * Find value from json data
        * @pram key
        * @pram data
        * @return object value
        * @throws KeyError
        """
        if key not in data:
            raise KeyError("Key not exists")

        return data[key]

    def get(self):
        """
        * Getting prepared data
        * @return object
        """
        return self._json_data

    def set_path(self, file_path):
        """
        * Set main json file path
        * @param file_path
        * @throws FileNotFoundError
        """
        self._parse_json_file(file_path)
        return self

    def at(self, root):
        """
        * Set root where PyJsonq start to prepare
        * @param root
        * @return self
        * @throws KeyError
        """
        leafs = root.strip(" ").split('.')

        for leaf in leafs:
            self._json_data = self._get_value(leaf, self._json_data)

        return self

    # ---------- Query Methods ------------- #

    def where(self, key, operator, val):
        """
        * Apply where condition
        * @param key
        * @param operator
        * @param val
        * @return self
        """
        pass
