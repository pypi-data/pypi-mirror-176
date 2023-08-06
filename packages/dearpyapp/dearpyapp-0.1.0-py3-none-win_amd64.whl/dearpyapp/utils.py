from types import FunctionType
from contextlib import contextmanager
from collections import ChainMap

import dearpygui.dearpygui as dpg
import dearpygui._dearpygui as internal_dpg
from recordclass import make_dataclass, dataobject


_top_container_name = 'mvWindowAppItem'
_container_name_lookup = {
    dpg.mvWindowAppItem: _top_container_name,
    dpg.mvChildWindow: 'mvChildWindow',
    dpg.mvGroup: 'mvGroup',
    dpg.mvTab: 'mvTab'
}

_not_container_name_lookup = {
    dpg.mvCombo: 'mvCombo',
    dpg.mvMenuBar: 'mvMenuBar',
    dpg.mvDragFloat: 'mvDragFloat',
    dpg.mvDragInt: 'mvDragInt',
    dpg.mvButton: 'mvButton',
    dpg.mvCheckbox: 'mvCheckbox',
}

_item_type_lookup = {v: k for k, v in ChainMap(_container_name_lookup,
                                               _not_container_name_lookup).items()}


def dpg_get_item_name(item) -> str:
    return internal_dpg.get_item_info(item)["type"].rsplit('::')[1]


def dpg_get_item_type(item) -> int:
    item_type = _item_type_lookup.get(dpg_get_item_name(item))
    assert item_type is not None
    return item_type


def dpg_get_container(item, container_type: int = dpg.mvWindowAppItem) -> int:
    container_name = _container_name_lookup.get(container_type)
    assert container_name is not None
    first_iter = True
    while True:
        item_name = dpg_get_item_name(item)
        if not first_iter and item_name == container_name:
            return item
        elif item_name == _top_container_name:
            return
        first_iter = False
        item = dpg.get_item_parent(item)


@contextmanager
def dpg_container(tag):
    try:
        dpg.push_container_stack(tag)
        yield tag
    finally:
        dpg.pop_container_stack()


# TODO переделать под датакласс
def dpg_uuid(cls, return_values=False):
    def wrap():
        values = list()
        for name, class_ in cls.__annotations__.items():
            if isinstance(class_, FunctionType) and class_.__qualname__ == wrap.__qualname__:
                value = class_()
            else:
                is_named_tuple = class_.__base__ is tuple and hasattr(class_, '_fields')
                try:
                    class_.__annotations__
                except AttributeError:
                    if is_named_tuple:
                        value = class_(*(dpg.generate_uuid() for _ in range(len(getattr(class_, '_fields')))))
                    else:
                        value = dpg.generate_uuid()
                else:
                    if is_named_tuple:
                        value = class_(*dpg_uuid(class_, return_values=True)())
                    else:
                        value = dpg_uuid(class_, )()

            values.append(value)

        if return_values:
            return values
        else:
            factory = cls if cls.__base__ is dataobject else \
                make_dataclass(cls.__name__, cls.__annotations__.keys(), fast_new=True)
            return factory(*values)

    return wrap


# TODO поддержка dataclass, tuple, list
# TODO делать перевод значения в соответсвующий класс типа int str и т.д.
# TODO возможность выгружать в существующий объект, а не создавать новый
# TODO переделка под dpg.get_values для оптимизации
# TODO периодически проверять, не изменил ли viewport свой размер, или просто по евенту перемещения окна сделать
def dpg_get_values(gui_obj):
    cls = getattr(gui_obj, '__class__')
    values = list()
    for tag, cls_ in cls.__annotations__.items():
        gui_obj_ = getattr(gui_obj, tag)
        is_named_tuple = cls_.__base__ is tuple and hasattr(cls_, '_fields')
        try:
            cls_.__annotations__
        except AttributeError:
            if is_named_tuple:
                value = cls_(*(dpg.get_value(getattr(gui_obj_, tag_)) for tag_ in cls_))
            else:
                value = cls_(dpg.get_value(gui_obj_))
        else:
            value = dpg_get_values(gui_obj_)
        values.append(value)
    return cls(*values)


def dpg_set_values(gui_obj, val_obj):
    cls = getattr(val_obj, '__class__')
    for tag, cls_ in cls.__annotations__.items():
        gui_obj_ = getattr(gui_obj, tag)
        val_obj_ = getattr(val_obj, tag)
        is_named_tuple = cls_.__base__ is tuple and hasattr(cls_, '_fields')
        try:
            cls_.__annotations__
        except AttributeError:
            if is_named_tuple:
                for tag_ in cls_:
                    dpg.set_value(getattr(gui_obj_, tag_), getattr(val_obj_, tag_))
            else:
                dpg.set_value(gui_obj_, val_obj_)
        else:
            dpg_set_values(gui_obj_, val_obj_)
