# map_entry.py
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

from gi.repository import GObject


class MapEntry(GObject.Object):
    __gtype_name__ = "MapEntry"

    def __init__(self, id: int, key: str, value: str, active: bool = True, status: str ="UNCHANGED"):
        super().__init__()

        self._id = id
        self._active = active
        self._key = key
        self._value = value
        self._status = status

    @GObject.Property(type=int)
    def id(self) -> int:
        return self._id

    @GObject.Property(type=str)
    def key(self) -> str:
        return self._key

    @GObject.Property(type=str)
    def value(self) -> str:
        return self._value

    @GObject.Property(type=str)
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, status: str):
        self._status = status

    @GObject.Property(type=bool, default=True)
    def active(self) -> bool:
        return self._active

    @active.setter
    def active(self, active: bool):
        self._active = active

    @key.setter
    def key(self, key: str):
        self._key = key

    @value.setter
    def value(self, value: str):
        self._value = value

    def __repr__(self):
        return f"MapEntry(id={self.id}, key={self.key}, value={self.value}) active={self.active}"

    def __str__(self):
        return f"{self._id} -> ({self._key}:{self._value}) active={self.active}"

    def to_dict(self) -> dict[str, str]:
        return {
            "id": self.id,
            "key": self.key,
            "value": self.value,
            "active": self.active,
            "status": self.status,
        }

