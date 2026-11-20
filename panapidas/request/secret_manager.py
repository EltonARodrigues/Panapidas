# secret_manager.py
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

import gi
gi.require_version("Secret", "1")
from gi.repository import Secret, GLib

from panapidas.utils.logger import logger
from panapidas import const


class SecretManager:

    def __init__(self):
        self.schema = Secret.Schema.new(
            const.APP_ID,
            Secret.SchemaFlags.NONE,
            {
                "var_id": Secret.SchemaAttributeType.STRING,
                "group_id": Secret.SchemaAttributeType.STRING,
                "variable": Secret.SchemaAttributeType.STRING,
            },
        )

    def save(self, name: str, value: str, attr: dict, callback=None):

        def _finish(source, result, _data):
            try:
                Secret.password_store_finish(result)
                if callback:
                    callback(True)
            except GLib.Error as e:
                logger.error(f"Error to save secret {name}: {e}")
                if callback:
                    callback(False)

        Secret.password_store(
            self.schema,
            attr,
            Secret.COLLECTION_DEFAULT,
            name,
            value,
            None,
            _finish,
            None
        )

    def delete_secret(self, attr_filter: dict, callback = None):

        attr = {}

        if "var_id" in attr_filter:
            attr["var_id"] = attr_filter["var_id"]

        if "group_id" in attr_filter:
            attr["group_id"] = attr_filter["group_id"]

        if "variable" in attr_filter:
            attr["variable"] = attr_filter["variable"]

        def on_clear_complete(source, result, user_data):
            try:
                deleted = Secret.password_clear_finish(result)
                if deleted:
                    logger.info(f"Deleted secret(s) for {attr}")
                else:
                    logger.warning(f"No secret to delete for {attr}")
                if callback:
                    callback(True)
            except GLib.Error as e:
                logger.error(f"Failed to delete secret: {e.message}")
                if callback:
                    callback(False)

        Secret.password_clear(
            self.schema,
            attr,
            None,  # cancellable
            on_clear_complete,
            None   # user_data
        )

    def load_envs(self, attr: dict, on_result=None):

        def _finish(source, result, _data):
            try:
                items = Secret.password_search_finish(result)
                envs = self._group_envs(items)
                if on_result:
                    on_result(envs, None)
            except GLib.Error as e:
                logger.error(f"Error to list secrets: {e}")
                if on_result:
                    on_result([], e)

        Secret.password_search(
            self.schema,
            attr or {},
            Secret.SearchFlags.ALL
            | Secret.SearchFlags.UNLOCK
            | Secret.SearchFlags.LOAD_SECRETS,
            None,
            _finish,
            None,
        )

    @staticmethod
    def _group_envs(itens: list) ->  dict:
        env_dict = {}

        for item in itens:
            secret = item.retrieve_secret_sync(None)
            secret_value = secret.get().decode("utf-8")


            attr = dict(item.get_attributes() or {})

            group_id = attr.get("group_id", "<sem tipo>")
            env_var_dict = {"id": attr["var_id"], "key": attr["variable"], "value": secret_value}
            finded_env =  group_id in env_dict

            if finded_env:
                env_dict[group_id].append(env_var_dict)
            else:
                env_dict[group_id] = [env_var_dict]

        return env_dict
