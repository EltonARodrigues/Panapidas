# copy_code.py
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

from gi.repository import GObject, Gdk, Gtk


@Gtk.Template(
    resource_path="/dev/eltonarodrigues/panapidas/widget/copy_code.ui"
)
class CopyCode(Gtk.Box):
    __gtype_name__ = "CopyCode"

    text_label = Gtk.Template.Child()

    _code_text = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @GObject.Property(type=str, default="")
    def code_text(self):
        return self._code_text

    @code_text.setter
    def code_text(self, value):
        self.text_label.set_label(value)
        self._code_text = value

    @Gtk.Template.Callback()
    def copy_text(self, _widget: Gtk.Button):
        clipboard = self.get_clipboard()
        clipboard.set(self._code_text)
