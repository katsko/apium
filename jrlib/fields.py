from datetime import datetime


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
                 default=UNDEF):
        self.value = UNDEF
        # TODO: if validators isn't list - raise exception
        # not raise ValueError, should new type for Internal Error
        self.validators = validators if isinstance(validators, list) else []
        self.required = required
        self.nullable = nullable
        self.default = default

    def __get__(self, obj, cls):
        return self.value

    def __set__(self, obj, value):
        self.value = value
        if self.value == UNDEF and self.default != UNDEF:
            self.value = self.default()\
                if callable(self.default) else self.default
        # self.value = self.to_python(self.value)
        self.value = self.clean()
        self._validate_first()

    def clean(self):
        """В классе-потомке привести поле к нужному типу и почистить.
        Например, привести float в int или
        удалить лишние пробелы в строке"""
        return self.value

    # TODO: to_python не нужен, можно преобразовывать и чистиь в clean
    # def to_python(value):
    #     """В классе-потомке привести значение к нужному типу, например,
    #     из int в float"""
    #     return value

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
    def validate(self):
        if not isinstance(self.value, int):
            raise TypeError('Expected int')


class Str(Field):
    def validate(self):
        if not isinstance(self.value, str):
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
    def validate(self):
        super(Date, self).validate()
        self.value = datetime.strptime(self.value, '%Y-%m-%d')


class List(Field):
    def validate(self):
        if not isinstance(self.value, list):
            raise ValueError('Expected list')


class MetaObjField(type):
    def __new__(self, name, bases, namespace):
        cls = super(MetaObjField, self).__new__(self, name, bases, namespace)
        cls._fields = [key for key, val in namespace.items()
                       if isinstance(val, BaseField)]
        return cls


class Obj(BaseField, metaclass=MetaObjField):

    def __init__(self, validators=None, required=False, nullable=True,
                 default=UNDEF, fields=None):
        print('class objfield init')
        self.value = UNDEF
        # TODO: if validators isn't list - raise exception
        # not raise ValueError, should new type for Internal Error
        self.validators = validators if isinstance(validators, list) else []
        self.required = required
        self.nullable = nullable
        self.default = default

        if isinstance(fields, dict):
            for key, val in fields.items():
                setattr(type(self), key, val)
                if isinstance(val, BaseField):
                    self._fields.append(key)

    def __set__(self, obj, value):
        self.value = value
        if self.value == UNDEF and self.default != UNDEF:
            self.value = self.default()\
                if callable(self.default) else self.default
        self.value = self.clean()

        print('O F {}'.format(self._fields))
        obj_value = {} if self.value == UNDEF else self.value
        for key in self._fields:
            try:
                print('OBJF - {} : {}'.format(key, obj_value.get(key, UNDEF)))
                setattr(self, key, obj_value.get(key, UNDEF))
            except Exception as exc:
                raise ValueError('{}: {}'.format(key, exc))

        self._validate_first()

    def clean(self):
        """В классе-потомке привести поле к нужному типу и почистить.
        Например, привести float в int или
        удалить лишние пробелы в строке"""
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
