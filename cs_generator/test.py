from enum import Enum

class Job(Enum):
    Teacher = 0
    Doctor = 1

j = Job.Teacher
print(j.__class__)
for x in Job:
    print(x.name, x.value)