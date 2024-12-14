class Descriptor:
    def __init__(self, name=None):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name, None)

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        if self.name in instance.__dict__:
            del instance.__dict__[self.name]