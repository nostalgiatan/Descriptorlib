# MonomerPropertyDescriptor

---

MonomerPropertyDescriptor is a key component of the Descriptorlib library, located in the `Descriptorlib.monomer` module. It is a powerful property descriptor designed to provide additional functionality for attributes of Python classes without modifying the original class code. MonomerPropertyDescriptor ensures the safety and consistency of attribute operations through its robust error handling capabilities.

## Features

MonomerPropertyDescriptor offers a range of features to enhance the behavior of attributes:

- **Read-only attribute**: Prevents the attribute from being modified.
- **Type checking**: Ensures that the attribute value conforms to the specified data type.
- **Custom validator**: Allows the definition of custom functions to validate attribute values.
- **Version control**: Tracks the historical changes of attribute values.
- **Thread safety**: Safely operates attributes in a multi-threaded environment.
- **Lazy initialization**: Initializes the attribute only when it is first accessed.
- **Access control**: Controls read and write permissions for attributes based on specific conditions.
- **Serialization and deserialization**: Allows attribute values to be serialized and deserialized when stored and retrieved.
- **Logging**: Records modifications to attribute values.
- **Callback function**: Executes a custom function when an attribute value is modified.
- **Immutable attribute**: Once an attribute is set, its value cannot be changed.
- **Non-iterable attribute**: Prevents the attribute from being iterated over, suitable for scenarios where the attribute should not be an iterable object.
- **Custom error messages**: Allows custom error messages to be defined for different error conditions.

## Installation

MonomerPropertyDescriptor, as part of the Descriptorlib library, can be installed via pip:

```bash
pip install Descriptorlib
```

## Usage

To use MonomerPropertyDescriptor, you first need to import it:

```python
from Descriptorlib.monomer import MonomerPropertyDescriptor
```

Then, when defining attributes in your class, use MonomerPropertyDescriptor as a decorator:

```python
class MyClass:
    my_attribute = MonomerPropertyDescriptor(type=int, default=0, read_only=True)
```

In the example above, `my_attribute` will be created as a read-only integer attribute with a default value of 0.

## Example

Here is a complete example using MonomerPropertyDescriptor:

```python
class TestObject:
    int_attr = MonomerPropertyDescriptor(type=int, default=0)
    str_attr = MonomerPropertyDescriptor(type=str, default="default")

test_obj = TestObject()
print(test_obj.int_attr)  # Output: 0
print(test_obj.str_attr)  # Output: "default"
```

## Error Handling

MonomerPropertyDescriptor provides comprehensive error handling capabilities and can catch and throw the following exceptions:

- `MonomerPropertyError`: Basic attribute errors.
- `SerializationError`: Errors that occur during the serialization of attribute values.
- `DeserializationError`: Errors that occur during the deserialization of attribute values.

These exceptions include detailed error information and error codes, facilitating debugging and logging.

## Contribution Guidelines

We welcome and encourage community members to contribute to `Descriptorlib`. Here are some steps for contributing:

- **Reporting Issues**: If you encounter any issues while using the library, please submit an issue through the GitHub repository's [issue tracker](complete link).
- **Suggesting Improvements**: If you have suggestions for improvements or new feature ideas, please create an issue to discuss with us.
- **Submitting Code**: If you wish to submit code, please follow these steps:
  1. Fork the repository.
  2. Create your feature branch (`git checkout -b my-new-feature`).
  3. Commit your changes (`git commit -am 'Add some feature'`).
  4. Push your branch to GitHub (`git push origin my-new-feature`).
  5. Open a Pull Request through GitHub.

Before submitting code, please ensure that your code adheres to the PEP 8 coding standards and that all unit tests pass.

---