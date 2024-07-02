import asyncio
import os
import importlib.util

import disnake
from disnake.ext import commands

from .functions_collector import FunctionsCore


class MZClient:
    def __init__(self, intents: str = "all", on_ready: str = "$console[Bot is ready]", db_warns: bool = False, debug_log: bool = False, debug_console: bool = True):
        if isinstance(intents, disnake.Intents):
            pass
        elif intents.lower() == "all":
            intents = disnake.Intents.all()
        elif intents.lower() == "default":
            intents = disnake.Intents.default()
        else:
            raise ValueError("In intents you need to select \"all\" or \"default\" value")
        self.user_on_ready = on_ready
        self.user_commands = []
        self.user_command_names = []
        self.exec_on_start = []
        self.user_events = {"message": None, "button": None, "interaction": None}
        self.bot = commands.InteractionBot(intents=intents)
        self.funcs = FunctionsCore(self, db_warns, debug_log, debug_console)
        self.bot.add_listener(self.on_ready, disnake.Event.ready)
        self.bot.add_listener(self.on_message, disnake.Event.message)
        self.bot.add_listener(self.on_button_click, disnake.Event.button_click)
        self.bot.add_listener(self.on_intreaction, disnake.Event.interaction)

    async def update_commands(self):
        """
        ## Updating command names which have $function in the name.
        ### Example input name: `$getVar[prefix]help`
        ### Output: `!help`
        """
        for i in self.exec_on_start:
            self.user_commands[i][0] = await self.funcs.is_have_functions(self.user_command_names[i], disnake.Message)

    async def run_code(self, code: str, ctx: disnake.Message = None):
        """
        ## Async run provided code

        #### Args:
            code (`str`): Code with functions (example: `$getVar[prefix]`, `$if[1==1] $text[text1] $else $text[text2] $endif`)
            ctx (`disnake.Message`): Context, default is None

        #### Returns:
            `str`: result of executed functions
        """
        chunks = await self.funcs.get_chunks(code)
        await self.funcs.check_ifs(chunks)
        chunks = await self.funcs.execute_chunks(chunks, ctx)
        if chunks or len(chunks) > 0:
            return "".join(chunks)
        return "" 

    def add_command(self, name: str, code: str):
        """
        ## Add command to handlering

        #### Args:
            name (`str`): Trigger what execute command if any person type it in chat. Can execute functions like name of command `$getVar[prefix]help` and finale command name will be view like `!help`
            code (`str`): Code for execute when command invoked. For send message always use $sendMessage - plain text not send. Check docs for info about stable functions.
        """
        self.user_commands.append([name, code])
        self.user_command_names.append(name)
        chunks = asyncio.run(self.funcs.get_chunks(name))
        for i in chunks:
            if i.startswith("$"):
                self.exec_on_start.append(len(self.user_commands)-1)

    def load_command(self, path):
        try:
            spec = importlib.util.find_spec(path)
            lib = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(lib)
        except:
            print(f"Cannot import commands from path \"{path}\"")

        try:
            lib.setup(self)
        except:
            print(f"Cannot find setup function for commands in \"{path}\"")

    def load_commands(self, dir):
        for folder in [i for i in os.walk(dir) if i != "__pycache__"]:
            for file in [i for i in folder[2] if i.endswith(".py")]:
                try:
                    export = folder[0].replace("\\", ".")+"."+file[:-3]
                    spec = importlib.util.find_spec(export)
                    lib = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(lib)
                except:
                    print(f"Cannot import commands from path \"{export}\"")

                try:
                    lib.setup(self)
                except:
                    print(f"Cannot find setup function for commands in \"{folder[0]}\"")

    def add_event(self, name: str, code: str):
        if name in self.user_events.keys():
            self.user_events[name] = code
        else:
            raise SyntaxError(f"\"{name}\" event dosnot exists.")

    async def on_ready(self):
        if self.user_on_ready:
            await self.run_code(self.user_on_ready)
        await self.update_commands()

    async def on_message(self, message: disnake.Message):
        """
        `message` event
        Executed when someone send message(and bots)
        """
        if self.user_events["message"]:
            await self.run_code(self.user_events["message"], message)
        if message.author.bot:
            return
        splitted_command = message.content.split(" ")
        for i in self.user_commands:
            if splitted_command[0] == i[0]:
                message.content = " ".join(splitted_command[1:])
                await self.run_code(i[1], message)

    async def on_button_click(self, inter: disnake.MessageInteraction):
        """
        `button` event
        Executed when someone clicked button
        """
        if self.user_events["button"]:
            await self.run_code(self.user_events["button"], inter)

    async def on_intreaction(self, inter: disnake.MessageInteraction):
        """
        `interaction` event
        Executed when some of interactions(buttons/menus and etc.) are invoked
        """
        if self.user_events["interaction"]:
            await self.run_code(self.user_events["interaction"], inter)

    def run(self, token: str):
        self.bot.run(asyncio.run(self.funcs.is_have_functions(token)))