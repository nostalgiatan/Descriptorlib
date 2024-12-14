from .libError import DescriptorLibError

class SerializationError(DescriptorLibError):
    ERROR_CODES = {
        'SERIALIZATION_ERROR': ('100', 'An error occurred during serialization.')
    }

    def __init__(self, attribute_name = None, message=None, error_code=None):
        if message is None and error_code is not None:
            message = self.ERROR_CODES.get(error_code, ('', 'Unknown serialization error.'))[1]
        super().__init__(message=message, error_code=error_code)
        self.attribute_name = attribute_name

    def __str__(self):
        return f"{self.error_code}: {self.attribute_name} - {super().__str__()}"


class DeserializationError(DescriptorLibError):
    ERROR_CODES = {
        'DESERIALIZATION_ERROR': ('101', 'An error occurred during deserialization.')
    }

    def __init__(self, message=None, error_code=None, attribute_name=None):
        if message is None and error_code is not None:
            message = self.ERROR_CODES.get(error_code, ('', 'Unknown deserialization error.'))[1]
        super().__init__(message=message, error_code=error_code)
        self.attribute_name = attribute_name

    def __str__(self):
        return f"{self.error_code}: {self.attribute_name} - {super().__str__()}"