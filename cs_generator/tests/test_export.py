import os
import pytest
from ..CSGenerator import CSGenerator
from .conftest import Test, Person, Job, Person1

@pytest.fixture(params=[('../samples')])
def dest_folder(request):
    return os.path.join(__file__, request.param)

@pytest.fixture(params=['TestNamespace'])
def namespace(request):
    return request.param

@pytest.fixture(params=[['Swimming', 'Video Games', 'Fishing']])
def hobbies(request):
    return request.param

@pytest.fixture(params=[{'name': 'Jack', 'age': 33, 'job': Job.Teacher}])
def person(request, hobbies):
    return Person(**request.param, hobbies=hobbies)

@pytest.fixture(params=[{'name': 'Mike', 'age': 44, 'job': Job.Doctor}])
def another_person(request, hobbies):
    return Person(**request.param, hobbies=hobbies)

@pytest.fixture
def folders(dest_folder):
    folder_1 = os.path.abspath(os.path.join(dest_folder, 'no_ref_keeping'))
    if not os.path.exists(folder_1):
        os.mkdir(folder_1)
    folder_2 = os.path.abspath(os.path.join(dest_folder, 'ref_keeping'))
    if not os.path.exists(folder_2):
        os.mkdir(folder_2)
    return (folder_1, folder_2)

@pytest.fixture
def person_dict(person, another_person):
    return {
        1: person,
        2: another_person
    }

def test_person_dict(person_dict, namespace, folders):
    folder_1 = folders[0]
    folder_2 = folders[1]

    os.remove(os.path.join(folder_1, 'Person.cs'))
    csg = CSGenerator(person_dict)
    csg.export(namespace, folder_1)
    assert os.path.exists(os.path.join(folder_1, 'Person.cs'))

    os.remove(os.path.join(folder_2, 'Person.cs'))
    csg = CSGenerator(person_dict, True)
    csg.export(namespace, folder_2)
    assert os.path.exists(os.path.join(folder_2, 'Person.cs'))



def test_person_export(person, namespace, folders):
    folder_1 = folders[0]
    folder_2 = folders[1]
    csg = CSGenerator(person)
    csg.export(namespace, folder_1)
    csg = CSGenerator(person, True)
    csg.export(namespace, folder_2)
    assert os.path.exists(os.path.join(folder_1, 'Person.cs'))
    assert os.path.exists(os.path.join(folder_2, 'Person.cs'))

def test_person1_export(namespace, folders):
    folder_1 = folders[0]
    folder_2 = folders[1]
    csg = CSGenerator(Person1)
    csg.export(namespace, folder_1)
    csg = CSGenerator(Person1, True)
    csg.export(namespace, folder_2)

def test_export(namespace, folders):
    folder_1 = folders[0]
    folder_2 = folders[1]

    t = Test()
    csg = CSGenerator(t)
    csg.export(namespace, folder_1)

    csg = CSGenerator(t, ref_keeping=True)
    csg.export(namespace, folder_2)
    assert os.path.exists(os.path.join(folder_1, 'Test.cs'))
    assert os.path.exists(os.path.join(folder_1, 'Job.cs'))
    assert os.path.exists(os.path.join(folder_2, 'Test.cs'))
    assert os.path.exists(os.path.join(folder_2, 'Job.cs'))


