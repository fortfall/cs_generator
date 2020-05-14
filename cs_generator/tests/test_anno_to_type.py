import logging
import pytest
from ..CSGenerator import anno_to_types

logger = logging.getLogger(__name__)

def test_int_var(int_var):
    t = anno_to_types(int_var)
    logger.debug(t)
    assert t == ('int', 'int')

def test_float_var(float_var):
    t = anno_to_types(float_var)
    logger.debug(t)
    assert t == ('float', 'float')

def test_str_var(str_var):
    t = anno_to_types(str_var)
    logger.debug(t)
    assert t == ('string', 'string')

def test_bool_var(bool_var):
    t = anno_to_types(bool_var)
    logger.debug(t)
    assert t == ('bool', 'bool')

def test_cls_var(cls_var):
    t = anno_to_types(cls_var)
    logger.debug(t)
    assert t == ('Dog', 'Dog')

def test_nullable_int(nullable_int):
    t = anno_to_types(nullable_int)
    logger.debug(t)
    assert t == ('int?', 'int?')

def test_nullbale_enum(nullable_enum):
    t = anno_to_types(nullable_enum)
    logger.debug(t)
    assert t == ('Job?', 'Job?')

def test_nullable_cls(nullable_cls):
    t = anno_to_types(nullable_cls)
    logger.debug(t)
    assert t == ('Dog', 'Dog')

def test_dyanmic(dynamic):
    t = anno_to_types(dynamic)
    logger.debug(t)
    assert t == ('dynamic', 'dynamic')

def test_lst_var(lst_var):
    t = anno_to_types(lst_var)
    logger.debug(t)
    assert t == ('IReadOnlyList<float>', 'List<float>')
    t = anno_to_types(lst_var, True)
    logger.debug(t)
    assert t == ('IList<float>', 'List<float>')

def test_lst_nullable_dog(lst_nullable_dog):
    t = anno_to_types(lst_nullable_dog)
    logger.debug(t)
    assert t == ('IReadOnlyList<Dog>', 'List<Dog>')
    t = anno_to_types(lst_nullable_dog, True)
    logger.debug(t)
    assert t == ('IList<Dog>', 'List<Dog>')

def test_lsy_dynamic(lst_dynamic):
    t = anno_to_types(lst_dynamic)
    logger.debug(t)
    assert t == ('IReadOnlyList<dynamic>', 'List<dynamic>')
    t = anno_to_types(lst_dynamic, True)
    logger.debug(t)
    assert t == ('IList<dynamic>', 'List<dynamic>')

def test_tup_var(tup_var):
    t = anno_to_types(tup_var)
    logger.debug(t)
    assert t == ('IReadOnlyList<int>', 'List<int>')
    t = anno_to_types(tup_var, True)
    logger.debug(t)
    assert t == ('IList<int>', 'List<int>')

def test_tup_dynamic(tup_dynamic):
    t = anno_to_types(tup_dynamic)
    logger.debug(t)
    assert t == ('IReadOnlyList<dynamic>', 'List<dynamic>')
    t = anno_to_types(tup_dynamic, True)
    logger.debug(t)
    assert t == ('IList<dynamic>', 'List<dynamic>')

def test_dct_int_str(dct_int_str):
    t = anno_to_types(dct_int_str)
    logger.debug(t)
    assert t == ('IReadOnlyDictionary<int, string>', 'Dictionary<int, string>')
    t = anno_to_types(dct_int_str, True)
    logger.debug(t)
    assert t == ('IDictionary<int, string>', 'Dictionary<int, string>')

def test_dct_str_dynamic(dct_str_dynamic):
    t = anno_to_types(dct_str_dynamic)
    logger.debug(t)
    assert t == ('IReadOnlyDictionary<string, dynamic>', 'Dictionary<string, dynamic>')
    t = anno_to_types(dct_str_dynamic, True)
    logger.debug(t)
    assert t == ('IDictionary<string, dynamic>', 'Dictionary<string, dynamic>')

def test_dct_enum_flaot(dct_enum_float):
    t = anno_to_types(dct_enum_float)
    logger.debug(t)
    assert t == ('IReadOnlyDictionary<Job, float>', 'Dictionary<Job, float>')
    t = anno_to_types(dct_enum_float, True)
    logger.debug(t)
    assert t == ('IDictionary<Job, float>', 'Dictionary<Job, float>')

def test_nested(nested):
    t = anno_to_types(nested)
    logger.debug(t)
    assert t == ('IReadOnlyList<IReadOnlyDictionary<string, Job?>>', 
                 'List<Dictionary<string, Job?>>')
    t = anno_to_types(nested, True)
    logger.debug(t)
    assert t == ('IList<IDictionary<string, Job?>>', 
                 'List<Dictionary<string, Job?>>')
