class FunctionsHandler:
    """
    ## Main class for handling functions like $if, $sendMessage, $console and etc.
    #### Check docs for better explaining what you need to do if you want to add a command
    """
    def __init__(self):
        # every function from this list needs to have the same self.func_functionname, else - warning in console
        self.all_funcs = [
            "$if", "$elif", "$else", "$stop", "$eval", "$pyeval",
            # info
            "$guildinfo", "$channelinfo", "$roleinfo", "$userinfo", "$hasrole",
            # checks
            "$ismemberexists", "$isroleexists", "$isuserexists", "$isguildexists", "$isnumber",
            # messages
            "$sendmessage", "$editmessage", "$message", "$addreaction",
            # administration
            "$addrole", "$removerole",
            # moderation
            "$ban", "$unban", "$kick",
            # text
            "$text", "$replacetext", "$lowercase", "$uppercase", "$titlecase",
            # interactions
            "$customid", "$value", "$options", "$defer",
            # variables
            "$var", "$getvar", "$setvar", "$delvar", "$getmembervar", "$setmembervar", "$delmembervar",
            "$getguildvar", "$setguildvar", "$delguildvar", "$getuservar", "$setuservar", "$deluservar",
            # other
            "$calculate", "$loop", "$updatecommands", "$docs", "$console"
        ]
        # don't touch this list
        self.logic_funcs = ["$if", "$elif", "$else", "$endif"]
        # add if func don't want to get args with []
        self.no_arg_funcs = ["$else", "$stop", "$customid", "$defer"]
        # if func can be on arg or with args - add it here
        self.can_be_no_arg = ["$message", "$updatecommands", "$value"]
        # dict. with func names and func_<func-name> methods, generated automatically
        self.funcs = {}

    def sync_functions(self, functions: dict):
        """
        ## Sync functions from FunctionCore original class
        By default `self.funcs` is empty, and all functions are generated in the main class FunctionCore.
        After FunctionCore generates it, FunctionsHandler copies invoke this method with the dictionary.
        """
        self.funcs = functions

    async def check_ifs(self, chunks: list):
        """
        ## Check if all $if blocks are closed or written correctly
        ### Example:
        ### Input `"$if[$message[0]==hello] $sendMessage[Hello World!] $else $sendMessage[Bye bye]"`
        ### Output `(SyntaxError) The amount of $endif must be equal to the amount of $if`
        """
        ifs = 0
        elses = 0
        ends = 0
        for cmd in chunks:
            for func in self.logic_funcs:
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
                    break
        if ifs != ends:
            raise SyntaxError("The amount of $endif must be equal to the amount of $if")
        if ifs < elses:
            raise SyntaxError("The amount of $else must be equal or lower to the amount of $if")

    async def get_args(self, entry: str, ctx = None):  # ctx not needed but many entries provide ctx
        """
        ## Gets args from function
        ### Example:
        ### Input `"1234567890987654321;Hello World!"`
        ### Output `["1234567890987654321", "Hello World!"]`
        """
        args_list = []
        while len(entry) > 0:
            add_arg = ""
            brackets = 0
            for i in entry:
                add_arg += i
                if i == "[":
                    brackets += 1
                elif i == "]":
                    brackets -= 1
                if i == ";" and brackets == 0:
                    args_list.append(add_arg[:-1])
                    entry = entry[len(add_arg):]
                    break
            else:
                args_list.append(add_arg)
                break
        return args_list

    async def execute_function(self, entry: str, ctx):
        """
        ## Execute function and return its result
        ### Example:
        ### Input `"$sendMessage[Hello World!]"`
        ### Output `"" (empty string)`
        It is because $sendMessage only sends a message.
        ### Example 2:
        ### Input `"$text[Hello World!]"`
        ### Output `"Hello World!"`
        """
        result = None
        splitted = entry.split("[")
        try:
            func_name = splitted[0].lower()
            if len(splitted) > 1:
                if func_name in self.can_be_no_arg or func_name in self.logic_funcs:
                    result = await self.funcs[func_name](ctx, "[".join(splitted[1:])[:-1])
                else:
                    result = await self.funcs[func_name](ctx, "[".join(splitted[1:])[:-1])
            else:
                if func_name in self.no_arg_funcs or func_name in self.can_be_no_arg:
                    result = await self.funcs[func_name](ctx)
        except Exception as e:
            raise SyntaxError(f"Can't complete this function: {func_name}\n\nCheck that all parentheses are closed and that you have written the function correctly. Error: {e}")
        return result if result else ""

    async def finds_function(self, entry: str, chunks: list):
        """
        ## Return first find command in the entry
        ## and edit entry by deleting then command
        ### Example:
        ### Input `"$if[$message[0]==hello] $sendMessage[Hello World!] $else $sendMessage[Bye bye] $endif"`
        ### Output ` $sendMessage[Hello World!] $else $sendMessage[Bye bye] $endif`
        """
        add_command = ""
        brackets = 0
        for i in entry:
            if i == "[":
                brackets += 1
            elif i == "]":
                brackets -= 1
                if brackets == 0:
                    chunks.append(add_command + i)
                    return entry[len(add_command):]
            elif (add_command + i).lower() in self.no_arg_funcs or (add_command + i).lower() in ["$stop", "$endif"] or ((add_command + i).lower() in self.can_be_no_arg and len(add_command + i) == len(entry)):
                if (add_command + i).lower() == "$else":
                    chunks.append((add_command + i).replace("$else", "$elif[true]"))
                else:
                    chunks.append(add_command + i)
                return entry[len(add_command):]
            elif (add_command).lower() in self.can_be_no_arg and i == ";" and brackets == 0:
                chunks.append(add_command)
                return entry[len(add_command) - 1:]
            add_command += i

    async def get_chunks(self, entry: str):
        """
        ## Split entry for functions
        ### Example:
        ### Input `"$if[$message[0]==hello] $sendMessage[Hello World!] $else $sendMessage[Bye bye] $endif"`
        ### Output `["$if[$message[0]==hello]", "$sendMessage[Hello World!]", "$elif[true]", "$sendMessage[Bye bye]", "$endif"]`
        """
        chunks = []
        while len(entry) > 0:
            entry = await self.finds_function(entry, chunks)
        return chunks

    async def execute(self, entry: str, ctx):
        """
        ## Main executor
        ## Getting functions and exec it all
        ## Special for function-calling
        ### Example:
        ### Input `"$if[$message[0]==hello] $sendMessage[Hello World!] $else $sendMessage[Bye bye] $endif"`
        ### Output `"" (empty string)`
        It is because $sendMessage only sends a message.
        """
        chunks = await self.get_chunks(entry)
        await self.check_ifs(chunks)
        results = []
        for chunk in chunks:
            results.append(await self.execute_function(chunk, ctx))
        return "".join(results)
