from ..monomer import MonomerPropertyDescriptor

class MyClass:
    myattr = MonomerPropertyDescriptor(
        default=0,
        type=int,
        writable=True,
        immutable=False,
        non_iterable=False,
        read_only=False,
        error_messages={
            "type": "Value must be an integer.",
            "immutable": "Attribute 'myattr' is immutable."
        },
        validator=lambda x: x > 0,
        depends_on=None,
        serialize=True,
        log_changes=True,
        access_control=lambda instance: instance.has_permission,
        version_control=True,
        lazy=True,
        factory=lambda instance: 42  # 示例工厂函数
    )

    def __init__(self, value=None, has_permission=True):
        self.has_permission = has_permission
        if value is not None:
            self.myattr = value

# 示例操作
obj = MyClass()
print(obj.myattr)  # 懒加载属性将被初始化并返回
obj.myattr = 30  # 设置新值并执行回调函数
print(obj.myattr)
print(MyClass.myattr.get_history())  # 属性值的历史变更

# 添加回调函数
def my_callback(instance, value):
    print(f"Callback called with value: {value}")

MyClass.myattr.add_callback(my_callback)
obj.myattr = 40  # 设置新值，触发回调函数