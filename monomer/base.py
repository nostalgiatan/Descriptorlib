from .libException import DescriptorLibError

class Descriptor:
    def __init__(self, name=None):
        self.name = name

    def __get__(self, instance, owner):
        try:
            if instance is None:
                return self
            return instance.__dict__.get(self.name, None)
        except Exception as e:
            raise DescriptorLibError('Error accessing attribute.', 'ATTRIBUTE_ACCESS_ERROR') from e

    def __set__(self, instance, value):
        try:
            instance.__dict__[self.name] = value
        except Exception as e:
            raise DescriptorLibError('Error setting attribute value.', 'ATTRIBUTE_SET_ERROR') from e

    def __delete__(self, instance):
        try:
            if self.name in instance.__dict__:
                pass
        except Exception as e:
            raise DescriptorLibError('Attribute not found.', 'ATTRIBUTE_NOT_FOUND')
        try:
            del instance.__dict__[self.name]
        except Exception as e:
            raise DescriptorLibError('Error deleting attribute.', 'ATTRIBUTE_DELETE') from e