from collections import OrderedDict
from datetime import datetime

ORDER_DEFAULT = 1000000


class Undefined:
    """
    Type for api-field if field does not exist in json.
    This field is not None, exactly does not exist.
    """
    pass


UNDEF = Undefined()


class BaseField:
    pass


class Field(BaseField):
    def __init__(self, validators=None, required=False, nullable=True,
                 default=UNDEF, order=ORDER_DEFAULT):
        self.value = UNDEF
        if validators is not None and not isinstance(validators, list):
            raise TypeError('validators is not iterable')
        self.validators = validators if validators else []
        self.required = required
        self.nullable = nullable
        self.default = default
        self.order = order

    def __get__(self, obj, cls):
        return self.value

    def __set__(self, obj, value):
        print('setter')
        print(type(obj))
        print(obj)
        print('/setter')
        self.value = value
        if self.value == UNDEF and self.default != UNDEF:
            self.value = self.default()\
                if callable(self.default) else self.default
        self.value = self.format()
        self._validate_first()

    def format(self):
        return self.value

    def _validate_first(self):
        if self.required and self.value == UNDEF:
            raise ValueError('Field is required')
        if not self.nullable and self.value is None:
            raise ValueError('Expected not None')
        if self.value == UNDEF:
            self.value = None
        if self.value is not None:
            for validator in self.validators:
                validator(self.value)
            self.validate()

    def validate(self):
        """В классе-потомке провалидировать"""
        pass


class Int(Field):
    def format(self):
        try:
            return int(float(self.value))
        except (ValueError, TypeError):
            return self.value

    def validate(self):
        super(Int, self).validate()
        if not isinstance(self.value, int):
            raise ValueError('Expected int')


class Float(Field):
    def format(self):
        try:
            return float(self.value)
        except (ValueError, TypeError):
            return self.value

    def validate(self):
        super(Float, self).validate()
        if not isinstance(self.value, float):
            raise ValueError('Expected float')


class Str(Field):
    def format(self):
        try:
            return str(self.value)
        except Exception:
            raise TypeError('Expected str')


class Dict(Field):
    def validate(self):
        if not isinstance(self.value, dict):
            raise TypeError('Expected dict (json)')


class Email(Str):
    def validate(self):
        super(Email, self).validate()
        if '@' not in self.value:
            raise ValueError('Expected email')


class Date(Str):
    def format(self):
        self.value = super(Date, self).format()
        try:
            return datetime.strptime(self.value, '%Y-%m-%d')
        except Exception:
            raise TypeError('Expected date %Y-%m-%d')


class List(Field):
    def validate(self):
        if not isinstance(self.value, list):
            raise ValueError('Expected list')


class MetaObjField(type):
    def __new__(self, name, bases, namespace):
        cls = super(MetaObjField, self).__new__(self, name, bases, namespace)
        # cls._fields = [key for key, val in namespace.items()
        #                if isinstance(val, BaseField)]
        cls._fields = {key: val.order for key, val in namespace.items()
                       if isinstance(val, BaseField)}
        cls._fields = OrderedDict(
            sorted(cls._fields.items(), key=lambda item: item[0]))
        return cls


class Obj(BaseField, metaclass=MetaObjField):

    def __init__(self, validators=None, required=False, nullable=True,
                 default=UNDEF, order=ORDER_DEFAULT, fields=None):
        print('class objfield init')
        self.value = UNDEF
        if validators is not None and not isinstance(validators, list):
            raise TypeError('validators is not iterable')
        self.validators = validators if validators else []
        self.required = required
        self.nullable = nullable
        self.default = default
        self.order = order

        if isinstance(fields, dict):
            for key, val in fields.items():
                setattr(type(self), key, val)
                if isinstance(val, BaseField):
                    # self._fields.append(key)
                    self._fields.update({key: val.order})
            self._fields = OrderedDict(
                sorted(self._fields.items(), key=lambda item: item[0]))

    def __set__(self, obj, value):
        self.value = value
        if self.value == UNDEF and self.default != UNDEF:
            self.value = self.default()\
                if callable(self.default) else self.default
        self.value = self.format()

        print('O F {}'.format(self._fields))
        obj_value = {} if self.value == UNDEF else self.value
        for key in self._fields:
            try:
                print('OBJF - {} : {}'.format(key, obj_value.get(key, UNDEF)))
                setattr(self, key, obj_value.get(key, UNDEF))
            except Exception as exc:
                raise ValueError('{}: {}'.format(key, exc))

        self._validate_first()

    def format(self):
        return self.value

    def _validate_first(self):
        if self.required and self.value == UNDEF:
            raise ValueError('Field is required')
        if not self.nullable and self.value is None:
            raise ValueError('Expected not None')
        if self.value == UNDEF:
            self.value = None
        if self.value is not None:
            for validator in self.validators:
                validator(self)
            self.validate_fields()
            self.validate()

    def validate_fields(self):
        for key in self._fields:
            validator = getattr(self, 'validate_{}'.format(key), None)
            if validator:
                try:
                    validator(getattr(self, key))
                except Exception as exc:
                    raise ValueError('{}: {}'.format(key, exc))

    def validate(self):
        """В классе-потомке провалидировать"""
        pass
