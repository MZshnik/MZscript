import logging

from MZscript import BasePlugin, MZClient
from quart import Quart, jsonify, render_template, redirect, request


class Dashboard(BasePlugin):
    def __init__(self):
        self.client: MZClient = None
        self.app = Quart(__name__, static_url_path="/static")

        @self.app.route("/")
        async def route_page():
            events = [[event, self.client.user_events[event]] for event in self.client.user_events if self.client.user_events[event]]
            commands = self.client.user_commands
            if len(self.client.user_commands) == 0:
                commands = [["None", ""]]

            if len(events) == 0:
                events = [["None", ""]]
            return await render_template(
                "index.html",
                commands=commands,
                events=events
                )

        @self.app.route("/create-command")
        async def create_command_page():
            return await render_template(
                "newcode.html",
                code="Command"
                )

        @self.app.route("/create-event")
        async def create_event_page():
            return await render_template(
                "newcode.html",
                code="Event"
                )

        @self.app.post("/api/create-code")
        async def create_code():
            content = await request.json
            if content["type"] == "command":
                self.client.add_command(content["name"], content["code"])
            else:
                self.client.add_event(content["name"], content["code"])
            return Quart.response_class()

        @self.app.get("/edit-code")
        async def edit_code_page():
            return await render_template(
                "editcode.html",
                name=request.args.get("name"),
                code=request.args.get("code"),
                type=request.args.get("type")
                )

        @self.app.post("/api/edit-code")
        async def edit_code():
            content = await request.json
            if content["type"] == "command":
                self.client.edit_command(content["name"], content["code"])
            else:
                self.client.edit_event(content["name"], content["code"])
            return Quart.response_class()

    def setup(self, client: MZClient):
        self.client = client

    async def on_ready(self):
        logging.getLogger('hypercorn.access').disabled = True
        await self.app.run_task(host='127.0.0.1', port=5000, debug=False)