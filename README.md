# MZscript
## Improved BDFD interpreter in Python
### [Documentation](/docs/DOCS.md)
#### [Docs site](https://mzscript.vercel.app)
### [Contribution](/docs/CONTRIBUTING.md)
#### Works on (tested) Python 3.10 and newer
## Instaling💻
```
pip install git+https://github.com/MZshnik/MZscript
```
## Updating📥
```
pip install --upgrade git+https://github.com/MZshnik/MZscript
```

## First steps🎉
#### Create your first command:
```py
from MZscript import MZClient

bot = MZClient()

bot.add_command(name="!help", code="""
$sendMessage[
Whats up?
!moderation
!info
!economy]
""")

bot.run("your bot token")
```
#### Try $if blocks:
```py
bot.add_command(name="!help", code="""
$sendMessage[
Choose menu:
$if[$message[0]==mod]
You choose moderation
$elif[$message[0]==mod]
You choose info
$elif[$message[0]==mod]
You choose economy
$else
!help moderation
!help info
!help economy
$endif]
""")
```
#### Change prefix with variables:
```py
# insert code in to on_ready is necessary
bot = MZClient(on_ready="""
$if[$getVar[prefix]==]
$setVar[prefix;!]
$endif
$console[Bot is ready]
""")

bot.add_command(name="$getVar[prefix]set-prefix", code="""
$if[$message[0]==]
$setVar[prefix;$message[0]]
$sendMessage[Prefix setted to "$message[0]"]
$updateCommands[] <-- update command names
$else
$sendMessage[Type some prefix, like: !, ?, #...]
$endif
""")

bot.add_command(name="$getVar[prefix]get-prefix", code="""
$if[$getVar[prefix]==]
$setVar[prefix;!] <-- default prefix
$endif
$sendMessage[Prefix is "$getVar[prefix]"]
""")

bot.add_command(name="$getVar[prefix]help", code="""
$sendMessage[
$getVar[prefix]help moderation
$getVar[prefix]help info
$getVar[prefix]help economy
]""")
```
#### Create buttons with events
```py
bot.add_command(name="!button", code="""
$sendMessage[
Content;Title;Description;footer;;0058CF;;;;; <-- embed args
;#addButton[primary;Amogus;False;amogus] <-- embed tags
;#addField[Amogus;Click me] <-- another tag
]""")

bot.add_event(name="button", code="""
$defer <-- defer button response
$if[$customID==amogus]
$sendMessage[New amogus in $channelInfo[name]]
$else
$console[Button "$customID" dosnot set]
$endif
""")
```
#### Make lvl system:
```py
bot.add_command(name="!lvl", code="""
$if[$getUserVar[lvl]==]
$setUserVar[lvl;1]
$endif
$sendMessage[Your lvl: $getUserVar[lvl]($getUserVar[exp]/100 xp to lvl up)]""")

bot.add_event(name="message", code="""
$if[$getUserVar[lvl]==]
$setUserVar[lvl;1]
$endif
$if[$getUserVar[exp]==]
$setUserVar[exp;0]
$endif
$setUserVar[exp;$calculate[$getUserVar[exp]+2]]
$if[$calculate[$getUserVar[exp]/100]==1]
$setUserVar[lvl;$calculate[$getUserVar[lvl]+1]]
$endif
""")
```

#### List of all functions
| Function        | Full support | No args | Can be no/with args |
| :-------------- |------------: | :-: | :- |
|$if|+|-|-
|$elif|+|-|-
|$else|+|+|-
|$stop|+|+|-
|$endif|+|+|-
|$eval|-|-|-
|$guildInfo|+|-|-
|$channelInfo|+|-|-
|$roleInfo|+|-|-
|$userInfo|+|-|-
|$hasRole|+|-|-
|$isMemberExists|+|-|-
|$isRoleExists|+|-|-
|$isUserExists|+|-|-
|$isGuildExists|+|-|-
|$isNumber|+|-|-
|$sendMessage|+|-|-
|$addReaction|+|-|-
|$message|+|-|-
|$text|+|-|-
|$replaceText|+|-|-
|$ban|+|-|-
|$unban|+|-|-
|$kick|+|-|-
|$lowerCase|+|-|-
|$upperCase|+|-|-
|$titleCase|+|-|-
|$customID|+|+|-
|$defer|+|+|-
|$var|+|-|-
|$getVar|+|-|-
|$setVar|+|-|-
|$delVar|+|-|-
|$getMemberVar|+|-|-
|$setMemberVar|+|-|-
|$delMemberVar|+|-|-
|$gelGuildVar|+|-|-
|$setGuildVar|+|-|-
|$delGuildVar|+|-|-
|$getUserVar|+|-|-
|$setUserVar|+|-|-
|$delUserVar|+|-|-
|$updateCommands|+|-|+
|$calculate|+|-|-
|$console|+|-|-
> Full support means is function 100% works/tested
#### List of functions tags:
| Function | Tags |
| -------- | ---- |
|$sendMessage | #addButton, #addField, #addReaction |
#### List of events:
| Name | Description |
| -------- | ---- |
|message | Activated when anyone send message |
|button | Activated when anyone press button from bot |
## In Developing🔨
- More functions from BDFD
- More custom functions
- Documentation
- Сontributing
## In the Future🚀
- Most usefull $eval
- $pyeval
- Support of mods

#### Repository and first lines of code by [MZshnik](https://github.com/MZshnik)
