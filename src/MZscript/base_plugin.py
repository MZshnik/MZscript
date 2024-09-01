from abc import ABC, abstractmethod

import disnake


class BasePlugin(ABC):
    """
    ## Base class for creating MZscript plugins
    ### This class discribes events what MZClient can call
    ### Only 1 method is required - `setup`. If it ignored, raises NotImplementedError
    """

    @abstractmethod
    def setup(self, client):
        """
        ## Setup plugin
        ### Required to implement. If it ignored, raises NotImplementedError

        ### Args:
            client (`MZClient`): Instance of MZClient class. Contains all user and bot settings/information
        """
        raise NotImplementedError("Method \"setup\" of BasePlugin not implemented")

    async def on_ready(self):
        pass

    async def on_message(self, message: disnake.Message):
        pass

    async def on_button_click(self, inter: disnake.MessageInteraction):
        pass

    async def on_interaction(self, inter: disnake.MessageInteraction):
        pass

    async def on_slash(self, inter: disnake.MessageInteraction):
        pass

    async def invoked(self, command: dict):
        pass

    async def check(self, command: dict):
        pass
