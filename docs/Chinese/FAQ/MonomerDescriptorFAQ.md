# MonomerPropertyDescriptor 常见问题及解决方案

在使用 `MonomerPropertyDescriptor` 描述符时，可能会遇到一些问题，尤其是在实例级别上执行一些基于类优先级的操作，例如获取属性的历史记录、迭代属性值等。以下是一些常见问题及其解决方案。

## 问题：无法在实例级别执行基于类优先级的操作

当使用 `MonomerPropertyDescriptor` 描述符时，直接在实例上调用描述符特有的方法会导致错误，因为这些方法存在于描述符实例上，而不是属性值本身。

### 示例代码

```python
class MyClass:
    myattr = MonomerPropertyDescriptor(version_control=True, non_iterable=False)

test_obj = MyClass()
test_obj.myattr = [1, 2, 3]
test_obj.myattr.append(4)
# 以下代码会导致错误，因为 myattr 是一个 list，没有 get_history 方法
history = test_obj.myattr.get_history()
# 以下代码也会导致错误，因为 myattr 是一个 list，会直接迭代而不会触发描述符的 __iter__ 方法
for item in test_obj.myattr:
    print(item)
```

### 错误信息

```
AttributeError: 'list' object has no attribute 'get_history'
```

或者

```
TypeError: 'list' object is not iterable
```

### 解决方案

1. **在类级别上执行操作**：

   如果可以接受在类级别上执行操作，可以直接在描述符上调用相应的方法。
   
```python
     history = MyClass.myattr.get_history()
```

2. **使用类方法来执行操作**：

   在类中定义一个方法，该方法在内部调用描述符的相应方法。
   
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