import asyncio
import sqlite3
from time import perf_counter  # for permormance log

import disnake
from disnake.ext import commands


class MZClient:
    pass

class CommandsHandler:
    pass

class Database:
    def __init__(self):
        self.connection = sqlite3.connect("database.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users(
            guild_id INT,
            user_id INT,
            var_name VARCHAR,
            var_value VARCHAR
            )""")

    async def get_global_var(self, var_name: str):
        result = self.cursor.execute("SELECT var_value FROM users WHERE user_id = ? AND var_name = ? AND guild_id = ?", (0, var_name, 0)).fetchone()
        if result:
            return result[0]
        else:
            return False

    async def get_value_from_member(self, guild_id: str, user_id: int, var_name: str):
        result = self.cursor.execute("SELECT var_value FROM users WHERE guild_id = ? AND user_id = ? AND var_name = ?", (guild_id, user_id, var_name)).fetchone()
        if result:
            return result[0]
        else:
            return False

    async def get_value_from_guild(self, guild_id: int, var_name: str):
        result = self.cursor.execute("SELECT var_value FROM users WHERE guild_id = ? AND var_name = ? AND user_id = ?", (guild_id, var_name, 0)).fetchone()
        if result:
            return result[0]
        else:
            return False

    async def get_value_from_user(self, user_id: int, var_name: str):
        result = self.cursor.execute("SELECT var_value FROM users WHERE user_id = ? AND var_name = ? AND guild_id = ?", (user_id, var_name, 0)).fetchone()
        if result:
            return result[0]
        else:
            return False

    async def set_global_var(self, var_name: str, var_value: str):
        if await self.get_global_var(var_name):
            self.cursor.execute("UPDATE users SET var_value = ? WHERE var_name = ?", (var_value, var_name))
        else:
            self.cursor.execute("INSERT INTO users(guild_id, user_id, var_name, var_value) VALUES(?, ?, ?, ?)", (0, 0, var_name, var_value))
        self.connection.commit()

    async def set_value_of_member(self, guild_id: str, user_id: str, var_name: str, var_value: str):
        if await self.get_value_from_member(guild_id, user_id, var_name):
            self.cursor.execute("UPDATE users SET var_value = ? WHERE var_name = ? AND guild_id = ? AND user_id = ?", (var_value, var_name, guild_id, user_id))
        else:
            self.cursor.execute("INSERT INTO users(guild_id, user_id, var_name, var_value) VALUES(?, ?, ?, ?)", (guild_id, user_id, var_name, var_value))
        self.connection.commit()

    async def set_value_of_guild(self, guild_id: str, var_name: str, var_value: str):
        if await self.get_value_from_guild(guild_id, var_name):
            self.cursor.execute("UPDATE users SET var_value = ? WHERE var_name = ? AND guild_id = ? AND user_id = ?", (var_value, var_name, guild_id, 0))
        else:
            self.cursor.execute("INSERT INTO users(guild_id, user_id, var_name, var_value) VALUES(?, ?, ?, ?)", (guild_id, 0, var_name, var_value))
        self.connection.commit()

    async def set_value_of_user(self, user_id: str, var_name: str, var_value: str):
        if await self.get_value_from_user(user_id, var_name):
            self.cursor.execute("UPDATE users SET var_value = ? WHERE var_name = ? AND guild_id = ? AND user_id = ?", (var_value, var_name, 0, user_id))
        else:
            self.cursor.execute("INSERT INTO users(guild_id, user_id, var_name, var_value) VALUES(?, ?, ?, ?)", (0, user_id, var_name, var_value))
        self.connection.commit()

class BDFDApp(CommandsHandler):
    def __init__(self, client: MZClient):
        self.client = client
        self.database = Database()
        self.all_funcs = [
            "$if",
            "$elif",
            "$else",
            "$stop",
            "$eval",

            "$sendmessage",
            "$message",
            "$addbutton",
            "$channelid",
            "$text",

            "$getvar",
            "$setvar",
            "$getmembervar",
            "$setmembervar",
            "$getguildvar",
            "$setguildvar",
            "$getuservar",
            "$setuservar",
            
            "$updatecommands",
            "$console"
        ]
        self.logic_funcs = ["$if", "$elif", "$else", "$endif"]
        self.no_arg_funcs = ["$else", "$channelid"]
        self.can_be_no_arg = ["$message", "$updateCommands"]

    async def func_console(self, ctx: disnake.message.Message = None, args: str = None):
        if args is None or len(args) == 0:
            return
        print(await self.is_have_commands(args, ctx))

    async def func_updatecommands(self, ctx: disnake.message.Message, args: str):
        await self.update_commands()

    async def func_getvar(self, ctx: disnake.message.Message, args: str):
        result = await self.is_have_commands(args, ctx)
        result = await self.database.get_global_var(result)
        if result:
            return result
        else:
            print(f"WARNING: Value for global var \"{args}\" not provided (returning empty string)")
            return ""

    async def func_setvar(self, ctx: disnake.message.Message, args: str):
        args_list = await self.get_args(args)
        count = 0
        for i in args_list:
            args_list[count] = await self.is_have_commands(i, ctx)
            count += 1
        if len(args_list) < 2:
            raise ValueError(f"$setVar needs 2 arguments, but only {len(args_list)} provided: \"{args}\"")
        await self.database.set_global_var(args_list[0], args_list[1])

    async def func_getmembervar(self, ctx: disnake.message.Message, args: str):
        args_list = await self.get_args(args)
        count = 0
        for i in args_list:
            args_list[count] = await self.is_have_commands(i, ctx)
            count += 1
        if len(args_list) < 1:
            raise ValueError(f"$getMemberVar needs 1 arguments, but only {len(args_list)} provided: \"{args}\"")
        if len(args_list) == 1:
            args_list.append(ctx.author.id)
        if len(args_list) == 2:
            args_list.append(ctx.guild.id)
        result = await self.database.get_value_from_member(args_list[2], args_list[1], args_list[0])
        if result:
            return result
        else:
            print(f"WARNING: Value for member var \"{args_list[0]}\" not provided (returning empty string)")
            return ""

    async def func_setmembervar(self, ctx: disnake.message.Message, args: str):
        args_list = await self.get_args(args)
        count = 0
        for i in args_list:
            args_list[count] = await self.is_have_commands(i, ctx)
            count += 1
        if len(args_list) < 2:
            raise ValueError(f"$setMemberVar needs 2 arguments, but only {len(args_list)} provided: \"{args}\"")
        if len(args_list) == 2:
            args_list.append(ctx.author.id)
        if len(args_list) == 3:
            args_list.append(ctx.guild.id)
        await self.database.set_value_of_member(args_list[3], args_list[2], args_list[0], args_list[1])

    async def func_getguildvar(self, ctx: disnake.message.Message, args: str):
        args_list = await self.get_args(args)
        count = 0
        for i in args_list:
            args_list[count] = await self.is_have_commands(i, ctx)
            count += 1
        if len(args_list) < 1:
            raise ValueError(f"$getGuildVar needs 1 arguments, but only {len(args_list)} provided: \"{args}\"")
        if len(args_list) == 1:
            args_list.append(ctx.guild.id)
        result = await self.database.get_value_from_guild(args_list[1], args_list[0])
        if result:
            return result
        else:
            print(f"WARNING: Value for guild var \"{args_list[0]}\" not provided (returning empty string)")
            return ""

    async def func_setguildvar(self, ctx: disnake.message.Message, args: str):
        args_list = await self.get_args(args)
        count = 0
        for i in args_list:
            args_list[count] = await self.is_have_commands(i, ctx)
            count += 1
        if len(args_list) < 2:
            raise ValueError(f"$setVar needs 2 arguments, but only {len(args_list)} provided: \"{args}\"")
        if len(args_list) == 2:
            args_list.append(ctx.guild.id)
        await self.database.set_value_of_guild(args_list[2], args_list[0], args_list[1])

    async def func_getuservar(self, ctx: disnake.message.Message, args: str):
        args_list = await self.get_args(args)
        count = 0
        for i in args_list:
            args_list[count] = await self.is_have_commands(i, ctx)
            count += 1
        if len(args_list) < 1:
            raise ValueError(f"$getUserVar needs 1 arguments, but only {len(args_list)} provided: \"{args}\"")
        if len(args_list) == 1:
            args_list.append(ctx.author.id)
        result = await self.database.get_value_from_user(args_list[1], args_list[0])
        if result:
            return result
        else:
            print(f"WARNING: Value for user var \"{args_list[0]}\" not provided (returning empty string)")
            return ""

    async def func_setuservar(self, ctx: disnake.message.Message, args: str):
        args_list = await self.get_args(args)
        count = 0
        for i in args_list:
            args_list[count] = await self.is_have_commands(i, ctx)
            count += 1
        if len(args_list) < 2:
            raise ValueError(f"$setUserVar needs 2 arguments, but only {len(args_list)} provided: \"{args}\"")
        if len(args_list) == 2:
            args_list.append(ctx.author.id)
        await self.database.set_value_of_user(args_list[2], args_list[0], args_list[1])

    async def func_message(self, ctx: disnake.message.Message, args: str = ""):
        if len(args) == 0:
            return ctx.content
        return ctx.content.split(" ")[int(args)]

    async def func_eval(self, ctx: disnake.message.Message, args: str): # its unstability function. try not use it
        chunks = await self.get_chunks(args)
        for i in chunks:
            if i.startswith("$"):
                args = await self.client.run_code(args, ctx)
                args = await self.client.run_code(args, ctx)
                return args
        else:
            return args

    async def func_if(self, ctx: disnake.message.Message, args: str):
        if args.lower() == "true":
            return True
        elif args.lower() == "false":
            return False
        choices = ["==", ">=", "<=", "!=", "<", ">"]
        operator_mapping = {
            "==": lambda x, y: x == y,
            "!=": lambda x, y: x != y,
            ">": lambda x, y: x > y,
            ">=": lambda x, y: x >= y,
            "<": lambda x, y: x < y,
            "<=": lambda x, y: x <= y,
        }
        for i in choices:
            if i in args:
                if i in ["==", "!="]:
                    vals = args.split(i)
                    val1 = vals[0].strip()
                    val2 = vals[1].strip()
                else:
                    vals = args.split(i)
                    val1 = int(vals[0])
                    val2 = int(vals[1])
                val1 = await self.is_have_commands(val1, ctx)
                val2 = await self.is_have_commands(val2, ctx)
                if operator_mapping.get(i, lambda x, y: None)(val1, val2):
                    return True
                else:
                    return False
        return False

    async def func_else(self, ctx: disnake.message.Message): # all $else function translated to $elif[True] for better output because he have brackets
        return "$elif[True]"

    async def func_stop(self, ctx: disnake.message.Message): # nvm, this function will be made in the future
        return "STOPIT"

    async def func_elif(self, ctx: disnake.message.Message, args: str): # return result from $if (DRY)
        return await self.func_if(ctx, args)

    async def func_addbutton(self, ctx: disnake.message.Message, args: str): # test and fun function
        print(f"addButton with args: {args}")
        return "penis is good"

    async def func_sendmessage(self, ctx: disnake.message.Message, args: str): # send message to provided channel or ctx
        try:
            args_list = await self.get_args(args)
            if len(args_list) == 2:
                channel = ctx.guild.get_channel(int(await self.is_have_commands(args_list[0])))
                if channel:
                    await channel.send(await self.is_have_commands(args_list[1], ctx))
                else:
                    raise SyntaxError(f"Can't find channel \"{args_list[0]}\"")
            elif len(args_list) == 1:
                result = await self.is_have_commands(args_list[0], ctx)
                await ctx.channel.send(result)
        except Exception as e:
            raise SyntaxError("$sendMessage: Cannot send empty message")

    async def func_channelid(self, ctx: disnake.message.Message):
        return ctx.channel.id

    async def func_text(self, ctx: disnake.message.Message, args: str):
        return args

class CommandsHandler(BDFDApp):
    def __init__(self, client: MZClient):
        super().__init__(client)
        self.funcs = {}
        for line in self.all_funcs:
            try:
                function = eval("self.func_"+line.replace("$", "").lower())
                self.funcs[line] = function
            except NameError as e:
                print(f"WARNING: for command \"{line}\" not exists function found.")

    async def is_have_commands(self, entry: str, ctx: disnake.message.Message = None):
        chunks = await self.get_chunks(entry)
        for i in chunks:
            if i.startswith("$"):
                return await self.execute_chunks(chunks, ctx)
        else:
            return entry

    async def update_commands(self):
        for i in self.client.exec_on_start:
            self.client.user_commands[i][0] = await self.is_have_commands(self.client.user_command_names[i], disnake.message.Message)

    async def get_args(self, entry: str, ctx: disnake.message.Message = None):
        """
        ## Gets args from function\n
        ### Example:\n
        #### Input `"$sendMessage[1234567890987654321;Hello World!]"`\n
        #### Output `["1234567890987654321", "Hello World!"]`
        """
        args_list = []
        brackets = 0
        while len(entry) > 0:
            brackets = 0
            addArg = ""
            for i in entry:
                addArg += i
                if i == "[":
                    brackets += 1
                elif i == "]":
                    brackets -= 1
                if i == ";" and brackets == 0:
                    args_list.append(addArg[:-1])
                    entry = entry[len(addArg):]
                    break
            else:
                args_list.append(addArg)
                break
        return args_list

    async def execute_function(self, entry: str, ctx: disnake.message.Message):
        """
        ## Execute function and return his result\n
        ### Example:\n
        #### Input `"$sendMessage[Hello World!]"`\n
        #### Output `"" (empty string)`
        It is because $sendMessage only send message.
        ### Example 2:\n
        #### Input `"$text[Hello World!]"`\n
        #### Output `"Hello World!"`
        """
        result = None
        splited = entry.split("[")
        try:
            if len(splited) > 1:
                if splited[0] in self.can_be_no_arg or splited[0] in self.logic_funcs:
                    result = await self.funcs[splited[0].lower()](ctx, "[".join(splited[1:])[:-1])
                else:
                    result = await self.funcs[splited[0].lower()](ctx, "[".join(splited[1:])[:-1])
            else:
                if splited[0] in self.no_arg_funcs or splited[0] in self.can_be_no_arg:
                    result = await self.funcs[splited[0].lower()](ctx)
        except:
            raise SyntaxError(f"Cant complete this function: {splited[0]}\n\nCheck that all parentheses are closed and that you are writed the function correctly.")
        if result:
            return result
        else:
            return ""

    async def check_ifs(self, chunks):
        """
        ## Check if all $if blocks closed or writed correctly\n
        ### Example:\n
        #### Input `"$if[$message[0]==hello] $sendMessage[Hello World!] $else $sendMessage[Bye bye]"`\n
        #### Output `(SyntaxError) The amount of $endif must be equal to the amount of $if`
        """
        ifs = 0
        elses = 0
        ends = 0
        for func in self.logic_funcs:
            for cmd in chunks:
                if cmd.startswith(func):
                    if func == "$if":
                        ifs += 1
                    elif func == "$elif":
                        if ifs == 0:
                            raise SyntaxError("$elif has been declared before $if")
                    elif func == "$else":
                        if ifs == 0:
                            raise SyntaxError("$else has been declared before $if")
                        elses += 1
                    elif func == "$endif":
                        if ifs == 0:
                            raise SyntaxError("$endif has been declared before $if")
                        ends += 1
        if ifs != ends:
            raise SyntaxError("The amount of $endif must be equal to the amount of $if")
        if ifs < elses:
            raise SyntaxError("The amount of $else must be equal or lower to the amount of $if")

    async def find_command(self, entry: str, chunks: list):
        """
        ## Return first find command in the entry\n
        ## and edit entry by deleting then command\n
        ### Example:\n
        #### Input `"$if[$message[0]==hello] $sendMessage[Hello World!] $else $sendMessage[Bye bye] $endif"`\n
        #### Output ` $sendMessage[Hello World!] $else $sendMessage[Bye bye] $endif`
        """
        addCommand = ""
        brackets = 0
        for i in entry:
            if i == "[":
                brackets += 1
            elif i == "]":
                brackets -= 1
                if brackets == 0:
                    chunks.append(addCommand+i)
                    return entry[len(addCommand):]
            elif addCommand+i in self.no_arg_funcs or addCommand+i in ["$stop", "$endif"] or (addCommand+i in self.can_be_no_arg and len(addCommand+i)==len(entry)):
                if addCommand+i == "$else":
                    chunks.append((addCommand+i).replace("$else", "$elif[True]"))
                else:
                    chunks.append(addCommand+i)
                return entry[len(addCommand):]
            addCommand += i

    async def get_chunks(self, entry: str):
        """
        ## Return all chunks of code by splitting it with $ and []\n
        ### Example:\n
        #### Input `"$if[$message[0]==hello] $sendMessage[Hello World!] $else $sendMessage[Bye bye] $endif"`\n
        #### Output `["$if[$message[0]==hello]", "$sendMessage[Hello World!]", "$else", "$sendMessage[Bye bye]", "$endif"]`
        """
        chunks = []
        checkCommands = True
        async def find_text():
            addText = ""
            for i in entry:
                if i == "$":
                    if len(addText) != 0 and addText != "\n":
                        chunks.append(addText)
                    return entry[len(addText):]
                addText += i
            else:
                if len(addText) == len(entry):
                    chunks.append(addText)
                    return entry[len(addText):]
                return entry[1:]
        while len(entry) > 0:
            checkCommands = True
            while checkCommands:
                entry = await find_text()
                if len(entry) == 0:
                    break
                if entry[0] == "$":
                    entry = await self.find_command(entry, chunks)
                    checkCommands = False
                if len(entry) != 0:
                    entry = entry[1:]
        return chunks

    async def find_endif(self, chunks: list):
        """
        ## Find and return index of $endif in the chunks(list) by check if all $if's closed\n
        ### Example:\n
        #### Input `"$if[$message[0]==hello] $sendMessage[Hello World!] $else $sendMessage[Bye bye] $endif"`\n
        #### Output `4 (index in the list)`
        """
        unclosedifs = 0
        counter = -1
        for i in chunks:
            counter += 1
            if i.startswith("$endif"):
                unclosedifs -= 1
                if unclosedifs == 0:
                    return counter
            elif i.startswith("$if"):
                unclosedifs += 1

    async def find_elif(self, chunks: list, main_if: tuple, main_endif: tuple, ctx: disnake.message.Message):
        """
        ## Return chunks(list) with executed $if condition. Delete $if block if it return False or delete $elif condition if $if return True.
        Replace $elif to $if if $if is False but $elif Found. If $elif not found but $if is True - all if block deleting.
        If $if return True but $elif not found - $if and $endif deleting from chunks(list).
        If $elif return False - all $if block from $if to $endif deleting.\n
        ### Example:\n
        #### Input `"$if[False] $sendMessage[Hello World!] $else $sendMessage[Bye bye] $endif"`\n
        #### Output `["$if[True]", "$sendMessage[Bye bye]", "$endif"]`
        """
        unclosedifs = 0
        this_count = -1
        return_chunks = chunks.copy()
        for i in chunks:
            this_count += 1
            if i.startswith("$if"):
                unclosedifs += 1
            elif i.startswith("$endif"):
                unclosedifs -= 1
            elif i.startswith("$elif"):
                if unclosedifs == 1:
                    main_elif = (await self.execute_function(i, ctx), this_count, ctx)
                    if main_if[0]:
                        return_chunks = chunks[:main_elif[1]] + chunks[main_endif+1:]
                        return_chunks.pop(main_if[1])
                    else:
                        return_chunks[main_elif[1]] = return_chunks[main_elif[1]].replace("$elif", "$if")
                        return_chunks = return_chunks[:main_if[1]] + return_chunks[main_elif[1]:]
                    return return_chunks
        else:
            if main_if[0]:
                return_chunks.pop(main_endif)
                return_chunks.pop(main_if[1])
            else:
                return_chunks = return_chunks[:main_if[1]] + return_chunks[main_endif+1:]
        return return_chunks

    async def execute_chunks(self, old_chunks, ctx: disnake.message.Message):
        """
        ## Execute all chunks\n
        ### Example:\n
        #### Input `"$if[$message[0]==hello] $sendMessage[Hello World!] $else $sendMessage[Bye bye] $endif"`\n
        #### Output `["$if[$message[0]==hello]", "$sendMessage[Hello World!]", "$else", "$sendMessage[Bye bye]", "$endif"]`
        """
        new_chunks = old_chunks.copy()
        while new_chunks:
            count = -1
            for chunk in new_chunks.copy():
                count += 1
                main_if = None
                main_endif = None
                if chunk.startswith("$if"):
                    main_if = (await self.execute_function(chunk, ctx), count)
                    main_endif = await self.find_endif(new_chunks)
                    new_chunks = await self.find_elif(new_chunks, main_if, main_endif, ctx)
                    break
                else:
                    for i in self.all_funcs:
                        if chunk.lower().startswith(i):
                            new_chunks[count] = await self.execute_function(chunk, ctx)
                            break
            else:
                break
        while new_chunks.count("") > 0:
            new_chunks.remove("")
        return "".join(new_chunks)

class MZClient:
    def __init__(self, intents: str = "all", on_ready: str = None):
        self.funcs = CommandsHandler(self)
        if intents.lower() == "all":
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
        self.bot.add_listener(self.on_ready, disnake.Event.ready)
        self.bot.add_listener(self.on_message, disnake.Event.message)

    async def run_code(self, code: str, ctx: disnake.message.Message = None):
        """
        ## Async run provided code

        #### Args:
            code (`str`): Code with functions (example: `$getVar[prefix]`, `$if[1==1] $text[text1] $else $text[text2] $endif`)
            ctx (`disnake.message.Message`): Context

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
        await self.funcs.update_commands()
        print("Bot ready for work")

    async def on_message(self, message: disnake.message.Message):
        if message.author == self.bot.user:
            return
        splited_command = message.content.split(" ")
        for i in self.user_commands:
            if splited_command[0] == i[0]:
                message.content = " ".join(splited_command[1:])
                # time1 = perf_counter()
                await self.run_code(i[1], message)
                # print(perf_counter()-time1)

    def run(self, token: str):
        self.bot.run(token)