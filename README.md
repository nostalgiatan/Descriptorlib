# Descriptorlib: Python 属性描述符库
---

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-LGPL-green.svg)](LICENSE)
[![Coverage Status](https://img.shields.io/coveralls/nostalgiatan/Descriptorlib/master.svg?style=flat-square)](https://coveralls.io/r/https://github.com/nostalgiatan/Descriptorlib)
[![PyPI](https://img.shields.io/pypi/v/Descriptorlib.svg?style=flat-square)](https://pypi.org/project/Descriptorlib/)
[![Documentation Status](https://readthedocs.org/projects/descriptorlib/badge/?version=latest&style=flat-square)](https://descriptorlib.readthedocs.io/en/latest/?badge=latest)

`Descriptorlib` 是一个 Python 库，它提供了一系列强大的描述符，用于增强 Python 类的属性功能。通过使用描述符，你可以轻松实现属性的类型检查、只读、延迟初始化、版本控制、线程安全等特性。

## 安装

使用 pip 安装 `Descriptorlib`:

```bash
pip install Descriptorlib
```

## 文档

`Descriptorlib` 提供了详细的文档，包括中文和英文版本。每个描述符都有其对应的文档，方便用户查找和使用。

- [Chinese Documentation](/docs/Chinese/Descriptordocs)
- [English Documentation](/docs/English/Descriptordocs)

### 常见问题与解决方案

在 `Chinese` 和 `English` 目录下都有一个 `FAQ` 目录，收录了常见问题与解决方案。

## 测试

我们为每个描述符提供了单元测试，确保它们的可用性和正确性。测试代码位于 `tests` 目录。

## 示例

`examples` 目录提供了描述符的使用示例，帮助用户快速上手。

## 库结构

- **monomer**: 所有描述符都储存在此目录下。
- **libException**: 包含所有错误信息的目录。
- **utils**:包含公用于所有描述符的工具目录。

## 贡献指南

我们欢迎和鼓励社区成员为 `Descriptorlib` 做出贡献。请参考 [CONTRIBUTING.md](CONTRIBUTING.md) 了解如何贡献代码。

## 许可证

`Descriptorlib` 使用 LGPL 许可证，请查看 [LICENSE](LICENSE) 文件了解更多信息。

---
