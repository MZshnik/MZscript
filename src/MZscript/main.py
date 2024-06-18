import asyncio

import disnake
from disnake.ext import commands

from functions_collector import FunctionsCore


class MZClient:
    def __init__(self, intents: str = "all", on_ready: str = "$console[Bot is ready]"):
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
        self.bot = commands.InteractionBot(intents=intents)
        self.funcs = FunctionsCore(self)
        self.bot.add_listener(self.on_ready, disnake.Event.ready)
        self.bot.add_listener(self.on_message, disnake.Event.message)

    async def update_commands(self):
        """
        ## Updating command names which have $function in the name.
        ### Example input name: `$getVar[prefix]help`
        ### Output: `!help`
        """
        for i in self.exec_on_start:
            self.user_commands[i][0] = await self.funcs.is_have_functions(self.user_command_names[i], disnake.message.Message)

    async def run_code(self, code: str, ctx: disnake.message.Message = None):
        """
        ## Async run provided code

        #### Args:
            code (`str`): Code with functions (example: `$getVar[prefix]`, `$if[1==1] $text[text1] $else $text[text2] $endif`)
            ctx (`disnake.message.Message`): Context, default is None

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

    async def on_ready(self):
        if self.user_on_ready:
            await self.run_code(self.user_on_ready)
        await self.update_commands()

    async def on_message(self, message: disnake.message.Message):
        if message.author == self.bot.user:
            return
        splited_command = message.content.split(" ")
        for i in self.user_commands:
            if splited_command[0] == i[0]:
                message.content = " ".join(splited_command[1:])
                await self.run_code(i[1], message)

    def run(self, token: str):
        self.bot.run(token)