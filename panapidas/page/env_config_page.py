# env_config_page.py
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

from gi.repository import Adw, Gtk, GObject

from panapidas.widget.map_list_menu import MapListMenu
from panapidas.model.env_object import ActiveEnvs, EnvObject


@Gtk.Template(
    resource_path="/eltonarodrigues/org/codeberg/panapidas/page/env_config_page.ui"
)
class EnvConfigPage(Adw.NavigationPage):
    __gtype_name__ = "EnvConfigPage"

    __gsignals__ = {
        "env-saved": (GObject.SignalFlags.RUN_FIRST, None, (EnvObject,)),
    }

    env_list = Gtk.Template.Child()
    save_env_button = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.params = None
        self.env_object = None

    def set_env(self, env_object: EnvObject):
        self.env_object = env_object
        self.params = MapListMenu(self.env_list, env_object.envs, None, False, False)
        self.params.connect("map-changed", self._on_map_change)

    def _on_map_change(self, widget: MapListMenu):
        self.env_object.envs = widget.get_map_entry()
        self.save_env_button.set_sensitive(True)

    @Gtk.Template.Callback()
    def on_env_save(self, _: Gtk.Button):
        active_envs = ActiveEnvs()
        active_envs.initialize(
            self.env_object.id, self.env_object.name, self.env_object.envs
        )
        self.emit("env-saved", self.env_object)
