# import_dialog.py
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

from gi.repository import Adw, GObject, Gio, Gtk


@Gtk.Template(
    resource_path="/dev/eltonarodrigues/panapidas/widget/import_dialog.ui"
)
class ImportDialog(Adw.Dialog):
    __gtype_name__ = "ImportDialog"

    __gsignals__ = {
        "import-file-selected": (GObject.SignalFlags.RUN_FIRST, None, (str,)),
    }

    def __init__(self):
        super().__init__()

        self.file_dialog = Gtk.FileDialog()


    def _on_collection_opened(self, dialog: Gtk.FileDialog, result: Gio.AsyncResult):
        file = dialog.open_finish(result)
        import_path = file.get_path()
        self.close()
        self.emit("import-file-selected", import_path)

    @Gtk.Template.Callback()
    def on_import_collection(self, widget: Gtk.Button):
        self.file_dialog.open(self.get_root(), None, self._on_collection_opened)
