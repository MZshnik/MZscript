from MZscript import MZClient

def setup(client: MZClient):
    client.add_command(
    name="!command",
    code="""
    $sendMessage[Hello!]
    """)