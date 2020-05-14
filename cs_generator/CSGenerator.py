import os
import logging
import re
from enum import Enum
from inspect import isclass
from collections.abc import Iterable
from pystache import Renderer
from typing import (List, Union, Dict, Tuple, Set, FrozenSet, Optional, _GenericAlias)
from .utils import is_customized_class, is_elemental, is_collection
from .tests.conftest import Job

BUILTIN_TYPES = {list, dict, float, set, frozenset, int, str, Enum, type(None)}
SUPPORTED_TYPES = {int, float, str, bool, list, dict, set, frozenset, tuple}
ELEMENTAL_MAP = {
    float: 'float',
    str: 'string',
    int: 'int',
    bool: 'bool'
}

cls_tmpl_path = os.path.abspath(os.path.join(__file__, '../template/cls_tmpl.mustache'))
enum_tmpl_path = os.path.abspath(os.path.join(__file__, '../template/enum_tmpl.mustache'))

logger = logging.getLogger(__name__)

def anno_to_types(anno, ref_keeping=False) -> str:
    '''
    Args:
        anno: typing annotation
        ref_keeping: whether reference preserving is used in .Net json deserialization
    Return:
        type string in C#
    '''
    if isinstance(anno, _GenericAlias):
        origin = anno.__dict__['__origin__']
        args = anno.__dict__['__args__']
        if origin is Union:
            if len(args) == 2 and type(None) in args:
                for x in args:
                    if x is not type(None):
                        inner_anno = x
                        break
                # return Nullable tmpl only another arg is value type
                inner_type = anno_to_types(inner_anno, ref_keeping)
                outer_type = ('{0}?', '{0}?') if inner_anno in (float, int, bool) or issubclass(inner_anno, Enum) else ('{0}', '{0}')
                field_type = outer_type[0].format(inner_type[0])
                param_type = outer_type[1].format(inner_type[1])
                return (field_type, param_type)
            else:
                return ('dynamic', 'dynamic')
        elif origin in (list, set, tuple, frozenset):
            inner_anno = args[0]
            inner_type = anno_to_types(inner_anno, ref_keeping)
            outer_type = ('IList<{0}>' if ref_keeping else 'IReadOnlyList<{0}>', 'List<{0}>')
            field_type = outer_type[0].format(inner_type[0])
            param_type = outer_type[1].format(inner_type[1])
            return (field_type, param_type)
        elif origin is dict:
            key_anno = args[0]
            value_anno = args[1]
            key_type = anno_to_types(key_anno)
            value_type = anno_to_types(value_anno)
            outer_type = ('IDictionary<{0}, {1}>' if ref_keeping else 'IReadOnlyDictionary<{0}, {1}>', 'Dictionary<{0}, {1}>')
            field_type = outer_type[0].format(key_type[0], value_type[0])
            param_type = outer_type[1].format(key_type[1], value_type[1])
            return (field_type, param_type)
        else:
            raise Exception(f"Unsupported generic alias: {anno}")
    elif anno in ELEMENTAL_MAP:
        t = ELEMENTAL_MAP[anno]
        return (t, t)
    elif anno.__module__ == 'builtins':
        raise Exception(f"Unsupported type {anno}")
    else:
        return (anno.__name__, anno.__name__)
        
def read_all_text(filename):
    with open(filename, 'r') as fp:
        return fp.read()

class RefKeeping(Enum):
    Never = 0
    All = 1
    Some = 2

class CSGenerator:
    angle_pat = re.compile(r"&[lg]t;")
    angle_repl = lambda match: "<" if match.group(0) == "&lt;" else ">"
    cls_tmpl = read_all_text(cls_tmpl_path)
    enum_tmpl = read_all_text(enum_tmpl_path)
    def __init__(self, obj, ref_keeping: Union[bool, Iterable]=False):
        self.obj = obj
        # set up flag and temp containers
        self._ref_keeping_cls = set()
        if isinstance(ref_keeping, bool):
            self.ref_keeping = RefKeeping.All if ref_keeping else RefKeeping.Never
        elif isinstance(ref_keeping, Iterable):
            self.ref_keeping = RefKeeping.Never if len(ref_keeping) == 0 else RefKeeping.Some
            for x in ref_keeping:
                self._ref_keeping_cls.add(x)
        else:
            self.ref_keeping = RefKeeping.Never
        self._classes = set()
        self._enums = set()
        self._cls_info = []
        self._enum_info = []
        self._used_names = set()
        # register all user defined classes and enums
        if isclass(obj):
            if obj in SUPPORTED_TYPES:
                raise Exception(f"{obj} is builtin type. Only user-defined classes and enums are supported.")
            else:
                self._register_customized_class(obj)
        else:
            self._register(obj)
        # parsing
        for x in self._classes:
            info = self._parse_cls(x)
            logger.debug(f"{x}: info len: {len(info)}")
            if len(info) > 0:
                self._cls_info.append(info)
        for x in self._enums:
            info = self._parse_enum(x)
            logger.debug(f"{x}: info len: {len(info)}")
            if len(info) > 0:
                self._enum_info.append(info)
        self._renderer = Renderer(file_encoding='utf-8', string_encoding='utf-8')
    
    def _register(self, obj):
        if is_elemental(obj):
            return
        elif is_collection(obj):
            self._register_collection(obj)
        elif is_customized_class(obj):
            self._register_customized_class(obj.__class__)

    def _register_collection(self, obj):
        if isinstance(obj, (list, tuple, set,frozenset)):
            for x in obj:
                self._register(x)
        elif isinstance(obj, (dict)):
            for k, v in obj:
                self._register(v)

    def _register_customized_class(self, cls):
        if issubclass(cls, Enum):
            self._enums.add(cls)
        else:
            if not hasattr(cls, '__annotations__'):
                logger.warning(f"{cls} is not registered (having no annotations attr).")
                return
            annos = cls.__annotations__
            if len(annos) == 0:
                logger.warning(f"{cls} is not registered (having no annotations).")
                return
            self._classes.add(cls)
            # continue register every annotated field
            # add customized cls
            for k, v in annos.items():
                self._register_annotation(v)

    def _register_annotation(self, anno):
        if anno in BUILTIN_TYPES or anno.__module__ == 'builtins':
            return
        elif isinstance(anno, _GenericAlias):
            for x in anno.__dict__['__args__']:
                self._register_annotation(x)
        else:
            self._register_customized_class(anno)

    def _parse_cls(self, cls):
        if not hasattr(cls, '__annotations__'):
            logger.warning(f"{cls} has no annotations attr.")
            return {}
        annos = cls.__annotations__
        if len(annos) == 0:
            logger.warning(f"{cls} has no annotations.")
            return {}
        name = self._get_available_name(cls.__name__)
        info = {
            "name": name,
            "field": []
        }
        # determine ref_keeping for this cls
        if self.ref_keeping == RefKeeping.All:
            ref_keeping = True
        elif self.ref_keeping == RefKeeping.Never:
            ref_keeping = False
        elif cls in self._ref_keeping_cls:
            ref_keeping = True
        else:
            ref_keeping = False
        logger.debug(f"{cls}: {self.ref_keeping} {ref_keeping}")
        # obtain type info from annotations
        for k, v in annos.items():
            field_type, param_type = anno_to_types(v, ref_keeping=ref_keeping)
            info['field'].append(
                {
                    "fieldName": k,
                    "fieldType": field_type,
                    "paramType": param_type
                }
            )
        if len(info['field']) > 0:
            info['field'][-1]['endLine'] = True
        return info
    
    def _parse_enum(self, cls):
        if len(cls) == 0:
            logger.warning(f"Enum {cls.__name__} has no member.")
            return {}
        name = self._get_available_name(cls.__name__)
        self._used_names.add(name)
        info = {
            "name": name,
            "item": []
        }
        for x in cls:
            info["item"].append(
                {
                    "itemName": x.name,
                    "itemValue": x.value
                }
            )
        if len(info["item"]) > 0:
            info["item"][-1]["endLine"] = True
        return info
    
    def _get_available_name(self, name):
        suffix = 1
        while CSGenerator._format_name(name, suffix) in self._used_names:
            suffix += 1
        return CSGenerator._format_name(name, suffix)
    
    @staticmethod
    def _format_name(name, suffix):
        if suffix < 2:
            return name
        return name + '_' + str(suffix)
    
    @staticmethod
    def _test_dynamic(info):
        for x in info['field']:
            if 'dynamic' in x['fieldType'] or 'dynamic' in x['paramType']:
                return True
        return False

    def export(self, namespace, dest_folder):
        for info in self._cls_info:
            info['namespace'] = namespace
            if CSGenerator._test_dynamic(info):
                info['dynamic'] = [{}]
            filename = os.path.join(dest_folder, info['name'] + '.cs')
            with open(filename, 'w') as fp:
                text = self._renderer.render(CSGenerator.cls_tmpl, info)
                text = CSGenerator.angle_pat.sub(CSGenerator.angle_repl, text)
                fp.write(text)
        
        for info in self._enum_info:
            info['namespace'] = namespace
            filename = os.path.join(dest_folder, info['name'] + '.cs')
            with open(filename, 'w') as fp:
                text = self._renderer.render(CSGenerator.enum_tmpl, info)
                text = CSGenerator.angle_pat.sub(CSGenerator.angle_repl, text)
                fp.write(text)
