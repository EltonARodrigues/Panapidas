# add_certificate.py
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

from gi.repository import Gtk, Gio, Adw


@Gtk.Template(
    resource_path="/dev/eltonarodrigues/panapidas/widget/add_certificate.ui"
)
class AddCertificateDialog(Adw.AlertDialog):
    __gtype_name__ = "AddCertificateDialog"

    crt_action_row = Gtk.Template.Child()
    key_action_row = Gtk.Template.Child()
    pfx_action_row = Gtk.Template.Child()

    def __init__(self):
        super().__init__()

        self.file_dialog = Gtk.FileDialog()

        self.certificate = {
            "url": None,
            "crt": None,
            "key": None,
            "pfx": None,
        }

        self.set_response_enabled("save", False)

    def get_certificate(self):
        return self.certificate

    def _enable_save_button(self):
        if self.certificate["url"] and (
            self.certificate["crt"] or self.certificate["key"] or self.certificate["pfx"]
        ):
            self.set_response_enabled("save", True)
        else:
            self.set_response_enabled("save", False)

    def _on_file_opened(
        self, dialog: Gtk.FileDialog, result: Gio.AsyncResult, row: Adw.ActionRow, file_type: str
    ):
        file = dialog.open_finish(result)
        path = "file://" + file.get_path()
        row.set_subtitle(path)
        self.certificate[file_type] = path
        self._enable_save_button()

    @Gtk.Template.Callback()
    def on_add_key_path(self, _: Gtk.ToggleButton):
        self.file_dialog.open(
            self.get_root(), None, self._on_file_opened, self.key_action_row, "key"
        )

    @Gtk.Template.Callback()
    def on_add_crt_path(self, _: Gtk.ToggleButton):
        self.file_dialog.open(
            self.get_root(), None, self._on_file_opened, self.crt_action_row, "crt"
        )

    @Gtk.Template.Callback()
    def on_add_pfx_path(self, _: Gtk.ToggleButton):
        self.file_dialog.open(
            self.get_root(), None, self._on_file_opened, self.pfx_action_row, "pfx"
        )

    @Gtk.Template.Callback()
    def on_certificate_url_changed(self, entry: Adw.EntryRow):
        self.certificate["url"] = entry.get_text()
        self._enable_save_button()
