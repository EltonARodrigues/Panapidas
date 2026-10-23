import gi

gi.require_version("Secret", "1")
from gi.repository import Secret, GLib


class SecretManager:

    def __init__(self, schema_nome: str):
        self.schema = Secret.Schema.new(
            schema_nome,
            Secret.SchemaFlags.NONE,
            {
                "var_id": Secret.SchemaAttributeType.STRING,
                "group_id": Secret.SchemaAttributeType.STRING,
                "variable": Secret.SchemaAttributeType.STRING,
            },
        )

        self._service = None

    def _get_service(self):
        if self._service is None:
            self._service = Secret.Service.get_sync(Secret.ServiceFlags.NONE, None)
        return self._service

    def save(self, name: str, value: str, attr: dict, on_done=None):

        def _finish(source, result, _data):
            try:
                source.store_finish(result)
                if on_done:
                    on_done(True, None)
            except GLib.Error as e:
                print(f"Error to save secret {name}: {e}")
                if on_done:
                    on_done(False, e)

        self._get_service().store(
            self.schema,
            attr,
            Secret.COLLECTION_DEFAULT,
            name,
            Secret.Value(value, len(value), "str"),
            None,  # Cancellable
            _finish,
            None,
        )

    def save_sync(self, name: str, value: str, attr: dict) -> bool:
        try:
            print(attr)
            self._get_service().store_sync(
                self.schema,
                attr,
                Secret.COLLECTION_DEFAULT,
                name,
                Secret.Value(value, len(value), "str"),
                None,
            )
            return True
        except GLib.Error as e:
            print(f"Error to save secret {name}: {e}")
            return False

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
                deleted = source.clear_finish(result)
                if deleted:
                    print(f"Deleted secret(s) for {attr}")
                else:
                    print(f"No secret to delete for {attr}")
                if callback:
                    callback(True)
            except GLib.Error as e:
                print(f"Failed to delete secret: {e.message}")
                if callback:
                    callback(False)

        self._get_service().clear(
            self.schema,
            attr,
            None,  # cancellable
            on_clear_complete,
            None   # user_data
        )

    def load_envs(self, attr: dict, on_result=None):

        def _finish(source, result, _data):
            try:
                items = source.search_finish(result)
                envs = self._group_envs(items)
                if on_result:
                    on_result(envs, None)
            except GLib.Error as e:
                print(f"Error to list secrets: {e}")
                if on_result:
                    on_result([], e)

        self._get_service().search(
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
    def _group_envs(itens: list[dict]) ->  dict:
        env_dict = {}
        for index, item in enumerate(itens):
            item.load_secret_sync(None)
            secret_value = item.get_secret().get_text()

            attr = dict(item.get_attributes() or {})
            print(attr)

            group_id = attr.get("group_id", "<sem tipo>")
            env_var_dict = {"id": attr["var_id"], "key": attr["variable"], "value": secret_value}
            finded_env =  group_id in env_dict

            if finded_env:
                env_dict[group_id].append(env_var_dict)
            else:
                env_dict[group_id] = [env_var_dict]

        return env_dict
