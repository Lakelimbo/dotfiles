import datetime

from ignis import utils, widgets
from ignis.options import options
from ignis.services.audio import AudioService
from ignis.services.bluetooth import BluetoothDevice, BluetoothService
from ignis.services.network import NetworkService
from ignis.services.notifications import NotificationService
from ignis.services.recorder import RecorderService
from ignis.variable import Variable
from ignis.window_manager import WindowManager

from ..indicator_icon import IndicatorIcon, NetworkIndicatorIcon

network = NetworkService.get_default()
notifications = NotificationService.get_default()
recorder = RecorderService.get_default()
audio = AudioService.get_default()

window_manager = WindowManager.get_default()

current_time = Variable(
    value=utils.Poll(1000, lambda x: datetime.datetime.now().strftime("%H:%M")).bind(
        "output"
    )
)


class WifiIcon(NetworkIndicatorIcon):
    def __init__(self):
        super().__init__(device_type=network.wifi, other_device_type=network.ethernet)


class EthernetIcon(NetworkIndicatorIcon):
    def __init__(self):
        super().__init__(device_type=network.ethernet, other_device_type=network.wifi)


class VpnIcon(IndicatorIcon):
    def __init__(self):
        super().__init__(
            image=network.vpn.bind("icon_name"),
            visible=network.vpn.bind("is_connected"),
        )


class BluetoothIcon(IndicatorIcon):
    def __init__(self):
        super().__init__(
            image="bluetooth-symbolic",
            visible=BluetoothDevice.connected,
        )


class DNDIcon(IndicatorIcon):
    def __init__(self):
        super().__init__(
            image="notification-disabled-symbolic",
            visible=options.notifications.bind("dnd"),
        )


class RecorderIcon(IndicatorIcon):
    def __init__(self):
        super().__init__(
            image="media-record-symbolic",
            css_classes=["record-indicator"],
            setup=lambda self: recorder.connect(
                "notify::is-paused", self.__update_css_class
            ),
            visible=recorder.bind("active"),
        )

    def __update_css_class(self, *args) -> None:
        if recorder.is_paused:
            self.remove_css_class("active")
        else:
            self.add_css_class("active")


class VolumeIcon(IndicatorIcon):
    def __init__(self):
        super().__init__(
            image=audio.speaker.bind("icon_name"),
        )


class StatusPill(widgets.Button):
    def __init__(self, monitor: int):
        self._monitor = monitor
        self._window = window_manager.get_window("ignis_CONTROL_CENTER")

        super().__init__(
            child=widgets.Box(
                child=[
                    BluetoothIcon(),
                    RecorderIcon(),
                    WifiIcon(),
                    EthernetIcon(),
                    VpnIcon(),
                    VolumeIcon(),
                    DNDIcon(),
                    widgets.Label(
                        label=current_time.bind("value"),
                    ),
                ]
            ),
            css_classes=self._window.bind(
                "visible",
                lambda value: (
                    ["clock", "unset", "active"] if value else ["clock", "unset"]
                ),
            ),
            on_click=self.__on_click,
        )

    def __on_click(self, x) -> None:
        if self._window.monitor == self._monitor:
            self._window.visible = not self._window.visible
        else:
            self._window.set_monitor(self._monitor)
            self._window.visible = True
