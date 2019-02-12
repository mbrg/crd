#!/usr/bin/env python3.7

import pyperclip

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, ListProperty
from kivy.uix.listview import ListItemButton
from kivy.uix.popup import Popup
from kivy.clock import Clock

from crd.storage import AzureKeyVaultStorage
from crd.config import ConfigurationManager


class SecretListButton(ListItemButton):
    pass


class SecretStore(BoxLayout):
    secret_list = ObjectProperty()
    secret_key_ti = ObjectProperty()
    secret_value_ti = ObjectProperty()

    vault_ti = ObjectProperty()
    tenant_ti = ObjectProperty()

    tabbed_view = ObjectProperty()
    tab_add = ObjectProperty()
    tab_sync = ObjectProperty()

    def __init__(self, **kwargs):
        super(SecretStore, self).__init__(**kwargs)

        self.strg = None
        self.init_storage()

    def popup(self, txt):
        popup = Popup(title=txt, separator_height=0, title_align="center", content=None,
                      auto_dismiss=True, size_hint=(.5, .1))
        popup.open()

        Clock.schedule_once(lambda _: popup.dismiss(), 3.0)

    def init_storage(self):
        try:
            with ConfigurationManager() as cfg:
                if all(v in cfg.cache for v in ("vault", "tenant_id")):
                    self.strg = AzureKeyVaultStorage(vault=cfg.cache["vault"],
                                                     tenant_id=cfg.cache["tenant_id"])
        except (TypeError, ValueError):
            self.popup("Missing/bad configuration")

    def refresh_configuration(self):
        with ConfigurationManager() as cfg:
            self.vault_ti.text = cfg.cache.get("vault", "")
            self.tenant_ti.text = cfg.cache.get("tenant_id", "")

    def set_configuration(self):
        if self.vault_ti.text == "" or self.tenant_ti.text == "":
            self.popup("Please submit valid details")

        with ConfigurationManager() as cfg:
            cfg.cache = {
                "storage": "azure",
                "vault": self.vault_ti.text,
                "tenant_id": self.tenant_ti.text}
        self.popup("Saved changes")
        self.init_storage()

    def refresh_secrets(self):
        if not isinstance(self.strg, AzureKeyVaultStorage):
            return

        self.secret_list.adapter.data = sorted(list(self.strg))
        self.secret_list.adapter.update_for_new_data()

    def get_secret(self):
        if not isinstance(self.strg, AzureKeyVaultStorage):
            return

        if self.secret_list.adapter.selection:
            key = self.secret_list.adapter.selection[0].text

            try:
                pyperclip.copy(self.strg[key])
                self.popup("Secret copied to clipboard")
            except KeyError:
                self.popup("Key wasn't found")
        else:
            self.popup("Please select a key")

    def update_secret(self):
        if self.secret_list.adapter.selection:
            key = self.secret_list.adapter.selection[0].text

            try:
                self.secret_key_ti.text = key
                self.secret_value_ti.text = ""
                self.tabbed_view.switch_to(self.tab_add)
            except KeyError:
                self.popup("Key wasn't found")
        else:
            self.popup("Please select a key")

    def set_secret(self):
        if not isinstance(self.strg, AzureKeyVaultStorage):
            return

        if self.secret_key_ti.text == "" or self.secret_value_ti.text == "":
            self.popup("Name/Secret can't be empty")
            return

        self.strg[self.secret_key_ti.text] = self.secret_value_ti.text
        self.popup("Secret stored safely")

        self.refresh_secrets()
        self.tabbed_view.switch_to(self.tab_sync)

    def delete_secret(self):
        if not isinstance(self.strg, AzureKeyVaultStorage):
            return

        if self.secret_key_ti.text == "":
            self.popup("Name can't be empty")
            return

        try:
            del self.strg[self.secret_key_ti.text]
            self.popup("Secret deleted")

            self.refresh_secrets()
            self.tabbed_view.switch_to(self.tab_sync)
        except KeyError:
            self.popup("Key wasn't found")


class SecretStoreApp(App):
    def build(self):
        self.title = "Hush"

        self.secret_store = SecretStore()
        return self.secret_store

    def on_start(self):
        Clock.schedule_once(lambda x: self.secret_store.refresh_secrets(), 1.0)


if __name__ == "__main__":
    dbApp = SecretStoreApp()
    dbApp.run()
