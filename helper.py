class Helper(object):
    """docstring for Helper."""
    def __init__(self):
        self.condition_mapper = {
            "=": 'is_equal'
        }

    def is_equal(self, left_val, right_val):
        return left_val == right_val;

    def is_not_equal(self, left_val, right_val):
        return left_val != right_val;

    def is_greater(self, left_val, right_val):
        return left_val > right_val;


    def is_smaller(self, left_val, right_val):
        return left_val < right_val;


    def is_greater_or_equal(self, left_val, right_val):
        return left_val >= right_val;


    def is_smaller_or_equal(self, left_val, right_val):
        return left_val <= right_val;


    def is_in(self, key, arr):
        return Array.isArray(arr) and (key in arr)


    def is_not_in(self, key, arr):
        return Array.isArray(arr) and (key not in arr)


    def is_null(self, val):
        return val == None;


    def is_not_null(self, val):
        return val != None;

    def match(self, left_val, op, right_val):
        if (op not in self.condition_mapper):
            raise ValueError('Invalid where condition given')

        return self.condition_mapper[op](left_val, right_val)
