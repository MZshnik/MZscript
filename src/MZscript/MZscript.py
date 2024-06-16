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

        ]
        self.logic_funcs = ["$if", "$elif", "$else", "$endif"]
        self.no_arg_funcs = ["$else", "$channelid"]
        self.can_be_no_arg = ["$message"]

    async def func_getvar(self, ctx: disnake.message.Message, args: str):
        result = await self.database.get_global_var(args)
        if result:
            return result
        else:
            print(f"WARNING: Value for global var \"{args}\" not provided (returning empty string)")
            return ""

    async def func_setvar(self, ctx: disnake.message.Message, args: str):
        args_list = await self.get_args(args)
        if len(args_list) < 2:
            raise ValueError(f"$setVar needs 2 arguments, but only {len(args_list)} provided: \"{args}\"")
        await self.database.set_global_var(args_list[0], args_list[1])

    async def func_getmembervar(self, ctx: disnake.message.Message, args: str):
        args_list = await self.get_args(args)
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
        if len(args_list) < 2:
            raise ValueError(f"$setMemberVar needs 2 arguments, but only {len(args_list)} provided: \"{args}\"")
        if len(args_list) == 2:
            args_list.append(ctx.author.id)
        if len(args_list) == 3:
            args_list.append(ctx.guild.id)
        await self.database.set_value_of_member(args_list[3], args_list[2], args_list[0], args_list[1])

    async def func_getguildvar(self, ctx: disnake.message.Message, args: str):
        args_list = await self.get_args(args)
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
        if len(args_list) < 2:
            raise ValueError(f"$setVar needs 2 arguments, but only {len(args_list)} provided: \"{args}\"")
        if len(args_list) == 2:
            args_list.append(ctx.guild.id)
        await self.database.set_value_of_guild(args_list[2], args_list[0], args_list[1])

    async def func_getuservar(self, ctx: disnake.message.Message, args: str):
        args_list = await self.get_args(args)
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
                if "$" in val1:
                    val1 = await self.client.run_code(val1, ctx)
                if "$" in val2:
                    val2 = await self.client.run_code(val2, ctx)
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
            splited = await self.get_args(args)
            if len(splited) == 2:
                channel = await ctx.guild.get_channel(int(splited[0]))
                if channel:
                    chunks = await self.get_chunks(splited[1:])
                    for i in chunks:
                        if i.startswith("$"):
                            await channel.send(await self.execute_chunks(chunks, ctx))
                            break
                    else:
                        await channel.send(splited[1:])
                else:
                    raise SyntaxError(f"Can't find channel \"{splited[0]}\"")
            elif len(splited) == 1:
                chunks = await self.get_chunks(splited[0])
                for i in chunks:
                    if i.startswith("$"):
                        await ctx.channel.send(await self.execute_chunks(chunks, ctx))
                        break
                else:
                    await ctx.channel.send(splited[0])
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

    async def find_endif(self, chunks):
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

    async def find_elif(self, chunks, main_if: tuple, main_endif: tuple, ctx: disnake.message.Message):
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
        self.user_commands = {}
        self.exec_on_start = []
        self.bot = commands.InteractionBot(intents=intents)
        self.bot.add_listener(self.on_ready, disnake.Event.ready)
        self.bot.add_listener(self.on_message, disnake.Event.message)

    async def run_code(self, code, ctx: disnake.message.Message):
        chunks = await self.funcs.get_chunks(code)
        await self.funcs.check_ifs(chunks)
        chunks = await self.funcs.execute_chunks(chunks, ctx)
        if chunks or len(chunks) > 0:
            return "".join(chunks)
        return "" 

    def add_command(self, name: str, code: str):
        self.user_commands[name] = code
        chunks = asyncio.run(self.funcs.get_chunks(name))
        for i in chunks:
            if i.startswith("$"):
                self.exec_on_start.append(name)

    async def on_ready(self):
        if self.user_on_ready:
            await self.run_code(self.user_on_ready)
        for i in self.exec_on_start:
            self.user_commands[await self.run_code(i, disnake.message.Message)] = self.user_commands.pop(i)
        print("Bot ready for work")

    async def on_message(self, message: disnake.message.Message):
        if message.author == self.bot.user:
            return
        splited_command = message.content.split(" ")
        for i in self.user_commands.keys():
            if splited_command[0] == i:
                message.content = " ".join(splited_command[1:])
                # time1 = perf_counter()
                await self.run_code(self.user_commands[i], message)
                # print(perf_counter()-time1)

    def run(self, token: str):
        self.bot.run(token)