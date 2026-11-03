# script_info_page.py
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

from panapidas.widget.copy_code import CopyCode

@Gtk.Template(
    resource_path="/eltonarodrigues/org/codeberg/panapidas/page/script_info_page.ui"
)
class ScripInfoPage(Adw.PreferencesDialog):
    __gtype_name__ = "ScripInfoPage"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)