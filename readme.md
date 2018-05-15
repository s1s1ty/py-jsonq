# py-jsonq

**py-jsonq** is a simple, elegant Python package to Query over any type of JSON Data. It'll make your life easier by giving the flavour of an ORM-like query on your JSON.

This package is inspired from the awesome [jsonq](https://github.com/nahid/jsonq) package.

## Installation

```
pip install pyjsonq
```

## Usage

Just import the package before start using it.

As a Python Package:

```python
from pyjsonq.query import JsonQ
```

You can start using this package right away by importing your Json data from a file:

```Python
JsonQ('data.json')
```
or

```Python
JsonQ(data={"id": 1, "name": "shaonty"})
```

You can start Query your data using the various query methods such as **where**, **or_where**, **where_in**, **where_not_in**, **where_starts_with**, **where_ends_with**, **where_contains** and so on. Also you can aggregate your data after query using **sum**, **count**, **group_by**, **sort_by**, **max**, **min** etc.

Let's see a quick example:

```python
# sample Json data
json_object = {
    products: [
        {
            id: 1,
            city: 'bsl',
            name: 'iPhone',
            cat: 1,
            price: 80000.5
        },
        {
            id: 2,
            city: null,
            name: 'macbook pro',
            cat: 1,
            price: 150000
        },
        {
            id: 3,
            city: 'dhk',
            name: 'Redmi 3S Prime',
            cat: 2,
            price: 12000
        },
        {
            id: 4,
            city: 'bsl',
            name: 'macbook air',
            cat: 2,
            price: 110000
        }
    ]
};

qe = JsonQ(file_path)
res = q.at('products').where('cat', '=', 2).get()
print(res)

"""This will print

[
    {
        id: 3,
        city: 'dhk',
        name: 'Redmi 3S Prime',
        cat: 2,
        price: 12000
    },
    {
        id: 4,
        city: 'bsl',
        name: 'macbook air',
        cat: 2,
        price: 110000
    }
]
"""
```

Let's say we want to get the Summation of _price_ of the Queried result. We can do it easily by calling the **sum()** method instead of **get()**:

```Python
res = q.at('products').where('cat', '=', 2).sum('price')
print(res)
"""It will print:

122000

"""
```

Let's explore the full API to see what else magic this library can do for you.
Shall we?

## API

Following API examples are shown based on the sample JSON data given [here](examples/data.json). To get a better idea of the examples see that JSON data first. Also detailed examples of each API can be found [here](examples/).

**List of API:**

* [get](#get)
* [from_path](#from_filefile_path)
* [at](#atpath)
* [where](#wherekey-operator-value)
* [or_where](#orwherekey-operator-value)
* [where_in](#where_inkey-value)
* [where_not_in](#where_not_inkey-value)
* [where_null](#where_nullkey)
* [where_not_null](#where_not_nullkey)
* [where_starts_with](#where_starts_withkey-value)
* [where_ends_with](#where_ends_withkey-value)
* [where_contains](#where_containskey-value)
* [sum](#sumproperty)
* [count](#count)
* [size](#size)
* [max](#maxproperty)
* [min](#minproperty)
* [avg](#avgproperty)
* [first](#first)
* [last](#last)
* [nth](#nthindex)
* [group_by](#group_byproperty)
* [sort](#sortorder)
* [sortBy](#sortbyproperty-order)
* [reset](#resetdata)
* [clone](#clone)

### `get()`

This method will execute queries and will return the resulted data. You need to call it finally after using some query methods. Details can be found in other API examples.

### `from_file(file_path)`

This method is the alternative of set json file path. Details can be found in other API examples.

**example:**

Let's say you have a file named `data.json`. You can set path like this:

```Python
qu = JsonQ().from_file('data.json').at('users').where('id', '=', 1).get()
```

### `at(path)`

* `path` -- the path hierarchy of the data you want to start query from.

By default, query would be started from the root of the JSON Data you've given. If you want to first move to a nested path hierarchy of the data from where you want to start your query, you would use this method. Skipping the `path` parameter or giving **'.'** as parameter will also start query from the root Data.


**example:**

Let's say you want to start query over the values of _'users'_ property of your Json Data. You can do it like this:

```Python
qu = JsonQ(file_path).at('users').where('id', '=', 1).get()
```

If you want to traverse to more deep in hierarchy, you can do it like:

```Python
qe = JsonQ(file_path).at('users.5.visits').where('year', '=', 2011).get()
```

See a detail example [here](examples/at.py).

### `where(key, operator, value)`

* `key` -- the property name of the data. Or you can pass a Function here to group multiple query inside it. See details in [example](examples/where.py)
* `value` -- value to be matched with. It can be a _int_, _string_, _bool_ or even _float_ - depending on the `operator`.
* `operator` -- operand to be used for matching. The following operands are available to use:

    * `=` : For equality matching
    * `eq` : Same as `=`
    * `!=` : For weak not equality matching
    * `neq` : Same as `!=`
    * `>` : Check if value of given **key** in data is Greater than **value**
    * `gt` : Same as `>`
    * `<` : Check if value of given **key** in data is Less than **value**
    * `lt` : Same as `<`
    * `>=` : Check if value of given **key** in data is Greater than or Equal of **value**
    * `gte` : Same as `>=`
    * `<=` : Check if value of given **key** in data is Less than or Equal of **value**
    * `lte` : Same as `<=`
    * `null` : Check if the value of given **key** in data is **null** (`value` parameter in `where()` can be omitted for this `operator`)
    * `notnull` : Check if the value of given **key** in data is **not null** (`value` parameter in `where()` can be omitted for this `operator`)
    * `in` : Check if the value of given **key** in data is exists in given **value**. **value** should be a plain _List_.
    * `notin` : Check if the value of given **key** in data is not exists in given **val**. **val** should be a plain _List_.
    * `startswith` : Check if the value of given **key** in data starts with (has a prefix of) the given **value**. This would only works for _String_ type data.
    * `endswith` : Check if the value of given **key** in data ends with (has a suffix of) the given **value**. This would only works for _String_ type data.
    * `contains` : Same as `in`

**example:**

Let's say you want to find the _'users'_ who has _id_ of `1`. You can do it like this:

```Python
qu = JsonQ(file_path).at('users').where('id', '=', 1).get()
```

You can add multiple _where_ conditions. It'll give the result by AND-ing between these multiple where conditions.

```Python
qe = JsonQ(file_path).at('users').where('id', '=', 1).where('location', '=', 'Sylhet').get()
```

See a detail example [here](examples/where.py).

### `or_where(key, operator, value)`

Parameters of `or_where()` are the same as `where()`. The only difference between `where()` and `or_where()` is: condition given by the `or_where()` method will OR-ed the result with other conditions.

For example, if you want to find the users with _id_ of `1` or `2`, you can do it like this:

```Python
re = JsonQ(file_path).at('users').where('id', '=', 1).or_where('id', '=', 2).get()
```

See detail example [here](examples/or_where.py).

### `where_in(key, value)`

* `key` -- the property name of the data
* `value` -- it should be an **List**

This method will behave like `where(key, 'in', value)` method call.

### `where_not_in(key, value)`

* `key` -- the property name of the data
* `value` -- it should be an **List**

This method will behave like `where(key, 'notin', value)` method call.

### `where_null(key)`

* `key` -- the property name of the data

This method will behave like `where(key, '=', 'None')` method call.

### `where_not_null(key)`

* `key` -- the property name of the data

This method will behave like `where(key, '!=', 'None')` method call.

### `where_starts_with(key, value)`

* `key` -- the property name of the data
* `value` -- it should be a String

This method will behave like `where(key, 'startswith', value)` method call.

### `where_ends_with(key, value)`

* `key` -- the property name of the data
* `value` -- it should be a String

This method will behave like `where(key, 'endswith', value)` method call.

### `where_contains(key, val)`

* `key` -- the property name of the data
* `value` -- it should be a String or List

This method will behave like `where(key, 'contains', val)` method call.

### `sum(property)`

* `property` -- the property name of the data

**example:**

Let's say you want to find the sum of the _'price'_ of the _'products'_. You can do it like this:

```Python
qe = JsonQ(file_path).at('products').sum('price')
```

If the data you are aggregating is plain list, you don't need to pass the 'property' parameter.
See detail example [here](examples/sum.py)

### `count()`

It will return the number of elements in the collection.

**example:**

Let's say you want to find how many elements are in the _'products'_ property. You can do it like:

```Python
qe = JsonQ(file_path).at('products').count()
```

See detail example [here](examples/count.py).

### `size()`

This is an alias method of `count()`.

### `max(property)`

* `property` -- the property name of the data

**example:**

Let's say you want to find the maximum of the _'price'_ of the _'products'_. You can do it like this:

```Python
qu = JsonQ(file_path).at('products').max('price')
```

If the data you are querying is plain array, you don't need to pass the 'property' parameter.
See detail example [here](examples/max.py)

### `min(property)`

* `property` -- the property name of the data

**example:**

Let's say you want to find the minimum of the _'price'_ of the _'products'_. You can do it like this:

```Python
qe = JsonQ(file_path).at('products').min('price')
```

If the data you are querying is plain array, you don't need to pass the 'property' parameter.
See detail example [here](examples/min.py)

### `avg(property)`

* `property` -- the property name of the data

**example:**

Let's say you want to find the average of the _'price'_ of the _'products'_. You can do it like this:

```Python
qe = JsonQ(file_path).at('products').avg('price')
```

If the data you are querying is plain array, you don't need to pass the 'property' parameter.
See detail example [here](examples/avg.py)

### `first()`

It will return the first element of the collection.

**example:**

```Python
qe = JsonQ(file_path).at('products').first()
```

See detail example [here](examples/first.py).

### `last()`

It will return the last element of the collection.

**example:**

```Python
qe = JsonQ(file_path).at('products').last()
```

See detail example [here](examples/last.py).

### `nth(index)`

* `index` -- index of the element to be returned.

It will return the nth(n starts from 0) element of the collection. If the given index is a **positive** value, it will return the nth element from the beginning. If the given index is a **negative** value, it will return the nth element from the end.

**example:**

```Python
qe = JsonQ(file_path).at('products').nth(2)
```

See detail example [here](examples/nth.py).


### `group_by(property)`

* `property` -- The property by which you want to group the collection.

**example:**

Let's say you want to group the _'users'_ data based on the _'location'_ property. You can do it like:

```Python
qe = JsonQ(file_path).at('users').group_by('location').get()
```

See detail example [here](examples/group_by.py).

### `sort(order)`

* `order` -- If you skip the _'order'_ property the data will be by default ordered as **ascending**. You need to pass **'desc'** as the _'order'_ parameter to sort the data in **descending** order. Also, you can pass a compare function in _'order'_ parameter to define your own logic to order the data.

**Note:** This method should be used for plain Array. If you want to sort an Array of Objects you should use the **sortBy()** method described later.

**example:**

Let's say you want to sort the _'arr'_ data. You can do it like:

```Python
qe = JsonQ(file_path).at('arr').sort().get()
```

See detail example [here](examples/sort.py).

### `sort_by(property, order)`

* `property` -- You need to pass the property name on which the sorting will be done.
* `order` -- If you skip the _'order'_ property the data will be by default ordered as **ascending**. You need to pass **'desc'** as the _'order'_ parameter to sort the data in **descending** order. Also, you can pass a compare function in _'order'_ parameter to define your own logic to order the data.

**Note:** This method should be used for Array of Objects. If you want to sort a plain Array you should use the **sort()** method described earlier.

**example:**

Let's say you want to sort the _'price'_ data of _'products'_. You can do it like:

```Python
qe = JsonQ(file_path).at('products').sort_by('price').get()
```

See detail example [here](examples/sort_by.py).

### `reset(data)`

* `data` -- can be a JSON file path, or a JSON string or a JSON Object. If no data passed in the `data` parameter, the `JsonQ` Object instance will be reset to previously initialised data.

At any point, you might want to reset the Object instance to a completely different set of data and then query over it. You can use this method in that case.

See a detail example [here](examples/reset.py).

### `clone()`

It will return a complete clone of the Object instance.

See a detail example [here](examples/clone.py).


## Bugs and Issues

If you encounter any bugs or issues, feel free to [open an issue at
github](https://github.com/s1s1ty/py-jsonq/issues).

Also, you can shoot me an email to
<mailto:shaonty.dutta@gmail.com> for suggestion or bugs.

## Credit

Speical thanks to [Nahid Bin Azhar](https://github.com/nahid) for the inspiration and guidance for the package.

## Others Platform
- [php-jsonq](https://github.com/nahid/jsonq)
- [js-jsonq](https://github.com/me-shaon/js-jsonq)
