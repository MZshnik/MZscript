# this is example of plugin creating, maded by vanezus <3

# Use quart - this async flask
from quart import Quart, jsonify
# need for types
from disnake.ext import commands


class WebsitePlugin: #name
    # init, there is code of plugin
    def __init__(self):
        # quart 
        self.app = Quart(__name__)
        #route /
        @self.app.route('/')
        async def exm(): # ASYNC
            return jsonify({"bot": self.bot.user.display_name}) # -> return bot display name
    # self.bot declaration
    def setup(self, bot):
        self.bot: commands.InteractionBot = bot
    # there is async starting of server
    async def run(self):
        await self.app.run_task(host='0.0.0.0', port=5000)
    # On bot and website ready
    async def on_ready(self):
        print(True)


# example of add:
# from website.py import WebsitePlugin
# # end of file
# bot.add_plugin(WebsitePlugin())
