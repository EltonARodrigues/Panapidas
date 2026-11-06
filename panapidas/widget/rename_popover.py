# rename_popover.py
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

from gi.repository import Gtk, GLib

from panapidas.model.requests import RequestItem


@Gtk.Template(
    resource_path="/dev/eltonarodrigues/panapidas/widget/rename_popover.ui"
)
class RenamePopover(Gtk.Popover):
    __gtype_name__ = "RenamePopover"

    save_new_name = Gtk.Template.Child()

    def __init__(self):
        super().__init__()

        self.set_position(Gtk.PositionType.RIGHT)

        self.save_new_name.set_action_name("app.rename-item")
        self.save_new_name.set_action_target_value(
            GLib.Variant.new_tuple(GLib.Variant("s", ""), GLib.Variant("s", ""))
        )

    def set_rename_item(self, item: RequestItem):
        self.item = item

    @Gtk.Template.Callback()
    def on_rename_change(self, widget: Gtk.Entry):
        self._rename = widget.get_text()
        item_id = GLib.Variant.new_string(self.item.id)
        new_name = GLib.Variant.new_string(self._rename)
        target = GLib.Variant.new_tuple(item_id, new_name)
        self.save_new_name.set_action_target_value(target)

    @Gtk.Template.Callback()
    def on_save_name(self, _widget: Gtk.Button):
        self.popdown()