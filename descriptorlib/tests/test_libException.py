import pytest
import threading
from descriptorlib.monomer import MonomerPropertyError,Descriptor,  DeserializationError, SerializationError, DescriptorLibError

class TestbaseDescriptor:
    class MyClass:
        attr = Descriptor('attr')
    
    def test_descriptor_get(self):
        obj = self.MyClass()
        obj.__dict__['attr'] = 10
        assert obj.attr == 10
    
    def test_descriptor_get_none(self):
        obj = self.MyClass()
        assert obj.attr is None
    
    def test_descriptor_set(self):
        obj = self.MyClass()
        obj.attr = 20
        assert obj.__dict__['attr'] == 20
    
    def test_descriptor_delete(self):
        obj = self.MyClass()
        obj.__dict__['attr'] = 30
        del obj.attr
        assert 'attr' not in obj.__dict__
    
    def test_descriptor_get_instance_none(self):
        class TestClass:
            test_attr = Descriptor('test_attr')
        assert TestClass.test_attr == TestClass.test_attr  # 测试 instance 为 None 的情况
    
    def test_descriptor_delete_error(self):
        obj = self.MyClass()
        with pytest.raises(DescriptorLibError) as exc_info:
            del obj.attr
        assert 'ATTRIBUTE_DELETE' in str(exc_info.value)
    
    def test_descriptor_delete_not_found(self):
        class TestClass:
            test_attr = Descriptor('test_attr')
        instance = TestClass()
        TestClass.test_attr.__dict__['test_attr'] = 10  # 确保属性存在
        # 模拟删除属性时发生的异常
        TestClass.test_attr.__dict__ = {}
        with pytest.raises(DescriptorLibError) as exc_info:
            del instance.test_attr
        assert 'ATTRIBUTE_NOT_FOUND' in str(exc_info.value)
    
    def test_get_attribute_access_error(self):
        class TestClass:
            test_attr = Descriptor('test_attr')
        
        instance = TestClass()
        TestClass.test_attr.__dict__ = {}
        with pytest.raises(DescriptorLibError) as exc_info:
            getattr(instance, 'test_attr')
        assert exc_info.value.error_code == 'ATTRIBUTE_ACCESS_ERROR'
    
    def test_set_attribute_set_error(self):
        class TestClass:
            test_attr = Descriptor('test_attr')
        
        instance = TestClass()
        TestClass.test_attr.__dict__ = {}
        with pytest.raises(DescriptorLibError) as exc_info:
            instance.test_attr = 'new_value'
        assert exc_info.value.error_code == 'ATTRIBUTE_SET_ERROR'

def test_error_codes():
    # 遍历所有错误代码，确保每个都能正确地设置错误消息
    for error_code, (code, default_message) in DescriptorLibError.ERROR_CODES.items():
        with pytest.raises(DescriptorLibError) as exc_info:
            raise MonomerPropertyError(error_code=error_code)
        assert exc_info.value.error_code == error_code
        assert str(exc_info.value) == f"{error_code}: {default_message}"

    # 测试未知错误代码
    with pytest.raises(DescriptorLibError) as exc_info:
        raise MonomerPropertyError(error_code='UNKNOWN_CODE')
    assert exc_info.value.error_code == 'UNKNOWN_CODE'
    assert "Unknown error." in str(exc_info.value)

def test_error_codes():
    # 遍历所有错误代码，确保每个都能正确地设置错误消息
    for error_code, (code, default_message) in DescriptorLibError.ERROR_CODES.items():
        with pytest.raises(DescriptorLibError) as exc_info:
            raise DeserializationError(error_code=error_code)
        assert exc_info.value.error_code == error_code
        assert str(exc_info.value) == f"{error_code}: {default_message}"

    # 测试未知错误代码
    with pytest.raises(DescriptorLibError) as exc_info:
        raise DeserializationError(error_code='UNKNOWN_CODE')
    assert exc_info.value.error_code == 'UNKNOWN_CODE'
    assert "Unknown error." in str(exc_info.value)

def test_error_codes():
    # 遍历所有错误代码，确保每个都能正确地设置错误消息
    for error_code, (code, default_message) in DescriptorLibError.ERROR_CODES.items():
        with pytest.raises(DescriptorLibError) as exc_info:
            raise SerializationError(error_code=error_code)
        assert exc_info.value.error_code == error_code
        assert str(exc_info.value) == f"{error_code}: {default_message}"

    # 测试未知错误代码
    with pytest.raises(DescriptorLibError) as exc_info:
        raise SerializationError(error_code='UNKNOWN_CODE')
    assert exc_info.value.error_code == 'UNKNOWN_CODE'
    assert "Unknown error." in str(exc_info.value)

def test_error_codes():
    # 遍历所有错误代码，确保每个都能正确地设置错误消息
    for error_code, (code, default_message) in DescriptorLibError.ERROR_CODES.items():
        with pytest.raises(DescriptorLibError) as exc_info:
            raise DescriptorLibError(error_code=error_code)
        assert exc_info.value.error_code == error_code
        assert str(exc_info.value) == f"{error_code}: {default_message}"

    # 测试未知错误代码
    with pytest.raises(DescriptorLibError) as exc_info:
        raise DescriptorLibError(error_code='UNKNOWN_CODE')
    assert exc_info.value.error_code == 'UNKNOWN_CODE'
    assert "Unknown error." in str(exc_info.value)
