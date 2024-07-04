class FunctionsHandler:
    """
    ## Main class for handlering functions like $if, $sendMessage, $console and etc.
    #### Check docs for better explaining what you need to do if you want add command
    """
    def __init__(self):
        # every function from this list need to have same self.func_functionname, else - warning in console
        self.all_funcs = [
            "$if",
            "$elif",
            "$else",
            "$stop",
            "$eval",
            "$pyeval",
            # info
            "$guildinfo",
            "$channelinfo",
            "$roleinfo",
            "$userinfo",
            "$hasrole",
            # checks
            "$ismemberexists",
            "$isroleexists",
            "$isuserexists",
            "$isguildexists",
            "$isnumber",
            # messages
            "$sendmessage",
            "$editmessage",
            "$message",
            "$addreaction",
            # moderation
            "$ban",
            "$unban",
            "$kick",
            # text
            "$text",
            "$replacetext",
            "$lowercase",
            "$uppercase",
            "$titlecase",
            # interactions
            "$customid",
            "$value",
            "$options",
            "$defer",
            # variables
            "$var",
            "$getvar",
            "$setvar",
            "$delvar",
            "$getmembervar",
            "$setmembervar",
            "$delmembervar",
            "$getguildvar",
            "$setguildvar",
            "$delguildvar",
            "$getuservar",
            "$setuservar",
            "$deluservar",
            # other
            "$calculate",
            "$loop",
            "$updatecommands",
            "$docs",
            "$console"
        ]
        # dont touch this list
        self.logic_funcs = ["$if", "$elif", "$else", "$endif"]
        # add if func dont want to get args with []
        self.no_arg_funcs = ["$else", "$stop", "$customid", "$defer"]
        # if func can be on arg or with args - add it here
        self.can_be_no_arg = ["$message", "$updatecommands", "$value"]
        # dict. with func names and func_<func-name> methods, generated automaticly
        self.funcs = {}

    def sync_functions(self, functions: dict):
        """
        ## Sync functions from FunctionCore original class
        By default `self.funcs` is empty, and all function generated in main class FunctionCore.
        After FunctionCore generate it, for i in FunctionsHandler copys invoke this methode with dictinary
        """
        self.funcs = functions

    async def check_ifs(self, chunks: list):
        """
        ## Check if all $if blocks closed or writed correctly
        ### Example:
        ### Input `"$if[$message[0]==hello] $sendMessage[Hello World!] $else $sendMessage[Bye bye]"`
        ### Output `(SyntaxError) The amount of $endif must be equal to the amount of $if`
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

    async def get_args(self, entry: str, ctx = None): # ctx not needed but many entrys what provide ctx
        """
        ## Gets args from function
        ### Example:
        ### Input `"1234567890987654321;Hello World!"`
        ### Output `["1234567890987654321", "Hello World!"]`
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

    async def execute_function(self, entry: str, ctx):
        """
        ## Execute function and return his result
        ### Example:
        ### Input `"$sendMessage[Hello World!]"`
        ### Output `"" (empty string)`
        It is because $sendMessage only send message.
        ### Example 2:
        ### Input `"$text[Hello World!]"`
        ### Output `"Hello World!"`
        """
        result = None
        splitted = entry.split("[")
        try:
            if len(splitted) > 1:
                if splitted[0].lower() in self.can_be_no_arg or splitted[0].lower() in self.logic_funcs:
                    result = await self.funcs[splitted[0].lower()](ctx, "[".join(splitted[1:])[:-1])
                else:
                    result = await self.funcs[splitted[0].lower()](ctx, "[".join(splitted[1:])[:-1])
            else:
                if splitted[0].lower() in self.no_arg_funcs or splitted[0].lower() in self.can_be_no_arg:
                    result = await self.funcs[splitted[0].lower()](ctx)
        except:
            raise SyntaxError(f"Cant complete this function: {splitted[0]}\n\nCheck that all parentheses are closed and that you are writed the function correctly. Most useful message in top of error.")
        if result:
            return result
        return ""

    async def finds_function(self, entry: str, chunks: list):
        """
        ## Return first find command in the entry
        ## and edit entry by deleting then command
        ### Example:
        ### Input `"$if[$message[0]==hello] $sendMessage[Hello World!] $else $sendMessage[Bye bye] $endif"`
        ### Output ` $sendMessage[Hello World!] $else $sendMessage[Bye bye] $endif`
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
            elif (addCommand+i).lower() in self.no_arg_funcs or (addCommand+i).lower() in ["$stop", "$endif"] or ((addCommand+i).lower() in self.can_be_no_arg and len(addCommand+i)==len(entry)):
                if (addCommand+i).lower() == "$else":
                    chunks.append((addCommand+i).replace("$else", "$elif[True]"))
                else:
                    chunks.append(addCommand+i)
                return entry[len(addCommand):]
            elif (addCommand).lower() in self.can_be_no_arg and i==";" and brackets == 0:
                chunks.append(addCommand)
                return entry[len(addCommand)-1:]
            addCommand += i

    async def get_chunks(self, entry: str):
        """
        ## Return all chunks of code by splitting it with $ and []
        ### Example:
        ### Input `"$if[$message[0]==hello] $sendMessage[Hello World!] $else $sendMessage[Bye bye] $endif"`
        ### Output `["$if[$message[0]==hello]", "$sendMessage[Hello World!]", "$else", "$sendMessage[Bye bye]", "$endif"]`
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
                    entry = await self.finds_function(entry, chunks)
                    checkCommands = False
                if entry:
                    if len(entry) != 0:
                        entry = entry[1:]
                else:
                    return chunks
        return chunks

    async def finds_endif(self, chunks: list):
        """
        ## Find and return index of $endif in the chunks(list) by check if all $if's closed
        ### Example:
        ### Input `"$if[$message[0]==hello] $sendMessage[Hello World!] $else $sendMessage[Bye bye] $endif"`
        ### Output `4 (index in the list)`
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

    async def finds_elif(self, chunks: list, main_if: tuple, main_endif: tuple, ctx):
        """
        ## Return chunks(list) with executed $if condition.\n
        Delete $if block if it return False or delete $elif condition if $if return True.\n
        Replace $elif to $if if $if is False but $elif Found. If $elif not found but $if is True - all if block deleting.\n
        If $if return True but $elif not found - $if and $endif deleting from chunks(list).\n
        If $elif return False - all $if block from $if to $endif deleting.
        ### Example:
        ### Input `"$if[False] $sendMessage[Hello World!] $else $sendMessage[Bye bye] $endif"`
        ### Output `["$if[True]", "$sendMessage[Bye bye]", "$endif"]`
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

    async def execute_chunks(self, old_chunks, ctx):
        """
        ## Execute all chunks
        ### Example:
        ### Input `["$if[$message[0]==hello]", "$sendMessage[Hello World!]", "$else", "$sendMessage[Bye bye]", "$endif"]`
        ### Output `` (if $message[0] == hello send message "Hello World!")
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
                    main_endif = await self.finds_endif(new_chunks)
                    new_chunks = await self.finds_elif(new_chunks, main_if, main_endif, ctx)
                    break
                else:
                    for i in self.all_funcs:
                        if chunk.lower().startswith(i.lower()):
                            new_chunks[count] = await self.execute_function(chunk, ctx)
                            if new_chunks[count] != True:
                                break
                            # stop function if error. To create error - return True in function
                            new_chunks[count] = ""
                            del new_chunks[count-1:]
                            while new_chunks.count("") > 0:
                                new_chunks.remove("")
                            return "".join(new_chunks)
            else:
                break
        while new_chunks.count("") > 0:
            new_chunks.remove("")
        return "".join(new_chunks)

    async def exec_tags(self, chunks: list, tags: list):
        counter = len(chunks)
        for i in chunks.copy()[::-1]:
            counter -= 1
            for tag in tags.keys():
                if str(i).lower().startswith(tag.lower()):
                    await tags[tag](i[len(tag)+1:-1])
                    chunks.pop(counter)

    async def is_have_functions(self, entry: str, ctx = None):
        """
        ## Check if entry text has functions to execute.
        Usually used for execute arguments in functions like $sendMessage[$message] < $message is argument what will be executed
        ### Example:
        ### Input `"Hello, and $message!"`
        ### Output `"Hello, and welcome to the guild!"`
        """
        chunks = await self.get_chunks(entry)
        for i in chunks:
            if i.startswith("$"):
                return await self.execute_chunks(chunks, ctx)
        else:
            return entry