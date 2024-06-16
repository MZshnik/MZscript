from MZscript import MZClient # import MZClinet - main class for create bot

bot = MZClient() # init class

# add new command with trigger !help
bot.add_command(name="!help", code="""
$sendMessage[Hello World!]
""")

# start your bot with your token
bot.run("your bot token")