from ..monomer import MonomerPropertyDescriptor
import threading
import pdb
from ..monomer.libException import MonomerPropertyError

class TestObject:
    # 只读属性
    readonly_attr = MonomerPropertyDescriptor(read_only=True, default="readonly_value")
    
    # 类型检查
    int_attr = MonomerPropertyDescriptor(type=int, default=0)
    
    # 带有验证器的属性
    positive_int_attr = MonomerPropertyDescriptor(type=int, validator=lambda x: x > 0, default=1)
    
    # 版本控制
    versioned_attr = MonomerPropertyDescriptor(version_control=True, default=0)
    
    # 线程安全
    thread_safe_attr = MonomerPropertyDescriptor(thread_safe=True, default=0)
    
    # 延迟初始化
    lazy_attr = MonomerPropertyDescriptor(lazy=True, factory=lambda self: 42)
    
    # 回调函数
    callback_attr = MonomerPropertyDescriptor(callbacks=[lambda self, value: setattr(self, 'callback_triggered', True)])

    # 访问控制属性
    access_control_attr = MonomerPropertyDescriptor(access_control=lambda self: self._can_access, default="accessible")
    
    # 不可变属性
    immutable_attr = MonomerPropertyDescriptor(immutable=True, default="immutable_value")
    
    # 序列化属性
    serialized_attr = MonomerPropertyDescriptor(serialize=True, default="serialized_value")
    
    non_iterable_attr = MonomerPropertyDescriptor(non_iterable=True, default=[])
    
    # 自定义错误消息
    custom_error_attr = MonomerPropertyDescriptor(error_messages={'type': 'Custom type error message.'}, type=int, default=0)

    def __init__(self):
        self._can_access = False
        self.callback_triggered = False

# 测试用例
def test_monomer_property_descriptor():
    test_obj = TestObject()

    # 测试只读属性
    try:
        test_obj.readonly_attr = "new_value"
    except MonomerPropertyError as e:
        print(f"Caught expected error for readonly attribute: {e}")

    # 测试类型检查
    try:
        test_obj.int_attr = "not_an_int"
    except MonomerPropertyError as e:
        print(f"Caught expected error for type check: {e}")

    # 测试验证器
    try:
        test_obj.positive_int_attr = -1
    except MonomerPropertyError as e:
        print(f"Caught expected error for validator: {e}")

    # 测试版本控制
    test_obj.versioned_attr = 1
    test_obj.versioned_attr = 2
    assert len(TestObject.versioned_attr.get_history()) == 2, "Version control history is incorrect"

    # 测试线程安全
    def update_attribute(obj, value):
        obj.thread_safe_attr = value

    thread1 = threading.Thread(target=update_attribute, args=(test_obj, 1))
    thread2 = threading.Thread(target=update_attribute, args=(test_obj, 2))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    assert test_obj.thread_safe_attr == 2, "Thread safety failed"

    # 测试延迟初始化
    assert test_obj.lazy_attr == 42, "Lazy initialization failed"

    # 测试回调函数
    test_obj.callback_attr = 10
    assert test_obj.callback_triggered, "Callback was not triggered"

    # 测试不可迭代属性
    try:
        for value in TestObject.non_iterable_attr:
            pass
    except MonomerPropertyError as e:
        print(f"Caught expected error for non-iterable attribute: {e}")

    # 测试访问控制
    try:
        test_obj.access_control_attr = "new_value"
    except MonomerPropertyError as e:
        print(f"Caught expected error for access control: {e}")
    test_obj._can_access = True

    # 测试不可变属性
    try:
        test_obj.immutable_attr = "first_value"  # 第一次设置应该成功
        test_obj.immutable_attr = "second_value"  # 第二次设置应该失败并抛出异常
    except MonomerPropertyError as e:
        print(f"Caught expected error for immutable attribute: {e}")
    else:
        assert False, "Setting immutable attribute a second time did not raise an error."

    # 测试自定义错误消息
    try:
        test_obj.custom_error_attr = "not_an_int"
    except MonomerPropertyError as e:
        print(f"Caught expected error for custom error message: {e}")

    # 测试序列化和反序列化
    test_obj.serialized_attr = "new_serialized_value"
    serialized_value = test_obj.serialized_attr
    assert isinstance(serialized_value, str), "Serialization failed"
    deserialized_value = TestObject.serialized_attr.deserialize_value(serialized_value, TestObject.serialized_attr.propert_type)
    assert deserialized_value == "new_serialized_value", "Deserialization failed"

    print("All tests passed.")

# 运行测试用例
test_monomer_property_descriptor()