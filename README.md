### Introduction
python script for generating C# files for Newtonsoft.Json deserialization from python enums and annotated classes.
### Installation
* from pip
```python
pip install cs_generator
```
* download package and run setup.py
```python
python setup.py install
```

### Usage
* Annotate classes that are to be converted to C#; should be annotated on class level.
* All used enum types will be converted (no annotation is needed)
* If reference keeping is used in deserialization, set ref_keeping to True
```python
from enum import Enum
from typing import List
from cs_generator import CSGenerator

class Job(Enum):
    Teachert = 0
    Engineer = 1
    Doctor = 2

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

csg = CSGenerator(Person, ref_keeping=True)
csg.export('TestNamespace', dest_folder)
# or
p = Person('Jack', 33, Job.Teacher, ['Swimming', 'Video Games', 'Fishing'])
csg = CSGenerator(p, ref_keeping=True)
csg.export('TestNamespace', dest_folder)
```
output cs script
```csharp
using Newtonsoft.Json;

namespace TestNamespace
{
    public enum Job
    {
        Teacher = 0,
        Engineer = 1,
        Doctor = 2
    }
}
```
```csharp
using System.Collections.Generic;
using Newtonsoft.Json;

namespace TestNamesapce
{
    public partial class Person    
    {
        public readonly string name; 
        public readonly int age; 
        public readonly Job job; 
        public readonly IList<string> hobbies; 

        [JsonConstructor]
        public Person(
            string name,
            int age,
            Job job,
            List<string> hobbies
        )
        {
            this.name = name;
            this.age = age;
            this.job = job;
            this.hobbies = hobbies;
        }
    }
}
```