class DescriptorLibError(Exception):
    """Descriptorlib装饰符引发的 所有错误的基类。"""
    
    # 定义通用错误代码及其默认错误消息
    ERROR_CODES = {
        'READ_ONLY': ('1001', 'Attempt to modify a read-only attribute.'),
        'IMMUTABLE': ('1002', 'Attempt to modify an immutable attribute.'),
        'TYPE_VALIDATION': ('1003', 'Property type validation failed.'),
        'VALIDATOR_FAILED': ('1004', 'Custom validator failed.'),
        'ACCESS_CONTROL': ('1005', 'Insufficient access control permissions.'),
        'SERIALIZATION': ('1006', 'Error occurred during serialization.'),
        'DESERIALIZATION': ('1007', 'Error occurred during deserialization.'),
        'ATTRIBUTE_NOT_FOUND': ('1008', 'Requested attribute does not exist.'),
        'INVALID_VALUE': ('1009', 'The provided value is invalid.'),
        'CALLBACK_FAILED': ('1010', 'Callback function execution failed.'),
        'ATTRIBUTE_ALREADY_EXISTS': ('1011', 'Attribute already exists.'),  # 属性已存在
        'ATTRIBUTE_REQUIRED': ('1012', 'Required attribute is missing.'),  # 必需的属性缺失
        'ATTRIBUTE_DELETED': ('1013', 'Attribute has been deleted.'),  # 属性已被删除
        'ATTRIBUTE_READONLY_AFTER_INIT': ('1014', 'Attribute is read-only after initialization.'),  # 属性在初始化后变为只读
        'ATTRIBUTE_IMMUTABLE_AFTER_SET': ('1015', 'Attribute is immutable after being set.'),  # 属性在设置后变为不可变
        'ATTRIBUTE_NOT_SERIALIZABLE': ('1016', 'Attribute is not serializable.'),  # 属性不可序列化
        'ATTRIBUTE_NOT_DESERIALIZABLE': ('1017', 'Attribute is not deserializable.'),  # 属性不可反序列化
        'ATTRIBUTE_NON_ITERABLE': ('1018', 'Attribute is not iterable.'),
        'HISTORY_CLEAR_ERROR': ('1019', 'Error occurred while clearing history.'),
        'ATTRIBUTE_READONLY_AFTER_SET': ('1020', 'Attribute is read-only after being set.'),  # 属性在设置后变为只读
        'ATTRIBUTE_SET_ERROR': ('1021', 'Error setting attribute value.'),
        'ATTRIBUTE_ACCESS_ERROR': ('1022', 'Error accessing attribute.'),
    }

    def __init__(self, message=None, error_code=None):
        """
        初始化错误实例。
        
        :param message: 错误消息。如果为None，则使用默认错误消息。
        :param error_code: 错误代码。
        """
        if message is None and error_code is not None:
            message = self.ERROR_CODES.get(error_code, ('', 'Unknown error.'))[1]
        super().__init__(message)
        self.error_code = error_code

    def __str__(self):
        """
        返回错误实例的字符串表示，包括错误代码和消息。
        """
        return f"{self.error_code}: {super().__str__()}"
