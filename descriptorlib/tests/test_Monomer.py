import pytest
from descriptorlib.monomer import MonomerPropertyDescriptor
import threading
from unittest.mock import patch
from descriptorlib.monomer.libException import MonomerPropertyError, DeserializationError, SerializationError

class TestMonomerPropertyDescriptor:
    class SampleClass:
        prop = MonomerPropertyDescriptor(default=0)

    def test_default_value(self):
        obj = self.SampleClass()
        assert obj.prop == 0

    def test_set_value(self):
        obj = self.SampleClass()
        obj.prop = 10
        assert obj.prop == 10

    def test_immutable_attribute(self):
        class ImmutableSampleClass:
            prop = MonomerPropertyDescriptor(default=0, immutable=True)

        obj = ImmutableSampleClass()
        with pytest.raises(MonomerPropertyError) as exc_info:
            obj.prop = 10
            obj.prop = 12
        assert 'IMMUTABLE' in str(exc_info.value)

    def test_read_only_attribute(self):
        class ReadOnlySampleClass:
            prop = MonomerPropertyDescriptor(default=0, read_only=True)

        obj = ReadOnlySampleClass()
        with pytest.raises(MonomerPropertyError) as exc_info:
            obj.prop = 10
        assert 'READ_ONLY' in str(exc_info.value)
    
    def test_unexpected_error_during_deletion(self):
        class TestClass:
            prop = MonomerPropertyDescriptor()
    
        obj = TestClass()
        obj.prop = 1
        with pytest.raises(MonomerPropertyError) as exc_info:
            with patch('builtins.delattr', side_effect=RuntimeError("Something went wrong during deletion")):
                del obj.prop
        assert "MONOMER_PROPERTY_ERROR" in str(exc_info.value)
        assert "Something went wrong during deletion" in str(exc_info.value)
    
    def test_delete_immutable_failure(self):
        class TestClass:
            prop = MonomerPropertyDescriptor(immutable=True)  # 或者 read_only=True
    
        obj = TestClass()
        with pytest.raises(MonomerPropertyError) as exc_info:
            del obj.prop
        assert "ATTRIBUTE_IMMUTABLE_AFTER_SET" in str(exc_info.value)

    def test_delete_read_only_failure(self):
        class TestClass:
            prop = MonomerPropertyDescriptor(read_only=True)
    
        obj = TestClass()
        with pytest.raises(MonomerPropertyError) as exc_info:
            del obj.prop
        assert "ATTRIBUTE_READONLY_AFTER_SET" in str(exc_info.value)

    def test_type_validation(self):
        class TypeSampleClass:
            prop = MonomerPropertyDescriptor(default=0, type=int)

        obj = TypeSampleClass()
        with pytest.raises(MonomerPropertyError) as exc_info:
            obj.prop = "not an int"
        assert 'TYPE_VALIDATION' in str(exc_info.value)
    
    def test_depends_on(self):
        class DependsOnSampleClass:
            prop1 = MonomerPropertyDescriptor(default=0)
            prop2 = MonomerPropertyDescriptor(default=0, depends_on=lambda instance: instance.prop1)
    
    def test_access_control(self):
        class AccessControlSampleClass:
            prop = MonomerPropertyDescriptor(default=0, access_control=lambda instance: False)

        obj = AccessControlSampleClass()
        with pytest.raises(MonomerPropertyError) as exc_info:
            obj.prop = 10
        assert 'ACCESS_CONTROL' in str(exc_info.value)

    def test_validator_function(self):
        def is_positive(value):
            return value > 0

        class ValidatorSampleClass:
            prop = MonomerPropertyDescriptor(default=1, validator=is_positive)

        obj = ValidatorSampleClass()
        with pytest.raises(MonomerPropertyError) as exc_info:
            obj.prop = -1
        assert 'VALIDATOR_FAILED' in str(exc_info.value)

    def test_history_tracking(self):
        class HistorySampleClass:
            prop = MonomerPropertyDescriptor(default=0, version_control=True)

        obj = HistorySampleClass()
        obj.prop = 1
        obj.prop = 2
        assert obj.prop == 2
        assert HistorySampleClass.prop.get_history() == [0, 1, 2]
    
    def test_clear_history(self):
        class HistorySampleClass:
            prop = MonomerPropertyDescriptor(default=0, version_control=True)

        obj = HistorySampleClass()
        obj.prop = 1
        obj.prop = 2
        HistorySampleClass.prop.clear_history()
        assert HistorySampleClass.prop.get_history() == []

    def test_thread_safety(self):
        class ThreadSafeSampleClass:
            prop = MonomerPropertyDescriptor(default=0, thread_safe=True)

        obj = ThreadSafeSampleClass()
        def set_value_in_thread(value):
            obj.prop = value

        # 创建线程并设置属性值
        threads = [threading.Thread(target=set_value_in_thread, args=(i,)) for i in range(10)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        # 确保属性值是最后一个线程设置的值
        assert obj.prop == 9

    def test_lazy_attribute(self):
        class LazySampleClass:
            def factory_method(self):
                return 42

            prop = MonomerPropertyDescriptor(default=None, lazy=True, factory=factory_method)

        obj = LazySampleClass()
        assert obj.prop == 42

    def test_callbacks(self):
        callback_values = []

        def callback(instance, value):
            callback_values.append(value)

        class CallbackSampleClass:
            prop = MonomerPropertyDescriptor(default=0, callbacks=[callback])

        obj = CallbackSampleClass()
        obj.prop = 10
        assert callback_values == [10]

    def test_delete_attribute(self):
        class DeleteSampleClass:
            prop = MonomerPropertyDescriptor()

        obj = DeleteSampleClass()
        obj.prop = 1
        del obj.prop
        with pytest.raises(MonomerPropertyError):
            _ = obj.prop
    
    def test_error_messages(self):
        class ErrorMessageSampleClass:
            prop = MonomerPropertyDescriptor(type=int, error_messages={
                "type": "Value must be of type int."
            })

        obj = ErrorMessageSampleClass()
        with pytest.raises(MonomerPropertyError) as exc_info:
            obj.prop = "not an int"
        assert 'TYPE_VALIDATION' in str(exc_info.value)
        assert "Value must be of type int." in str(exc_info.value)
    
    def test_serialization(self):
        class SerializationSampleClass:
            prop = MonomerPropertyDescriptor(default=0, serialize=True)

        obj = SerializationSampleClass()
        serialized_value, value_type = SerializationSampleClass.prop.serialize_value(10)
        obj.prop = 10
        assert obj.prop == serialized_value
    
    def test_deserialization(self):
        class SerializationExceptionSampleClass:
            prop = MonomerPropertyDescriptor(default=0, deserialize=True)
    
        obj = SerializationExceptionSampleClass()
        serialization_value, value_type = SerializationExceptionSampleClass.prop.serialize_value(10)
        obj.prop = serialization_value
        SerializationExceptionSampleClass.prop.propert_type = value_type
        assert obj.prop == 10
    
    # 回调函数异常处理
    def test_callback_exception(self):
        callback_values = []
    
        def callback(instance, value):
            callback_values.append(value)
            raise ValueError("Callback error")
    
        class CallbackExceptionSampleClass:
            prop = MonomerPropertyDescriptor(default=0, callbacks=[callback])
    
        obj = CallbackExceptionSampleClass()
        with pytest.raises(MonomerPropertyError) as exc_info:
            obj.prop = 10
        assert 'MONOMER_PROPERTY_ERROR' in str(exc_info.value)
        assert "Callback error" in str(exc_info.value)

    # 历史记录更新
    def test_history_update(self):
        class HistoryUpdateSampleClass:
            prop = MonomerPropertyDescriptor(default=0, version_control=True)
    
        obj = HistoryUpdateSampleClass()
        obj.prop = 1
        obj.prop = 2
        obj.prop = 3
        assert obj.prop == 3
        assert HistoryUpdateSampleClass.prop.get_history() == [0, 1, 2, 3]
    
    # 非可迭代属性访问
    def test_non_iterable_attribute_access(self):
        class NonIterableSampleClass:
            prop = MonomerPropertyDescriptor(default=0, non_iterable=True)
    
        obj = NonIterableSampleClass()
        with pytest.raises(MonomerPropertyError) as exc_info:
            list(NonIterableSampleClass.prop)
        assert 'ATTRIBUTE_NON_ITERABLE' in str(exc_info.value)
    
    # 属性依赖
    def test_depends_on_logic(self):
        class DependsOnLogicSampleClass:
            prop1 = MonomerPropertyDescriptor(default=0, version_control=True)
            prop2 = MonomerPropertyDescriptor(default=0, depends_on=lambda instance: instance.prop1 > 0)
    
        obj = DependsOnLogicSampleClass()
        
        # 尝试设置 prop2，应该失败，因为 prop1 的值不满足依赖条件
        with pytest.raises(MonomerPropertyError) as exc_info:
            obj.prop2 = 5
        assert 'DEPENDENCY_FAILED' in str(exc_info.value)
    
        # 设置 prop1 的值以满足依赖条件
        obj.prop1 = 1
    
        # 再次尝试设置 prop2，这次应该成功
        obj.prop2 = 5
        assert obj.prop2 == 5
    
        # 更新 prop1 的值以不满足依赖条件
        obj.prop1 = -1
    
        # 尝试更新 prop2，应该失败，因为 prop1 的值不再满足依赖条件
        with pytest.raises(MonomerPropertyError) as exc_info:
            obj.prop2 = -1
        assert 'DEPENDENCY_FAILED' in str(exc_info.value)
    
    # 工厂方法异常
    def test_factory_method_exception(self):
        class FactoryExceptionSampleClass:
            def faulty_factory_method(self):
                raise ValueError("Factory error")
    
            prop = MonomerPropertyDescriptor(default=None, lazy=True, factory=faulty_factory_method)
    
        obj = FactoryExceptionSampleClass()
        with pytest.raises(MonomerPropertyError) as exc_info:
            _ = obj.prop
        assert 'MONOMER_PROPERTY_ERROR' in str(exc_info.value)
        assert "Factory error" in str(exc_info.value)
   
    def test_deserialization_exception(self):
        class DeserializationExceptionSampleClass:
            prop = MonomerPropertyDescriptor(default=0, serialize=True, deserialize=True)
    
        obj = DeserializationExceptionSampleClass()
        serialized_value, value_type = DeserializationExceptionSampleClass.prop.serialize_value(10)
        with pytest.raises(DeserializationError) as exc_info:
            DeserializationExceptionSampleClass.prop.deserialize_value(b"not a serialized value", value_type)
        assert "DESERIALIZATION_ERROR" in str(exc_info.value)
        with pytest.raises(DeserializationError) as exc_info:
            DeserializationExceptionSampleClass.prop.deserialize_value(b"not a serialized value", '123')
        assert "DESERIALIZATION_ERROR" in str(exc_info.value)
    
    def test_serialization_exception(self):
        class DeserializationExceptionSampleClass:
            prop = MonomerPropertyDescriptor(default=0, serialize=True, deserialize=True)
    
        # 创建一个没有序列化规则的自定义对象
        class CustomObject:
            pass
    
        custom_obj = CustomObject()
    
        # 尝试序列化自定义对象，期望抛出 SerializationError
        with pytest.raises(SerializationError) as exc_info:
            serialized_value, value_type = DeserializationExceptionSampleClass.prop.serialize_value(custom_obj)
        
        assert "SERIALIZATION_ERROR" in str(exc_info.value)

    def test_thread_safe_attribute_access(self):
        class ThreadSafeAccessSampleClass:
            prop = MonomerPropertyDescriptor(default=0, thread_safe=True)
    
        obj = ThreadSafeAccessSampleClass()
    
        def modify_attribute():
            obj.prop = 1
    
        # 创建多个线程尝试修改属性
        threads = [threading.Thread(target=modify_attribute) for _ in range(10)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
    
        # 确保属性值是最后一个线程设置的值
        assert obj.prop == 1

    def test_serialization_and_deserialization_combination(self):
        class SerializationCombinationSampleClass:
            prop = MonomerPropertyDescriptor(default=0, serialize=True, deserialize=True)
    
        obj = SerializationCombinationSampleClass()
        serialized_value, value_type = SerializationCombinationSampleClass.prop.serialize_value(10)
        obj.prop = serialized_value
        assert SerializationCombinationSampleClass.prop.deserialize_value(obj.prop, value_type) == 10
    
    def test_callbacks_on_initialization(self):
        callback_values = []
    
        def callback(instance, value):
            callback_values.append(value)
    
        class CallbackOnInitSampleClass:
            prop = MonomerPropertyDescriptor(default=0, callbacks=[callback])
    
        obj = CallbackOnInitSampleClass()
        assert callback_values == []
    
    def test_concurrent_read_write_thread_safety(self):
        class ThreadSafeReadWriteSampleClass:
            prop = MonomerPropertyDescriptor(default=0, thread_safe=True)
    
        obj = ThreadSafeReadWriteSampleClass()
    
        def read_attribute():
            return obj.prop
    
        def write_attribute(value):
            obj.prop = value
    
        # 创建读写线程
        read_threads = [threading.Thread(target=read_attribute) for _ in range(5)]
        write_threads = [threading.Thread(target=write_attribute, args=(i,)) for i in range(5)]
    
        # 启动线程
        for thread in read_threads + write_threads:
            thread.start()
    
        # 等待线程完成
        for thread in read_threads + write_threads:
            thread.join()
    
        # 确保属性值是最后一个线程设置的值
        assert obj.prop == 4

    def test_depends_on_normal_behavior(self):
        class DependsOnNormalSampleClass:
            prop1 = MonomerPropertyDescriptor(default=0)
            prop2 = MonomerPropertyDescriptor(default=0, depends_on=lambda instance: instance.prop1 > 0)
    
        obj = DependsOnNormalSampleClass()
    
        # 尝试设置 prop2，应该失败，因为 prop1 的值不满足依赖条件
        with pytest.raises(MonomerPropertyError) as exc_info:
            obj.prop2 = 5
        assert 'DEPENDENCY_FAILED' in str(exc_info.value)
    
        # 设置 prop1 的值以满足依赖条件
        obj.prop1 = 5
    
        # 现在设置 prop2 应该成功，因为 prop1 的值满足依赖条件
        obj.prop2 = 5
        assert obj.prop2 == 5
    
        obj.prop1 = 3
        # 尝试设置 prop2，应该成功，因为 prop1 的值仍然满足依赖条件
        obj.prop2 = 3
        assert obj.prop2 == 3
    
        # 更改 prop1 的值，使其不满足依赖条件
        obj.prop1 = 0
        # 尝试设置 prop2，应该失败，因为 prop1 的值不再满足依赖条件
        with pytest.raises(MonomerPropertyError) as exc_info:
            obj.prop2 = -1
        assert 'DEPENDENCY_FAILED' in str(exc_info.value)

    def test_non_iterable_attribute_normal_behavior(self):
        class NonIterableNormalSampleClass:
            prop = MonomerPropertyDescriptor(default=0, non_iterable=True)

        obj = NonIterableNormalSampleClass()
        assert obj.prop == 0

    def test_factory_method_normal_behavior(self):
        class FactoryNormalSampleClass:
            def factory_method(self):
                return 42

            prop = MonomerPropertyDescriptor(default=None, lazy=True, factory=factory_method)

        obj = FactoryNormalSampleClass()
        assert obj.prop == 42

    def test_complex_thread_safety(self):
        class ComplexThreadSafeSampleClass:
            prop = MonomerPropertyDescriptor(default=0, thread_safe=True)

        obj = ComplexThreadSafeSampleClass()
        read_results = []

        def read_attribute():
            read_results.append(obj.prop)

        def write_attribute(value):
            obj.prop = value

        # 创建读写线程
        read_threads = [threading.Thread(target=read_attribute) for _ in range(10)]
        write_threads = [threading.Thread(target=write_attribute, args=(i,)) for i in range(1, 11)]

        # 启动线程
        for thread in read_threads + write_threads:
            thread.start()

        # 等待线程完成
        for thread in read_threads + write_threads:
            thread.join()

        # 确保最终属性值是最后一个线程设置的值
        assert obj.prop == 10
        # 确保在读写过程中读取的值是有效的
        assert all(0 <= value <= 10 for value in read_results)

    def test_serialization_boundary_conditions(self):
        class SerializationBoundarySampleClass:
            prop = MonomerPropertyDescriptor(default=0, serialize=True, deserialize=True)

        obj = SerializationBoundarySampleClass()
        # 测试非常大的数值
        large_value = 10**18
        obj.prop = large_value
        assert obj.prop == large_value

        # 测试特殊字符
        special_value = " spéci@l çhäracter$ "
        obj.prop = special_value
        assert obj.prop == special_value

    def test_callback_function_behavior(self):
        callback_values = []

        def callback(instance, value):
            callback_values.append(value)

        class CallbackBehaviorSampleClass:
            prop = MonomerPropertyDescriptor(default=0, callbacks=[callback])

        obj = CallbackBehaviorSampleClass()
        obj.prop = 10
        obj.prop = 20
        assert callback_values == [10, 20]

# 如果你需要在测试之前或之后进行设置和清理，可以使用pytest的fixture功能
@pytest.fixture
def setup_fixture():
    # setup code
    yield
    # teardown code
