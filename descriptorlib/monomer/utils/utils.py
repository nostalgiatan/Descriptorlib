import base64
import json
import datetime
import decimal

def _serialize_value(value):
    # 定义类型转换规则
    type_serializers = {
        list: lambda v: json.dumps(v).encode('utf-8'),
        dict: lambda v: json.dumps({k: _serialize_value(v)[0] for k, v in v.items()}).encode('utf-8'),
        tuple: lambda v: json.dumps(list(v)).encode('utf-8'),
        set: lambda v: json.dumps(list(v)).encode('utf-8'),
        frozenset: lambda v: json.dumps(list(v)).encode('utf-8'),
        int: lambda v: str(v).encode('utf-8'),
        float: lambda v: format(v, '.10g').encode('utf-8'),
        bool: lambda v: str(v).encode('utf-8'),
        str: lambda v: v.encode('utf-8'),
        bytes: lambda v: v,
        type(None): lambda v: b'None',
        datetime.date: lambda v: v.isoformat().encode('utf-8'),
        datetime.datetime: lambda v: v.isoformat().encode('utf-8'),
        datetime.time: lambda v: v.isoformat().encode('utf-8'),
        decimal.Decimal: lambda v: str(v).encode('utf-8'),
        complex: lambda v: json.dumps({'real': v.real, 'imag': v.imag}).encode('utf-8'),
    }
    value_type = type(value)
    if value_type in type_serializers:
        value_str = type_serializers[value_type](value)
        encoded_value = base64.b64encode(value_str).decode('utf-8')
        return encoded_value, value_type.__name__
    else:
        raise TypeError(f"Unsupported type: {value_type}")

def _deserialize_value(value_str, value_type):
    # 定义类型反转换规则
    type_deserializers = {
        'list': lambda v: json.loads(v),
        'dict': lambda v: json.loads({k: _deserialize_value(v)[0] for k, v in v.items()}),
        'tuple': lambda v: tuple(json.loads(v)),
        'set': lambda v: set(json.loads(v)),
        'frozenset': lambda v: frozenset(json.loads(v)),
        'int': lambda v: int(v),
        'float': lambda v: float(v),
        'bool': lambda v: v.lower() == 'true',
        'str': lambda v: v.decode('utf-8'),
        'bytes': lambda v: v,
        'NoneType': lambda v: None,
        'date': lambda v: datetime.date.fromisoformat(v.decode('utf-8')),
        'datetime': lambda v: datetime.datetime.fromisoformat(v.decode('utf-8')),
        'time': lambda v: datetime.time.fromisoformat(v.decode('utf-8')),
        'Decimal': lambda v: decimal.Decimal(v.decode('utf-8')),
        'complex': lambda v: complex(**json.loads(v.decode('utf-8'))),
    }
    if value_type in type_deserializers:
        return type_deserializers[value_type](base64.b64decode(value_str))
    else:
        raise TypeError(f"Unsupported type: {value_type}")