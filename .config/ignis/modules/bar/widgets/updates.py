import asyncio

from ignis import utils, widgets


class Updates(widgets.Box):
    def __init__(self):
        script_path = "$HOME/.dotfiles/.config/ignis/scripts/check_updates.sh"

        self.label = widgets.Label(label="…")
        super().__init__(
            css_classes=["updates", "unset"],
            child=[
                widgets.Icon(image="update-medium", pixel_size=16),
                self.label,
            ],
            visible=False,
        )

        utils.Poll(21_600_000, lambda x: asyncio.create_task(
            self._update_total(script_path)))

    async def _update_total(self, script_path):
        try:
            result = await utils.exec_sh_async(f"sh {script_path}")
            total = result.stdout.strip()
            self.label.label = f" {total}"
            self.visible = total != "0"
        except Exception:
            self.label.label = " Err"
            self.visible = False
