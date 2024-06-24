import disnake

from MZscript.functions_handler import FunctionsHandler


class Functions(FunctionsHandler):
    def __init__(self, handler):
        super().__init__()
        self.client = handler.client
        self.bot = handler.client.bot

    async def func_if(self, ctx, args: str):
        """
        $if[condition]
        Example:
        $if[$userInfo[id]==700061502089986139]"""
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
                    val1 = vals[0].strip()
                    val2 = vals[1].strip()
                else:
                    val1 = int(vals[0])
                    val2 = int(vals[1])
                val1 = await self.is_have_functions(val1, ctx)
                val2 = await self.is_have_functions(val2, ctx)
                return operator_mapping.get(i, lambda x, y: None)(val1, val2)
        return False

    async def func_elif(self, ctx, args: str): # return result from $if (DRY)
        """
        $elif[condition]
        Example:
        $elif[$message[0]==hello]
        """
        return await self.func_if(ctx, args)

    async def func_else(self, ctx): # all $else function translated to $elif[True] for better output because he have brackets
        "No args"
        return "$elif[True]"

    async def func_eval(self, ctx, args: str): # its unstability function. try not use it
        """
        $eval[code to eval]
        Example:
        $eval[$message]
        """
        chunks = await self.get_chunks(args)
        for i in chunks:
            if i.startswith("$"):
                args = await self.client.run_code(args, ctx)
                return await self.client.run_code(args, ctx)
        else:
            return args

def setup(handler):
    return Functions(handler)