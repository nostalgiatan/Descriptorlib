from descriptorlib.monomer import Descriptor
from descriptorlib.monomer.libException import DescriptorLibError

class MyClass:
    attr = Descriptor('attr')

# 示例：使用该类
obj = MyClass()
obj.attr = 10  # 正常设置属性
print(obj.attr)  # 正常获取属性

del obj.attr  # 正常删除属性
# 尝试删除不存在的属性
try:
    del obj.attr
except DescriptorLibError as e:
    print(e)  # 输出错误信息