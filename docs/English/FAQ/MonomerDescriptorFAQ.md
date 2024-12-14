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