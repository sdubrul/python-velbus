"""
:author: Thomas Delaet <thomas@delaet.org
"""
import velbus

class VMB2PBNModule(velbus.Module):
    """
    Velbus input module with 6 channels
    """
    def __init__(self, module_type, module_name, module_address, controller):
        velbus.Module.__init__(self, module_type, module_name, module_address, controller)
        self._is_closed = {}
        self._is_enabled = {}
        self._callbacks = {}

    def is_closed(self, channel):
        if channel in self._is_closed:
            return self._is_closed[channel]
        return False

    def _load(self):
        message = velbus.ModuleStatusRequestMessage(self._address)
        message.channels = list(range(1, self.number_of_channels()+1))
        self._controller.send(message)

    def number_of_channels(self):
        return 2

    def _on_message(self, message):
        if isinstance(message, velbus.PushButtonStatusMessage):
            for channel in message.closed:
                self._is_closed[channel] = True
            for channel in message.opened:
                self._is_closed[channel] = False
            for channel in message.get_channels():
                if channel in self._callbacks:
                    for callback in self._callbacks[channel]:
                        callback(self._is_closed[channel])
        elif isinstance(message, velbus.ModuleStatusMessage2):
            for channel in list(range(1, self.number_of_channels() + 1)):
                if channel in message.closed:
                    self._is_closed[channel] = True
                else:
                    self._is_closed[channel] = False
                if channel in message.enabled:
                    self._is_enabled[channel] = True
                else:
                    self._is_enabled[channel] = False


    def on_status_update(self, channel, callback):
        """
        Callback to execute on status of update of channel
        """
        if not channel in self._callbacks:
            self._callbacks[channel] = []
        self._callbacks[channel].append(callback)

    def get_categories(self, channel):
        if channel in self._is_enabled and self._is_enabled[channel]:
            return ['binary_sensor']
        else:
            return []


class VMB6PBNModule(VMB2PBNModule):
    """
    Velbus input module with 7 channels
    """
    def number_of_channels(self):
        return 6

velbus.register_module('VMB2PBN', VMB2PBNModule)
velbus.register_module('VMB6PBN', VMB6PBNModule)
