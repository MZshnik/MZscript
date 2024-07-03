import disnake

from ..functions_handler import FunctionsHandler


class Functions(FunctionsHandler):
    def __init__(self, handler):
        super().__init__()
        self.handler = handler
        self.bot = handler.client.bot

    async def func_if(self, ctx, args: str):
        """
        `$if[condition]`\n
        Compares 2 provided values between them
        ### Example:
        `$if[$userInfo[id]==700061502089986139]`
        """
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
                vals = args.split(i)
                if i in ["==", "!="]:
                    val1 = await self.is_have_functions(vals[0].strip(), ctx)
                    val2 = await self.is_have_functions(vals[1].strip(), ctx)
                else:
                    val1 = int(await self.is_have_functions(vals[0], ctx))
                    val2 = int(await self.is_have_functions(vals[1], ctx))
                return operator_mapping.get(i, lambda x, y: None)(val1, val2)
        return False

    async def func_elif(self, ctx, args: str): # return result from $if (DRY)
        """
        `$elif[condition]`\n
        Copy of $if
        ### Example:
        `$elif[$message[0]==hello]`
        """
        return await self.func_if(ctx, args)

    async def func_else(self, ctx): # all $else function translated to $elif[true] for better output because he have brackets
        """
        `$else`\n
        No args. Copy of $elif[true]
        ### Example:
        `$if[$message==hello] $sendMessage[Hello!] $else $sendMessage[Password?] $endif`
        """
        return "$elif[true]"

    async def func_stop(self, ctx):
        return True

    async def func_eval(self, ctx, args: str): # its unstability function. try not use it
        """
        `$eval[code to eval]`\n
        Execute provided code
        ### Example:
        `$eval[$sendMessage[$message]]`
        """
        chunks = await self.get_chunks(args)
        for i in chunks:
            if i.startswith("$"):
                args = await self.handler.client.run_code(args, ctx)
                return await self.handler.client.run_code(args, ctx)
        else:
            return args

    async def func_pyeval(self, ctx, args: str):
        command = """for i in args:
    for j in i:
        globals()[j] = i[j]\n"""
        command = "\n".join(["    "+i for i in (command+await self.is_have_functions(args, ctx)).split("\n")])
        command = "async def __ex(args):\n"+command
        exec(command, globals(), locals())
        result = await locals()["__ex"]((globals(), locals()))
        return result if result else ""

def setup(handler):
    return Functions(handler)