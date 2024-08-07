import hashlib

import disnake

from ...functions_handler import FunctionsHandler


class Extras(FunctionsHandler):
    def __init__(self, handler):
        super().__init__()
        self.handler = handler
        self.bot = handler.client.bot

    async def func_hash(self, ctx: disnake.Message, args: str):
        """
        `$hash[text;(length;hash;salt)]`
        ### Example:
        `$hash[password1234]`
        """
        args_list = await self.get_args(await self.is_have_functions(args, ctx), ctx)
        if len(args_list) > 4 or len(args_list) == 0:
            raise ValueError("$hash: Too many or no args provided")

        text_to_hash = args_list[0].encode()
        hash_length = int(args_list[1]) if len(args_list) > 1 and len(args_list[1]) != 0 else 16
        salt = b"mzscript" if len(args_list) != 4 else args_list[3].encode()

        hash_type = "256" if len(args_list) < 3 or len(args_list[2]) == 0 else args_list[2]
        if hash_type not in ["128", "256"]:
            error_msg = f"$hash: Unsupported hash format \"{hash_type}\". Please, select 128 or 256"
            if self.handler.debug_console:
                raise ValueError(error_msg)
            else:
                await ctx.channel.send(error_msg)
                return True

        if hash_type == "256":
            return hashlib.shake_256(salt+text_to_hash).hexdigest(hash_length)
        else:
            return hashlib.shake_128(salt+text_to_hash).hexdigest(hash_length)

def setup(handler):
    return Extras(handler)