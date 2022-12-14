"""This is the C2 commander Class which handles the devices & listeners"""
from typing import Optional
import subprocess
from threading import Thread
from multiprocessing import Process
from phoenix_framework.server.kits.base_handler import BaseHandler
from phoenix_framework.server.kits.base_listener import BaseListener
from phoenix_framework.server.plugins.base import BasePlugin
from phoenix_framework.server.utils.web import FlaskThread

INVALID_ID = "Invalid ID"
HANDLER_DOES_NOT_EXIST = "Handler doesn't exist"
LISTENER_DOES_NOT_EXIST = "Listener doesn't exist"


class Commander:
    """This is the Commander which handles the devices & listeners"""

    def __init__(self):
        self.web_server: FlaskThread
        self.active_listeners: dict[int, BaseListener] = {}
        self.active_handlers: dict[int, BaseHandler] = {}
        self.active_plugins: dict[str, BasePlugin] = {}

    def get_active_handler(self, handler_id: int) -> Optional[BaseHandler]:
        """Get a handler by id"""
        try:
            return self.active_handlers[int(handler_id)]
        except ValueError as e:
            raise ValueError(INVALID_ID) from e
        except KeyError as e:
            raise KeyError(HANDLER_DOES_NOT_EXIST) from e

    def get_active_listener(self, listener_id: int) -> Optional[BaseListener]:
        """Get a listener by id"""
        try:
            return self.active_listeners[int(listener_id)]
        except ValueError as e:
            raise ValueError(INVALID_ID) from e
        except KeyError:
            raise KeyError(LISTENER_DOES_NOT_EXIST) from None

    def add_active_listener(self, listener: BaseListener):
        """Add a listener to the commander"""
        self.active_listeners[int(listener.id)] = listener

    def add_active_handler(self, handler: BaseHandler):
        """Add a handler to the commander"""
        self.active_handlers[int(handler.id)] = handler

    def remove_active_listener(self, listener_id: int):
        """Remove a listener from the commander"""
        try:
            self.active_listeners.pop(int(listener_id))
        except ValueError as e:
            raise ValueError(INVALID_ID) from e
        except KeyError as e:
            raise KeyError(LISTENER_DOES_NOT_EXIST) from e

    def remove_active_handler(self, handler_id: int):
        """Remove a device from the commander by id"""
        try:
            self.active_handlers.pop(int(handler_id))
        except ValueError as e:
            raise ValueError(INVALID_ID) from e
        except KeyError as e:
            raise KeyError(HANDLER_DOES_NOT_EXIST) from e

    def load_plugin(self, plugin: BasePlugin, config: dict):
        """Load a plugin"""
        if plugin.name in self.active_plugins:
            raise KeyError(f"Plugin {plugin.name} already loaded")

        if plugin.execution_type not in ["function", "thread", "process", "file"]:
            raise ValueError(f"Invalid execution type {plugin.execution_type}")
        try:
            if plugin.execution_type == "function":
                plugin.execute(self, config)
            elif plugin.execution_type == "thread":
                Thread(target=plugin.execute, args=(self, config), name=plugin.name).start()
            elif plugin.execution_type == "process":
                Process(target=plugin.execute, args=(self, config), name=plugin.name).start()
            elif plugin.execution_type == "file":
                subprocess.Popen([plugin.execute])
        except Exception as e:
            raise Exception(f"Failed to load plugin '{plugin.name}'") from e

        self.active_plugins[plugin.name] = plugin

    def unload_plugin(self, plugin_name: str):
        """Unload a plugin"""
        try:
            self.active_plugins.pop(plugin_name)
        except KeyError as e:
            raise KeyError(f"Plugin {plugin_name} not loaded") from e
