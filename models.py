"""Models and Validator for Petcare application"""

import re
from datetime import datetime


class Field:
    """validator class"""

    def __set_name__(self, owner, name):
        self.name = name

    def __set__(self, obj, value):
        self.validate(value)
        obj.__dict__[self.name] = value

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name)

    def validate(self, value):
        """validate value"""
        raise NotImplementedError("Subclasses should implement validate()")

class CharField(Field):
    """charfield validator"""

    def __init__(self, min_length=0, max_length=100):
        self.min_length = min_length
        self.max_length = max_length

    def validate(self, value):
        """ validate char fields  """
        if not isinstance(value, str):
            raise ValueError(f"{self.name} : must be string")
        if len(value) > self.max_length or len(value) < self.min_length:
            raise ValueError(
                f"{self.name} : length should be between {self.min_length} and {self.max_length}"
            )


class IntField(Field):
    """intfield validator"""

    def __init__(self, min_value=0, max_value=100):
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value):
        """ validate int fields  """
        if not isinstance(value, int):
            raise ValueError(f"{self.name} : must be integer")
        if value > self.max_value or value < self.min_value:
            raise ValueError(
                f"{self.name} : must be between {self.min_value} and {self.max_value}"
            )


class PasswordField(Field):
    """ Password validator  """            
    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, value):
        """ validate the value  """
        if not isinstance(value, str):
            raise ValueError(f"{self.name}: must be a string")
        if len(value) < self.min_length:
            raise ValueError(f"{self.name}: too short, min {self.min_length}")
        if not any(c.isupper() for c in value):
            raise ValueError(f"{self.name}: must have at least one uppercase")
        if not any(c.isdigit() for c in value):
            raise ValueError(f"{self.name}: must have at least one digit")
        if not any(c in "!@#$%^&*" for c in value):
            raise ValueError(f"{self.name}: must have at least one special char")


class EmailField(Field):
    """email validator"""

    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    def validate(self, value):
        """ validate email format  """
        if not re.match(self.email_pattern, value):
            raise ValueError(f"{self.name} : form is not as asked")


class PhoneField(Field):
    """ phone validator  """
    def validate(self, value):
        """ validate phone number  """
        if not isinstance(value, str):
            raise ValueError(f"{self.name}: must be a string")
        if not value.startswith("+"):
            raise ValueError(f"{self.name}: must start with +")
        digits = value[1:]  # remove the + sign
        if not digits.isdigit():
            raise ValueError(f"{self.name}: after + must be digits only")
        if len(digits) < 9:
            raise ValueError(f"{self.name}: too short")


class ChoiceField(Field):
    """ choice Field validator  """
    def __init__(self, choices=None):
        if choices is None:
            choices=[]
        if not isinstance(choices, list):
            raise ValueError("choices should be a list")
        self.choices = choices

    def validate(self, value):
        """ validate choice fields  """
        if value not in self.choices:
            raise ValueError(f"{self.name} should exist in {self.choices}")


class Pet:
    """ Pet model  """
    name = CharField(min_length=1, max_length=50)
    age = IntField(min_value=0, max_value=30)
    weight = IntField(min_value=0, max_value=200)
    species = ChoiceField(["dog", "cat", "rabbit", "bird", "hamster"])

    def __init__(self, name, age, weight, species):
        self.name = name
        self.age = age
        self.weight = weight
        self.species = species
        self.created_at = datetime.now()

    def __repr__(self):
        return f"Pet(name={self.name},age={self.age},species={self.species})"

    def as_dict(self):
        """  return the object as a dictionary    """
        return {
            "name": self.name,
            "age": self.age,
            "weight": self.weight,
            "species": self.species,
            "created_at": self.created_at,
        }
