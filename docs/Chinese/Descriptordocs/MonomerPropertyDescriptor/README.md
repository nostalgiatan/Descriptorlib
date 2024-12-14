# MonomerPropertyDescriptor
---

MonomerPropertyDescriptor 是 Descriptorlib 库中的一个关键组件，位于 `Descriptorlib.monomer` 模块。它是一个强大的属性描述符，旨在为 Python 类的属性提供额外的功能，而无需修改原始类代码。MonomerPropertyDescriptor 通过丰富的错误处理能力，确保了属性操作的安全性和一致性。

## 特性

MonomerPropertyDescriptor 提供了一系列特性，以增强属性的行为：

- **只读属性**: 防止属性被修改。
- **类型检查**: 确保属性值符合指定的数据类型。
- **自定义验证器**: 允许定义自定义函数来验证属性值。
- **版本控制**: 跟踪属性值的历史变化。
- **线程安全**: 在多线程环境中安全地操作属性。
- **延迟初始化**: 属性在首次访问时才进行初始化。
- **访问控制**: 根据特定条件控制属性的读写权限。
- **序列化和反序列化**: 允许属性值在存储和检索时进行序列化和反序列化。
- **日志记录**: 记录属性值的修改。
- **回调函数**: 在属性值修改时执行自定义函数。
- **不可变属性**: 一旦属性被设置，其值不能被更改。
- **不可迭代属性**: 防止属性被迭代，适用于不希望属性成为可迭代对象的场景。
- **错误消息自定义**: 允许为不同的错误情况定义自定义的错误消息。

## 安装

MonomerPropertyDescriptor 作为 Descriptorlib 库的一部分，可以通过 pip 安装：

```bash
pip install Descriptorlib
```

## 使用方法

要使用 MonomerPropertyDescriptor，首先需要导入它：

```python
from Descriptorlib.monomer import MonomerPropertyDescriptor
```

然后，在您的类中定义属性时，使用 MonomerPropertyDescriptor 作为装饰器：

```python
class MyClass:
    my_attribute = MonomerPropertyDescriptor(type=int, default=0, read_only=True)
```

在上面的例子中，`my_attribute` 将被创建为一个只读的整数属性，默认值为 0。

## 示例

以下是一个使用 MonomerPropertyDescriptor 的完整示例：

```python
class TestObject:
    int_attr = MonomerPropertyDescriptor(type=int, default=0)
    str_attr = MonomerPropertyDescriptor(type=str, default="default")

test_obj = TestObject()
print(test_obj.int_attr)  # 输出: 0
print(test_obj.str_attr)  # 输出: "default"
```

## 错误处理

MonomerPropertyDescriptor 提供了丰富的错误处理能力，可以捕获并抛出以下异常：

- `MonomerPropertyError`: 基本的属性错误。
- `SerializationError`: 序列化属性值时发生的错误。
- `DeserializationError`: 反序列化属性值时发生的错误。

这些异常都包含了详细的错误信息和错误代码，便于调试和日志记录。

## 贡献指南

我们欢迎和鼓励社区成员为 `Descriptorlib` 做出贡献。以下是一些贡献的步骤：

- **发现问题**：如果您在使用过程中发现了问题，请通过 GitHub 仓库的 [issue tracker](完整的链接) 提交一个 issue。
- **提出改进**：如果您有改进的建议或新的特性想法，请创建一个 issue 与我们讨论。
- **提交代码**：如果您想要提交代码，请遵循以下步骤：
  1. Fork 仓库。
  2. 创建您的特性分支 (`git checkout -b my-new-feature`).
  3. 提交您的更改 (`git commit -am 'Add some feature'`).
  4. 将您的分支推送到 GitHub (`git push origin my-new-feature`).
  5. 通过 GitHub 发起 Pull Request。

在提交代码之前，请确保您的代码符合 PEP 8 编码标准，并且通过了所有的单元测试。

---