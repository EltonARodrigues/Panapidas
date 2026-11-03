# env_object.py
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

import uuid

from gi.repository import GObject

from panapidas.model.map_entry import MapEntry


class EnvObject(GObject.Object):
    __gtype_name__ = "EnvObject"

    __gsignals__ = {
        "env-changed": (GObject.SignalFlags.RUN_FIRST, None, ()),
    }

    def __init__(self, id=None, name=None, envs_map=[], status=None):
        super().__init__()
        self._id = str(uuid.uuid4()) if id is None else id
        self._name = name
        self.status = status or "UNCHANGE"
        self._envs = EnvObject.map_builder(envs_map)

    @GObject.Property(type=int)
    def id(self) -> int:
        return self._id

    @GObject.Property(type=str)
    def name(self) -> str:
        return self._name

    @GObject.Property()
    def envs(self) -> str:
        return self._envs

    @envs.setter
    def envs(self, envs_map_entry: list[MapEntry]) -> str:
        self._envs = envs_map_entry
        self.emit("env-changed")

    @name.setter
    def name(self, name: str):
        self._name = name

    @GObject.Property()
    def dict_envs(self):
        return [env_map.to_dict() for env_map in self._envs]

    @staticmethod
    def map_builder(envs_map):
        return [
            MapEntry(id=env.get("id"), key=env.get("key"), value=env.get("value"))
            for env in envs_map
        ]

    def to_dict(self) -> dict[str, any]:
        return {
            "id": self.id,
            "name": self.name,
            "envs_map": [env_map.to_dict() for env_map in self._envs],
        }

    def clear_deleted_envs(self):
        self._envs = list(filter(lambda env: env.status != "DELETED", self._envs))
        self.emit("env-changed")

class ActiveEnvs(EnvObject):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        super().__init__()
        self._id = None
        self._name = None
        self._envs = []

        self._initialized = True

    def initialize(self, env_id=None, name=None, env_list=None):
        self._id = env_id
        self._name = name
        self._envs = env_list or []
        self.emit("env-changed")

    def set_env(self, key: str, value: str) -> None:
        for env in self._envs:
            if env.key == key:
                env.status = "UPDATED"
                env.value = value
                break
        else:
            self._envs.append(MapEntry(id=str(uuid.uuid4()), key=key, value=value, active=True, status="UPDATED"))
        self.emit("env-changed")

    def get_env(self, key: str) -> str | None:
        for env in self._envs:
            if env.key == key:
                return env.value
        return None
