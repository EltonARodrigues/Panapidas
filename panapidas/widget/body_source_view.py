# body_source_view.py
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

from gi.repository import Gtk, GtkSource, GObject, Adw


@Gtk.Template(
    resource_path="/eltonarodrigues/org/codeberg/panapidas/widget/body_source_view.ui"
)
class BodySourceView(GtkSource.View):
    __gtype_name__ = "BodySourceView"

    buffer = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_language("json")

        self.scheme_manager = GtkSource.StyleSchemeManager.get_default()
        self.style_manager = Adw.StyleManager.get_default()
        self.style_manager.connect("notify::dark", self.update_style)

        self.update_style()

    def set_language(self, language_name: str):
        lang_manager = GtkSource.LanguageManager.get_default()
        language = lang_manager.get_language(language_name)

        if language:
            self.buffer.set_language(language)

    def set_response(self, text: str):
        self.buffer.set_text(text, -1)
        

    def update_style(self):
        scheme = self.scheme_manager.get_scheme(
            "Adwaita-dark" if self.style_manager.get_dark() else "Adwaita",
        )
        self.buffer.set_style_scheme(scheme)
