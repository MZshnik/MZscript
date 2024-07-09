import disnake
import aiohttp

from ...functions_handler import FunctionsHandler


class FuncRequest(FunctionsHandler):
    def __init__(self, handler):
        super().__init__()
        self.handler = handler
        self.bot = handler.client.bot

    async def func_request(self, ctx: disnake.Message, args: str = None):
        """
        `$request[[post/get];url;(payload);(headers)]`
        """
        args_list = await self.get_args(await self.is_have_functions(args, ctx))
        if len(args_list) > 2 or len(args_list) == 0:
            error_msg = "$request: Too many or no args provided"
            if self.handler.debug_console:
                raise ValueError(error_msg)
            else:
                await ctx.channel.send(error_msg)
                return True

        method = args_list[0].lower()
        url = args_list[1]

        payload = {}
        headers = {}

        if len(args_list) > 2:
            try:
                payload = eval(args_list[2])
            except Exception as e:
                print(e)
                payload = {}

        if len(args_list) > 3:
            try:
                headers = eval(args_list[3])
            except Exception as e:
                print(e)
                headers = {}

        async with aiohttp.ClientSession() as session:
            if method == 'post':
                async with session.post(url, json=payload, headers=headers) as response:
                    params = {
                        'status': response.status,
                        'headers': response.headers,
                        'payload': payload,
                        'headers': headers,
                        'text': await response.text()
                    }
                    return str(params)
            elif method == 'get':
                async with session.get(url, headers=headers) as response:
                    params = {
                        'status': response.status,
                        'headers': response.headers,
                        'payload': payload,
                        'headers': headers,
                        'text': await response.text()
                    }
                    return str(params)
            else:
                error_msg = "$request: Unsupported method" # TODO: Добавить больше методов, щась лень :D
                if self.handler.debug_console:
                    raise ValueError(error_msg)
                else:
                    await ctx.channel.send(error_msg)
                    return True

def setup(handler):
    return FuncRequest(handler)
