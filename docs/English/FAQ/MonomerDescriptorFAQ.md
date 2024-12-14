# Common Issues and Solutions for `MonomerPropertyDescriptor`

When using the `MonomerPropertyDescriptor` descriptor, you may encounter some issues, especially when performing class-priority operations at the instance level, such as retrieving the history of an attribute or iterating over an attribute's value. Below are some common issues and their solutions.

## Issue: Unable to Perform Class-Priority Operations at the Instance Level

When using the `MonomerPropertyDescriptor` descriptor, attempting to call descriptor-specific methods directly on an instance will result in errors because these methods exist on the descriptor instance, not on the attribute value itself.

### Example Code

```python
class MyClass:
    myattr = MonomerPropertyDescriptor(version_control=True, non_iterable=False)

test_obj = MyClass()
test_obj.myattr = [1, 2, 3]
test_obj.myattr.append(4)
# The following code will cause an error because myattr is a list, which does not have a get_history method
history = test_obj.myattr.get_history()
# The following code will also cause an error because myattr is a list, which will be iterated directly without triggering the descriptor's __iter__ method
for item in test_obj.myattr:
    print(item)
```

### Error Messages

```
AttributeError: 'list' object has no attribute 'get_history'
```

Or

```
TypeError: 'list' object is not iterable
```

### Solutions

1. **Perform Operations at the Class Level**:

   If it is acceptable to perform operations at the class level, you can directly call the corresponding method on the descriptor.
   
```python
     history = MyClass.myattr.get_history()
```

2. **Use Class Methods to Perform Operations**:

   Define a method within the class that internally calls the corresponding method of the descriptor.
   
```python
class MyClass:
    myattr = MonomerPropertyDescriptor(version_control=True, non_iterable=False)

    def get_myattr_history(self):
        return self.myattr.get_history(self)

    def iterate_myattr(self):
        return self.myattr.__iter__(self)

test_obj = MyClass()
history = test_obj.get_myattr_history()
for item in test_obj.iterate_myattr():
    print(item)
```

---

## Error: Using a Class Instead of an Instance in Property Dependency Checks

When using the `depends_on` decorator with `MonomerPropertyDescriptor`, a common mistake is to pass a class as an argument to the lambda function instead of an instance of the class.

### Error Example

```python
class SampleClass:
    prop1 = MonomerPropertyDescriptor(default=0)
    prop2 = MonomerPropertyDescriptor(default=0, depends_on=lambda cls: cls.prop1 > 0)
```

In the code above, the `depends_on` decorator uses the `cls` parameter, which is typically a reference to the class itself, not an instance of the class. This will cause the property dependency check to fail, as it does not trigger the `get` method of the descriptor.

### Solution

To address this issue, you should ensure that the `depends_on` decorator uses an instance of the class. Here is an example of how to correctly implement the property dependency check:

```python
class SampleClass:
    prop1 = MonomerPropertyDescriptor(default=0, version_control=True)
    prop2 = MonomerPropertyDescriptor(default=0, depends_on=lambda instance: instance.prop1 > 0)
```

In this corrected example, the `depends_on` decorator takes advantage of the fact that by calling `instance.prop1`, we can access the value of `prop1` to determine whether setting `prop2` is allowed.

### Considerations

- Make sure that the lambda function within the `depends_on` decorator accepts `instance` as a parameter.

---