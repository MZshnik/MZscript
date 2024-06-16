# MZscript
## Improved BDFD interpreter in Python
#### Supporting Python 3.8 and newer
## Instaling💻
```
pip install git+https://github.com/MZshnik/MZscript
```
## Updating📥
```
pip install --update git+https://github.com/MZshnik/MZscript
```

## First step🎉
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

bot.run("your but token")
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
#### Use variables:
```py
bot.add_command(name="!set-prefix", code="""
$setVar[prefix;$message[0]]
$sendMessage[Prefix setted to "$message[0]"]
""")

bot.add_command(name="!get-prefix", code="""
$sendMessage[Prefix is "$getVar[prefix]"]
""")

bot.add_command(name="$getVar[prefix]help", code="""
$sendMessage[
$getVar[prefix]help moderation
$getVar[prefix]help info
$getVar[prefix]help economy
]""")
```

#### List of all functions
| Function        | Full support | No args | Can be no/with args |
| :-------------- |------------: | :-: | :- |
|$if|+|-|-
|$elif|+|-|-
|$else|+|+|-
|$endif|-|+|-
|$stop|-|+|-
|$eval|-|-|-
|$sendMessage|+|-|-
|$message|+|-|-
|$addButton|-|-|-
|$channelID|+|+|-
|$text|+|-|-
|$getVar|+|-|-
|$setVar|+|-|-
|$getMemberVar|+|-|-
|$setMemberVar|+|-|-
|$getGuildVar|+|-|-
|$setGuildVar|+|-|-
|$getUserVar|+|-|-
|$setUserVar|+|-|-
## In Developing🔨
- More functions from BDFD
- More custom functions
- Documentation
## In the Future🚀
- Most usefull $eval
- $pyeval
- Support of mods
- Сontributers support
