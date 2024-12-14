from .libError import DescriptorLibError

class MonomerPropertyError(DescriptorLibError):
    ERROR_CODES = {
        'MONOMER_PROPERTY_ERROR': ('1100', 'An error occurred with the MonomerPropertyDescriptor.')
    }

    def __init__(self, message=None, error_code=None, property_name=None):
        if message is None and error_code is not None:
            message = self.ERROR_CODES.get(error_code, ('', 'Unknown error.'))[1]
        super().__init__(message=message, error_code=error_code)
        self.property_name = property_name

    def __str__(self):
        return f"{self.error_code}: {self.property_name} - {super().__str__()}"