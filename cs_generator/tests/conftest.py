import pytest
from enum import Enum
from typing import (List, Dict, Tuple, Set, FrozenSet, Union, Dict, DefaultDict, Optional)

class Job(Enum):
    Teacher = 0
    Engineer = 1
    Doctor = 2

class Dog:
    pass

class Person:
    name: str
    age: int
    job: Job
    hobbies: List[str]
    def __init__(self, name, age, job, hobbies):
        self.name = name
        self.age = age
        self.job = job
        self.hobbies = hobbies

class Person1:
    name: str
    age: int
    job: Job
    hobbies: List[str]
    def __init__(self, name, age, job, hobbies):
        self.name = name
        self.age = age
        self.job = job
        self.hobbies = hobbies

class Test:
    int_var: int
    float_var: float
    str_var: str
    bool_var: bool
    enum_var: Job
    cls_var: Dog
    nullable_int: Optional[int]
    nullable_enum: Optional[Job]
    nullable_cls: Optional[Dog]
    dynamic: Union[str, int]
    lst_var: List[float]
    lst_nullable_dog: List[Union[None, Dog]]
    lst_dynamic: List[Union[Job, Dog]]
    tup_var: Tuple[int]
    tup_dynamic: Tuple[Union[str, Dog]]
    dct_int_str: Dict[int, str]
    dct_str_dynamic: Dict[str, Union[Job, Dog]]
    dct_enum_float: Dict[Job, float]
    nested: List[Dict[str, Optional[Job]]]

@pytest.fixture(params=[Test()])
def annos(request):
    return request.param.__annotations__

@pytest.fixture
def int_var(annos):
    return annos['int_var']

@pytest.fixture
def float_var(annos):
    return annos['float_var']

@pytest.fixture
def str_var(annos):
    return annos['str_var']

@pytest.fixture
def bool_var(annos):
    return annos['bool_var']

@pytest.fixture
def enum_var(annos):
    return annos['enum_var']

@pytest.fixture
def cls_var(annos):
    return annos['cls_var']

@pytest.fixture
def nullable_int(annos):
    return annos['nullable_int']

@pytest.fixture
def nullable_enum(annos):
    return annos['nullable_enum']

@pytest.fixture
def nullable_cls(annos):
    return annos['nullable_cls']

@pytest.fixture
def dynamic(annos):
    return annos['dynamic']

@pytest.fixture
def lst_var(annos):
    return annos['lst_var']

@pytest.fixture
def lst_nullable_dog(annos):
    return annos['lst_nullable_dog']

@pytest.fixture
def lst_nullable_dog(annos):
    return annos['lst_nullable_dog']

@pytest.fixture
def lst_dynamic(annos):
    return annos['lst_dynamic']

@pytest.fixture
def tup_var(annos):
    return annos['tup_var']

@pytest.fixture
def tup_dynamic(annos):
    return annos['tup_dynamic']

@pytest.fixture
def dct_int_str(annos):
    return annos['dct_int_str']

@pytest.fixture
def dct_str_dynamic(annos):
    return annos['dct_str_dynamic']

@pytest.fixture
def dct_enum_float(annos):
    return annos['dct_enum_float']

@pytest.fixture
def nested(annos):
    return annos['nested']