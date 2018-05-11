class Helper(object):
    """docstring for Helper."""
    def __init__(self):
        self.condition_mapper = {
            '=': '_is_equal',
            '!=': '_is_not_equal',
            '>': '_is_greater',
            '<': '_is_smaller',
            '>=': '_is_greater_equal',
            '<=': '_is_smaller_equal',
            'in': '_is_in',
            'notin': '_is_not_in',
            'null': '_is_null',
            'notnull': '_is_not_null',
            'startswith': '_is_starts_with',
            'endswith': '_is_ends_with',
        }

    def _is_equal(self, left_val, right_val):
        return left_val == right_val;

    def _is_not_equal(self, left_val, right_val):
        return left_val != right_val;

    def _is_greater(self, left_val, right_val):
        return left_val > right_val;

    def _is_smaller(self, left_val, right_val):
        return left_val < right_val;

    def _is_greater_equal(self, left_val, right_val):
        return left_val >= right_val;

    def _is_smaller_equal(self, left_val, right_val):
        return left_val <= right_val;

    def _is_in(self, key, arr):
        return isinstance(arr, list) and (key in arr)

    def _is_not_in(self, key, arr):
        return isinstance(arr, list) and (key not in arr)

    def _is_null(self, val):
        return val is None;

    def _is_not_null(self, val):
        return val is not None;

    def _match(self, left_val, op, right_val):
        if (op not in self.condition_mapper):
            raise ValueError('Invalid where condition given')

        func = getattr(self, self.condition_mapper.get(op))
        return func(left_val, right_val)
