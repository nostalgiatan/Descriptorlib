import json
import logging
import threading
from .utils import _serialize_value, _deserialize_value
from .libException import MonomerPropertyError, SerializationError, DeserializationError
from .base import Descriptor

# 设置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MonomerPropertyDescriptor(Descriptor):
    def __init__(self, default=None, type=None, writable=True, immutable=False, non_iterable=False, read_only=False,
                 error_messages=None, validator=None, depends_on=None, serialize=False, deserialize=False, log_changes=False,
                 access_control=None, version_control=False, thread_safe=False, lazy=False, factory=None, callbacks=None):
        self.default = default
        self.type = type
        self.writable = writable
        self.immutable = immutable
        self.non_iterable = non_iterable
        self.read_only = read_only
        self.error_messages = error_messages or {}
        self.validator = validator
        self.depends_on = depends_on
        self.serialize = serialize
        self.deserialize = deserialize
        self.propert_type = None
        self.log_changes = log_changes
        self.access_control = access_control
        self.version_control = version_control
        self.thread_safe = thread_safe
        self.lazy = lazy
        self.factory = factory
        self.callbacks = callbacks if callbacks is not None else []
        self.private_name = None
        self.history = []
        self.lock = threading.Lock() if thread_safe else None
        if self.version_control and self.default is not None:
            self.history.append(self.default)
        self.deserialize_open = False

    def __set_name__(self, owner, name):
        self.private_name = f"_{name}"

    def __get__(self, instance, owner):
        if instance is None:
            return self
        self.instance = instance
    
        try:
            if self.lazy and not hasattr(instance, self.private_name):
                if self.factory is not None:
                    value = self.factory(instance)
                    if self.deserialize and self.propert_type is not None and self.deserialize_open is False:
                        value = self.deserialize_value(value, self.propert_type)
                        self.deserialize_open = True
                    setattr(instance, self.private_name, value)
                else:
                    raise MonomerPropertyError(
                        error_code='MONOMER_PROPERTY_ERROR',
                        property_name=self.private_name[1:],
                        message=f"Lazy attribute '{self.private_name[1:]}' requires a factory function."
                    )
    
            if self.thread_safe:
                with self.lock:
                    value = getattr(instance, self.private_name, self.default)
            else:
                value = getattr(instance, self.private_name, self.default)
    
            if value is None and self.default is None:
                raise MonomerPropertyError(
                    error_code='ATTRIBUTE_DELETED',
                    property_name=self.private_name[1:],
                    message=f"Attribute '{self.private_name[1:]}' has been deleted and no default value is set."
                )
    
            if self.deserialize and self.propert_type is not None and self.deserialize_open is False:
                value = self.deserialize_value(value, self.propert_type)
                self.deserialize_open = True
    
        except DeserializationError as e:
            raise MonomerPropertyError(
                error_code='ATTRIBUTE_NOT_DESERIALIZABLE',
                property_name=self.private_name[1:],
                message=str(e)
            )
        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}")
            raise MonomerPropertyError(
                error_code='MONOMER_PROPERTY_ERROR',
                property_name=self.private_name[1:],
                message=str(e)
            )
    
        self.deserialize_open = False
        return value

    def __set__(self, instance, value):
        try:
            if self.read_only:
                self._raise_error("read_only")
            if self.immutable and hasattr(instance, self.private_name):
                self._raise_error("immutable")
            if self.type and not isinstance(value, self.type):
                self._raise_error("type", f"Value must be of type {self.type.__name__}.")
            if self.validator and not self.validator(value):
                self._raise_error("validator")
            if self.access_control and not self.access_control(instance):
                self._raise_error("access_control")
            if not self.writable:
                self._raise_error("writable")
            if self.depends_on is not None:
                if not self.depends_on(instance):
                    raise MonomerPropertyError(
                        error_code='DEPENDENCY_FAILED',
                        property_name=self.private_name[1:],
                        message=f"Attribute '{self.private_name[1:]}' cannot be set due to dependency failure."
                    )
        
            # 使用锁来确保线程安全
            if self.thread_safe:
                with self.lock:
                    # 在锁的作用域内，首先添加当前值到历史记录（如果需要）
                    if self.version_control:
                        self.history.append(value)
                    
                    # 然后根据是否需要序列化来处理新值
                    if self.serialize:
                        try:
                            serialized_value, value_type = self.serialize_value(value)
                            setattr(instance, self.private_name, serialized_value)
                            self.propert_type = value_type
                        except SerializationError as e:
                            raise MonomerPropertyError(
                                error_code='ATTRIBUTE_NOT_SERIALIZABLE',
                                property_name=self.private_name[1:],
                                message=str(e)
                            )
                    else:
                        setattr(instance, self.private_name, value)
                    
                    # 记录日志
                    if self.log_changes:
                        logger.info(f"Attribute '{self.private_name[1:]}' set to {value}")
            else:
                # 如果不需要线程安全，则直接操作
                if self.version_control:
                    self.history.append(value)
                
                if self.serialize:
                    try:
                        serialized_value, value_type = self.serialize_value(value)
                        setattr(instance, self.private_name, serialized_value)
                        self.propert_type = value_type
                    except SerializationError as e:
                        raise MonomerPropertyError(
                            error_code='ATTRIBUTE_NOT_SERIALIZABLE',
                            property_name=self.private_name[1:],
                            message=str(e)
                        )
                else:
                    setattr(instance, self.private_name, value)
                
                if self.log_changes:
                    logger.info(f"Attribute '{self.private_name[1:]}' set to {value}")
            
            # 调用回调函数
            for callback in self.callbacks:
                callback(instance, value)
        except MonomerPropertyError as mpe:
            raise mpe
        except Exception as e:
            logger.error(f"Unexpected error setting attribute '{self.private_name[1:]}' with value {value}: {e}")
            raise MonomerPropertyError(
                error_code='MONOMER_PROPERTY_ERROR',
                property_name=self.private_name[1:],
                message=str(e)
            )

    def __delete__(self, instance):
        try:
            if self.immutable:
                self._raise_error("delete_immutable")
            if self.read_only:
                self._raise_error("delete_read_only")
            if hasattr(instance, self.private_name):
                if self.thread_safe:
                    with self.lock:
                        delattr(instance, self.private_name)
                        if self.log_changes:
                            logger.info(f"Attribute '{self.private_name[1:]}' deleted")
                else:
                    delattr(instance, self.private_name)
                    if self.log_changes:
                        logger.info(f"Attribute '{self.private_name[1:]}' deleted")
        except MonomerPropertyError as mpe:
            raise mpe
        except Exception as e:
            logger.error(f"Unexpected error deleting attribute '{self.private_name[1:]}': {e}")
            raise MonomerPropertyError(
                error_code='MONOMER_PROPERTY_ERROR',
                property_name=self.private_name[1:],
                message=str(e)
            )

    def _raise_error(self, error_type, message=None):
        error_code = None
        default_message = f"Attribute '{self.private_name[1:]}' cannot be {error_type}."
        if message is None:
            message = self.error_messages.get(error_type, default_message)
    
        # 根据错误类型设置错误代码
        if error_type == "read_only":
            error_code = 'READ_ONLY'
        elif error_type == "immutable":
            error_code = 'IMMUTABLE'
        elif error_type == "type":
            error_code = 'TYPE_VALIDATION'
        elif error_type == "validator":
            error_code = 'VALIDATOR_FAILED'
        elif error_type == "access_control":
            error_code = 'ACCESS_CONTROL'
        elif error_type == "writable":
            error_code = 'ATTRIBUTE_READONLY_AFTER_INIT'
        elif error_type == "delete_immutable":
            error_code = 'ATTRIBUTE_IMMUTABLE_AFTER_SET'
        elif error_type == "delete_read_only":
            error_code = 'ATTRIBUTE_READONLY_AFTER_SET'
        elif error_type == "non_iterable":
            error_code = 'ATTRIBUTE_NON_ITERABLE'
    
        raise MonomerPropertyError(
            error_code=error_code,
            property_name=self.private_name[1:],
            message=message
        )
    
    def __iter__(self):
        try:
            if self.non_iterable:
                self._raise_error("non_iterable")
            return iter(getattr(self.instance, self.private_name))
        except Exception as e:
            logger.error(f"Error iterating over attribute '{self.private_name[1:]}': {e}")
            raise MonomerPropertyError(
                error_code='MONOMER_PROPERTY_ERROR',
                property_name=self.private_name[1:],
                message=str(e)
            )
    
    def get_history(self):
        try:
            return self.history
        except Exception as e:
            logger.error(f"Error retrieving history for attribute '{self.private_name[1:]}': {e}")
            raise MonomerPropertyError(
                error_code='MONOMER_PROPERTY_ERROR',
                property_name=self.private_name[1:],
                message=str(e)
            )
   
    def clear_history(self):
        try:
            if self.thread_safe:
                with self.lock:
                    self.history = []
            else:
                self.history = []
            return True
        except Exception as e:
            # 记录错误信息
            logger.error(f"Error clearing history for attribute '{self.private_name[1:]}': {e}")
            # 可以选择抛出自定义异常或者返回False表示操作失败
            raise MonomerPropertyError(
                error_code='HISTORY_CLEAR_ERROR',
                property_name=self.private_name[1:],
                message=str(e)
            )
            return False

    def add_callback(self, callback):
        try:
            if not callable(callback):
                raise ValueError("Callback must be callable.")
            self.callbacks.append(callback)
        except Exception as e:
            logger.error(f"Error adding callback to attribute '{self.private_name[1:]}': {e}")
            raise MonomerPropertyError(
                error_code='MONOMER_PROPERTY_ERROR',
                property_name=self.private_name[1:],
                message=str(e)
            )
    
    def serialize_value(self, value):
        try:
            # 序列化逻辑
            serialized_value, value_type = _serialize_value(value)
            return serialized_value, value_type
        except Exception as e:
            raise SerializationError(
                error_code='SERIALIZATION_ERROR',
                message=str(e),
                attribute_name=self.private_name[1:]
            )

    def deserialize_value(self, value_str, value_type):
        try:
            # 反序列化逻辑
            deserialized_value = _deserialize_value(value_str, value_type)
            return deserialized_value
        except Exception as e:
            raise DeserializationError(
                error_code='DESERIALIZATION_ERROR',
                message=str(e),
                attribute_name=self.private_name[1:]
            )
