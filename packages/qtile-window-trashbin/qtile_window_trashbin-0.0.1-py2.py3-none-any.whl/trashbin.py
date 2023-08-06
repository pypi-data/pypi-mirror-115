# Copyright (C) 2021 Paul Hoffmann <phfn@phfn.de

#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.

#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.

"A thrashbin for qtile windows."

__version__ = "0.0.1"

from libqtile.core.manager import Qtile
from libqtile.backend.base import Window
from libqtile import qtile
from libqtile.log_utils import logger

class Trashbin(list[Window]):

    def __init__(self, group_name, delay = 5) -> None:
        self.delay = delay
        self.group_name = group_name

    def remove(self, win: Window):
        "Remove a window from the trash."
        super().remove(win)


    def restore(self, win: Window, group_name):
        "Remove a window from the trash."
        self.remove(win)
        win.togroup(group_name)

    def kill(self, win: Window):
        if win not in self:
            # when the callback comes, it may allready be removed.
            logger.info("window didn't get killed, cuz its allready removed")
            return
        self.remove(win)
        win.kill()

    def append(self, win: Window) -> None:
        super().append(win)
        win.togroup(self.group_name)
        qtile.call_later(self.delay, self.kill, win)

    def append_currend_window(self, qtile: Qtile) -> None:
        win = qtile.current_window
        if win is None:
            logger.info("tring to append current_window but got None from qtile")
            return
        self.append(win)

    def pop_to_current_group(self, qtile: Qtile):
        if len(self) <= 0:
            logger.info("tring to remove window from trashbin, when trashbin is allready empty")
            return
        win = self[-1]
        self.restore(win, qtile.current_group.name)


    def __len__(self):
        return super().__len__()

    def __getitem__(self, i: int) -> Window:
        return super().__getitem__(i)

    def __delitem__(self, key) -> None:
        super().__delitem__(key)

    def __setitem__(self, key, win: Window):
        super().__setitem__(key, win)

    def __iter__(self):
        return super().__iter__()
