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

from gettext import gettext as _
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
    empty_status_page = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.params = None
        self.env_object = None
        self.search_text = None

        self.env_list.set_filter_func(self._filtrar_linha)


    def set_env(self, env_object: EnvObject):
        self.set_title(env_object.name)
        self.env_object = env_object
        self.params = MapListMenu(self.env_list, env_object.envs, None, False, False)
        self.params.connect("map-changed", self._on_map_change)

    def _filtrar_linha(self, row: Gtk.ListBoxRow):
        env_name: str =  row.get_child().get_first_child().get_text()

        if self.search_text is None or self.search_text == "":
            return True

        if self.search_text in env_name:
            return True
        return False

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

    def _on_empty_filter_result(self):
        child = self.env_list.get_first_child()
        while child is not None:
            if isinstance(child, Gtk.ListBoxRow) and child.get_child_visible():
                return False
            child = child.get_next_sibling()

        return True

    @Gtk.Template.Callback()
    def on_search_change(self, search_entry: Gtk.SearchEntry):
        self.search_text = search_entry.get_text()
        self.params = None
        self.env_list.invalidate_filter()

        if self._on_empty_filter_result():
            self.empty_status_page.set_visible(True)
            self.empty_status_page.set_description(_("No matches found for your search."))
            self.env_list.set_visible(False)
        else:
            self.empty_status_page.set_visible(False)
            self.env_list.set_visible(True)
