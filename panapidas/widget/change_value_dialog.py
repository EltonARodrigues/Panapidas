# change_value_dialog.py
#
# Copyright 2026 Elton de Andrade Rodrigues
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-only

from gi.repository import Adw, Gtk


@Gtk.Template(
    resource_path="/eltonarodrigues/org/codeberg/panapidas/widget/change_value_dialog.ui"
)
class ChangeValueDialog(Adw.AlertDialog):
    __gtype_name__ = "ChangeValueDialog"

    value_entry = Gtk.Template.Child()

    def __init__(self, heading: str, body: str, value: str, **kwargs):
        super().__init__(heading=heading, body=body, **kwargs)
        self.value_entry.set_text(value or "")
        self._value = value

    def get_value(self) -> str:
        return self.value_entry.get_text()

    @Gtk.Template.Callback()
    def on_change_value(self, widget: Gtk.Button):
        self._value = self.get_value()
