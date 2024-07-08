# Welcome to documentation!
## Lets start with main functions:
- ### $if[conditione]
All conditions created with this function. You can use this operators:
| Less/More | then | Equal/not |
| ---------: | :----: | :--------- |
| <         | <=   | ==        |
| >         | >=   | !=        |
#### Logical operators or what $if returns
1. `True` - if condition is right
2. `False` - if condition is lie

#### Example:
`$if[1>2]` - return False because 1 not more then 2  
`$if[1<2]` - return True because 1 less then 2  
`$if[2==2]` - return True because 2 is equal 2  
`$if[Hello!=2]` - return True because "Hello" is not 2  
etc. 

- ### $elif
> $else but with conditione like $if
- ### $else
$else uses for say to code what if $if return False, we go to block of $else. You dont see, but $else is $elif[true] in the library code. If $if return True - code from block $else to $endif disappear. It is works with $elif but if $elif return False - all block from $if to $endif disappears. 
- ### $endif
Needs for end $if block. If you write $if - you need to write after him $endif. Its necessary.

## Good job! We go next - creating I/O commands.
Main thing what you need to think - plane text not sends. You need to write $sendMessage for sending message.
### And not less important - creating commands:
> dont miss to install last version by
> `pip install --update git+https://github.com/MZshnik/MZscript`  

First all, you need to import library
```py
from MZscript import MZClient
```
Now, init a main class MZClient
```py
bot = MZClient()
```
Good work, lets do first command
```py
bot.add_command(name="!help", code="""
$sendMessage[Hello World!]
""")
```
So, run the bot
```py
bot.run("your bot token")
```
Final code will looks like:
```py
from MZscript import MZClient

bot = MZClient()

bot.add_command(name="!help", code="""
$sendMessage[Hello World!]
""")

bot.run("your bot token")
```

Now you can `python main.py` or run your code or file how you want or can.  
You can test your first command by typing `!help` in the channel where bot can send and view messages.  
By default, MZClient uses all the intents that discord bots have, but you can configure it like this:
```py
bot = MZClient(intents="all") # best way is not set intents
```
Or just set intents how you want or need:)
```py
from disnake import Intents
intents = Intents.all()
intents.members = False # not recomened
bot = MZClient(intents=intents)
```
## Lets talk about commands
All commands invoked when user type same name of command in the chat. But, if you want to invoke command when somebody send message, just use events:
```py
bot.add_event(name="message", code="""
$sendMessage[Use send message? I too!]
""")
```
### [For commands you can use all this functions](/README.md?tab=readme-ov-file#list-of-all-functions)
> Remember, more functions will be added in time

About some functions:
- $text[some text] - wrap all text in it and return back. You can past commands or some content what you want to not process.
- $message - return all author message if you dont specify arguments (just $message). If you want to get first argument - $message[0], if second - $message[1] and etc.
- $channelID - return id of channel where command was invoked
> I think now a lot of functions is not usable, but later will change
### [Functions tags](/README.md?tab=readme-ov-file#list-of-functions-tags)
Tags is some under settings to function. They are provided after all arguments of function.
Now we have more than 3 in only 1 function, this is a description:
- #addButton - adds button to $sendMessage, args: `style, label, is disabled, customID, url, emoji, row`
- #addField - adds field to embed in $sendMessage, args: `name, value, is inline`
- #addReaction - adds reaction to message, args: `channel, message, emoji`
More tags for functions will be added soon
### [Events](/README.md?tab=readme-ov-file#list-of-events)
Events is more important thing in bot developering. You can add event in your code easily:
```py
bot.add_event(name="message", code="""
$console[Some guy send message in $channelInfo[name]]
"""
```
> It is worth saying that some events used by library by default. You can edit events in lib code if you want to control events by self
### Load commands (or "Cogs" / export module)
If you dont want write all commands in one file, use `bot.load_command(path)` or `bot.load_commands(dir)`, this is example of loaded file:
```py
from MZscript import MZClient
# import and set client argument to MZClient is not nessecary
def setup(client: MZClient):
    client.add_command(
    name="!command",
    code="""
$sendMessage[Hello!]
""")

    client.add_command(
    name="!command2",
    code="""
$sendMessage[Hello 2!]
""")
```
Example loading from path, test bot folder:  
/MyBot  
//Commands  
///command.py  
///another.py  
//main.py

#### Loading with `bot.load_command`
```py
# in main.py file in your folder
bot.load_command("Commands.command")
```
Load only provided file path
#### Loading with `bot.load_commands`
```py
bot.load_commands("Commands")
```
Load provided directory of files
## Now what about contributing?
View [this](/docs/CONTRIBUTING.md) file what describes what you need to contributing and made your own functions and events or modify library.