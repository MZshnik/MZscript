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
        `$request[(get/post/put/delete);url;(payload;headers)]`
        ### Example:
        `$request[http://worldtimeapi.org/api/timezone/Europe/Moscow]`
        """
        args_list = await self.get_args(await self.is_have_functions(args, ctx))
        if len(args_list) > 4 or len(args_list) == 0:
            error_msg = "$request: Too many or no args provided"
            if self.handler.debug_console:
                raise ValueError(error_msg)
            else:
                await ctx.channel.send(error_msg)
                return True

        method = args_list[0].lower().strip()
        if len(args_list) > 1:
            if method not in ["get", "post", "put", "head", "options", "patch"]:
                error_msg = f"$request: Unknown methode \"{method}\""
                if self.handler.debug_console:
                    raise ValueError(error_msg)
                else:
                    await ctx.channel.send(error_msg)
                    return True
        else:
            args_list.insert(0, "get")
            method = args_list[0]

        url = args_list[1]

        payload = {}
        headers = {}

        if len(args_list) > 2:
            try:
                payload = eval(args_list[2])
                print("Payload")
                print(payload)
            except Exception as e:
                print(e)
                payload = {}

        if len(args_list) > 3:
            try:
                headers = eval(args_list[3])
                print("Headers")
                print(headers)
            except Exception as e:
                print(e)
                headers = {}

        async with aiohttp.ClientSession() as session:
            params = {}
            if method == "get":
                async with session.get(url, json=payload, headers=headers) as response:
                    params = {
                        'status': response.status,
                        'headers': response.headers,
                        'payload': payload,
                        'headers': headers,
                        'text': await response.text()
                        }
            elif method == "post":
                async with session.post(url, json=payload, headers=headers) as response:
                    params = {
                        'status': response.status,
                        'headers': response.headers,
                        'payload': payload,
                        'headers': headers,
                        'text': await response.text()
                        }
            elif method == "put":
                async with session.put(url, json=payload, headers=headers) as response:
                    params = {
                        'status': response.status,
                        'headers': response.headers,
                        'payload': payload,
                        'headers': headers,
                        'text': await response.text()
                        }
            elif method == "delete":
                async with session.delete(url, json=payload, headers=headers) as response:
                    params = {
                        'status': response.status,
                        'headers': response.headers,
                        'payload': payload,
                        'headers': headers,
                        'text': await response.text()
                        }
            else:
                error_msg = f"$request: Unsupported method \"{method}\"" # TODO: Add head, options and patch methods
                if self.handler.debug_console:
                    raise ValueError(error_msg)
                else:
                    await ctx.channel.send(error_msg)
                    return True

            if len(params) > 0:
                return str(params)
            else:
                return ""

def setup(handler):
    return FuncRequest(handler)
