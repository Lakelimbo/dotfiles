from ignis import widgets

from .widgets import (AppLauncher, Apps, Battery, KeyboardLayout, StatusPill,
                      Tray, Updates, Workspaces)


class Bar(widgets.Window):
    __gtype_name__ = "Bar"

    def __init__(self, monitor: int):
        super().__init__(
            anchor=["left", "bottom", "right"],
            exclusivity="exclusive",
            monitor=monitor,
            namespace=f"ignis_BAR_{monitor}",
            layer="top",
            kb_mode="none",
            child=widgets.CenterBox(
                css_classes=["bar-widget"],
                start_widget=widgets.Box(child=[AppLauncher(), Workspaces()]),
                center_widget=widgets.Box(child=[Apps()]),
                end_widget=widgets.Box(
                    child=[
                        Tray(),
                        Updates(),
                        KeyboardLayout(),
                        Battery(),
                        StatusPill(monitor),
                    ]
                ),
            ),
            css_classes=["unset"],
        )
