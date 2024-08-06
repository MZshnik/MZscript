
# this is example of plugin creating, maded by vanezus <3

# Use quart - this async flask
from quart import Quart, jsonify
# need for types
from src.MZscript import MZClient, BasePlugin


class WebsitePlugin(BasePlugin): # name of plugin
    def __init__(self):
        self.app = Quart(__name__)

        #route /
        @self.app.route("/")
        async def route_page():
            return jsonify({"bot": self.bot_name}) # -> return bot display name

    # simple add function
    async def func_myfunction(self, ctx, args):
        print("Hello!")

    # self.client declaration
    def setup(self, client):
        self.client: MZClient = client
        self.client.funcs.add_function("$myfunction", self.func_myfunction)

    # there is async starting of server
    # on bot ready
    async def on_ready(self):
        self.bot_name: str = self.client.bot.user.display_name
        await self.app.run_task(host='127.0.0.1', port=5000, debug=False)

# # example of add:
# from .website import WebsitePlugin
#
# bot.add_plugin(WebsitePlugin())
