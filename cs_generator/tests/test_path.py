import os
import pytest
from ..CSGenerator import cls_tmpl_path, enum_tmpl_path

@pytest.fixture(params=[cls_tmpl_path, enum_tmpl_path])
def tmpl_path(request):
    return request.param

def test_path(tmpl_path):
    assert os.path.exists(tmpl_path)