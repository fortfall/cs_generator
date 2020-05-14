import os
import pytest
from ..CSGenerator import CSGenerator
from .conftest import Test, Person, Job

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

@pytest.fixture
def folders(dest_folder):
    folder_1 = os.path.abspath(os.path.join(dest_folder, 'no_ref_keeping'))
    if not os.path.exists(folder_1):
        os.mkdir(folder_1)
    folder_2 = os.path.abspath(os.path.join(dest_folder, 'ref_keeping'))
    if not os.path.exists(folder_2):
        os.mkdir(folder_2)
    return (folder_1, folder_2)


def test_person_export(person, folders):
    folder_1 = folders[0]
    folder_2 = folders[1]
    csg = CSGenerator(person)
    csg.export('TestNamesapce', folder_1)
    csg = CSGenerator(person, True)
    csg.export('TestNamespace', folder_2)
    assert os.path.exists(os.path.join(folder_1, 'Person.cs'))
    assert os.path.exists(os.path.join(folder_2, 'Person.cs'))

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


