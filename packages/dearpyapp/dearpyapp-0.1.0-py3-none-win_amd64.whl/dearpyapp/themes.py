import functools
import typing as t

import dearpygui.dearpygui as dpg


def wraps_hint(decorator: t.Callable) -> t.Callable:  # TODO to common utils
    return decorator


@wraps_hint
def _functools_cache(f):
    return functools.cache(f)


@_functools_cache
def dpg_get_color_theme(colors, text_color: t.Optional[tuple] = None,
                        text_align: t.Optional[tuple] = None,
                        item_types: t.Optional[t.Union[int, tuple]] = None):
    item_types = item_types or dpg.mvAll
    if not isinstance(item_types, (list, tuple)):
        item_types = (item_types,)

    with dpg.theme() as theme:
        for item_type in item_types:
            with dpg.theme_component(item_type):
                dpg.add_theme_color(dpg.mvThemeCol_Header, colors[0])
                dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, colors[1])
                dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, colors[2])

                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, colors[0])
                dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, colors[1])
                dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, colors[2])

                dpg.add_theme_color(dpg.mvThemeCol_Button, colors[0])
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, colors[1])
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, colors[2])

                dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 0, 0)

                if text_color:
                    dpg.add_theme_color(dpg.mvThemeCol_Text, text_color)

                if text_align:
                    dpg.add_theme_style(dpg.mvStyleVar_WindowTitleAlign, *text_align)
                    dpg.add_theme_style(dpg.mvStyleVar_SelectableTextAlign, *text_align)
                    dpg.add_theme_style(dpg.mvStyleVar_ButtonTextAlign, *text_align)
    return theme
