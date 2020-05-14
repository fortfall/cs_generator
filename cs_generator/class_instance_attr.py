import logging
from typing import (List, Dict, Union, Tuple, Optional, _GenericAlias)
from enum import Enum

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Base:
    attr = 1

class Derived(Base):
    pass

Derived.attr = 2

class Job(Enum):
    Teacher = 0
    Engineer = 1
    Doctor = 2

class Hop:
    def __init__(self):
        pass

class Test:
    static = 'static'
    job_attr: Job
    cls_attr: int
    ls_attr: List[int]
    nested: List[Dict[str, Job]]
    mixed: Union[Hop, None]
    tup: Tuple[str, int]
    opt_attr: Optional[Base]
    no_anno = None
    def __init__(self):
        self.a: int
        self.a = 5


if __name__ == "__main__":
    j = Job.Teacher
    annos = Test.__annotations__
    print(annos)
    nested = annos['nested']
    mixed = annos['mixed']
    tup = annos['tup']
    cls_attr = annos['cls_attr']
    job_attr = annos['job_attr']
    opt_attr = annos['opt_attr']
    nested_args = nested.__dict__['__args__']
    print(opt_attr.__dict__)
    # for x in nested.__dict__['__args__']:
    #     print(x, isinstance(x, _GenericAlias))
    

    # print(job_attr.__dict__, '\n')
    # print(nested.__dict__, '\n')
    # print(cls_attr.__dict__, '\n')
    
    # print(mixed.__dict__)
    # print(tup.__dict__)
    # print(List.__module__)
    # print(list.__module__)
    
