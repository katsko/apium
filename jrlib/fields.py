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
    def __init__(self, required=False, nullable=True):
        self.value = UNDEF
        self.required = required
        self.nullable = nullable

    def __get__(self, obj, cls):
        return self.value

    def __set__(self, obj, value):
        self.value = value
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
            self.validate()

    def validate(self):
        """В классе-потомке провалидировать"""
        pass


class IntField(Field):
    def validate(self):
        if not isinstance(self.value, int):
            raise TypeError('Expected int')


class CharField(Field):
    def validate(self):
        if not isinstance(self.value, str):
            raise TypeError('Expected str')


class DictField(Field):
    def validate(self):
        if not isinstance(self.value, dict):
            raise TypeError('Expected dict (json)')


class EmailField(CharField):
    def validate(self):
        super(EmailField, self).validate()
        if '@' not in self.value:
            raise ValueError('Expected email')


class DateField(CharField):
    def validate(self):
        super(DateField, self).validate()
        self.value = datetime.strptime(self.value, '%Y-%m-%d')


class ListField(Field):
    def validate(self):
        if not isinstance(self.value, list):
            raise ValueError('Expected list')


class MetaObjField(type):
    def __new__(self, name, bases, namespace):
        cls = super(MetaObjField, self).__new__(self, name, bases, namespace)
        cls._fields = [key for key, val in namespace.items()
                       if isinstance(val, BaseField)]
        return cls


class ObjField(BaseField, metaclass=MetaObjField):

    def __init__(self, required=False, nullable=True, fields=None):
        print('class objfield init')
        self.value = UNDEF
        self.required = required
        self.nullable = nullable

        if isinstance(fields, dict):
            for key, val in fields.items():
                setattr(type(self), key, val)
                if isinstance(val, BaseField):
                    self._fields.append(key)

    def __set__(self, obj, value):
        self.value = value
        self.value = self.clean()

        print('O F {}'.format(self._fields))
        if self.value != UNDEF:
            for key in self._fields:
                try:
                    print('OBJF - {} : {}'.format(key, self.value.get(key)))
                    setattr(self, key, self.value.get(key, UNDEF))
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
            self.validate()

    def validate(self):
        """В классе-потомке провалидировать"""
        pass
