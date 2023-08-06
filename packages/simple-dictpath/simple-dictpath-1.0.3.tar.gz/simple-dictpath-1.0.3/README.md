# Simple DictPath
Provides a simple path-like access to nested dictionary elements

# Install
```bash
pip install simple-dictpath
```

# Examples
```python
from dictpath import dictp

# First declare a dictp, just like a regular dict.
testval = dictp({
    "first": {
        "second": {
            "animals": [
                {
                    "type": "cat",
                    "name": "meow1",
                    "children": 2
                },
                {
                    "type": "cat",
                    "name": "meow1",
                    "children": 4
                },
                {
                    "type": "cat",
                    "name": "meow1",
                    "children": 6
                },
                {
                    "type": "dog",
                    "name": "dog1",
                    "eye_colour": "blue"
                },
                {
                    "type": "dog",
                    "name": "dog2",
                    "eye_colour": "green"
                },
            ]
        }
    }
})

# dictps can behave just like regular dicts when needed:
# prints: 'meow1'
print(testval["first"]["second"]["animals"][0]["name"])

# But the power comes in cleanly accessing nested elements.
# To use, just call the dictp value like a function with '()' syntax:
animals = testval("first/second/animals")
print(animals)

# If a any key is missing, whole thing just returns None:
cars = testval("first/third/cars")
assert(cars is None)

# To force a keyError, use raise_if_missing:
# This throws: KeyError: 'third'
testval("first/third/cars", raise_if_missing=True)

# You can use list indexes to only get certain elements in a nested list
# prints: 'cat'
first = testval("first/second/animals/0/type")
print(first)

# Uses list comprehension, e.g. "1:2", ":-1", ":", etc.
last_two = testval("first/second/animals/-2:/type")
middle_cats = testval("first/second/animals/1:-2/name")
all_animals = testval("first/second/animals")
all_types = testval("first/second/animals/:/type")

# If key actually is a string with ":", use raw_index option
testval("real/key/:/a", raw_index=True)

# To only get list items that have a specific subkey, use drop_missing:
# This returns [None, None, None, 'blue', 'green']
testval("first/second/animals/:/eye_colour")
# This returns ['blue', 'green']
testval("first/second/animals/:/eye_colour", drop_missing=True)

# You can also set a overide the value if missing:
# This returns ['unknown', 'unknown', 'unknown', 'blue', 'green']
testval("first/second/animals/:/eye_colour", value_if_missing="unknown")

# These both return "no cars"
testval("first/second/cars", value_if_missing="no cars")
testval("first/second/cars/0/type", value_if_missing="no cars")
```
