# MZscript
## Improved BDFD interpreter in Python
#### Supporting Python 3.10 and newer
## Instaling💻
```
pip install git+https://github.com/MZshnik/MZscript
```

## First step🎉
#### Create your first command:
```py
from MZscript import MZclient

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

#### Use one of this functions:
| Function        | Full support | No args | Can be no/with args |
| :-------------- |------------: | :-: | :- |
|$if|+|-|-
|$elif|+|-|-
|$else|+|+|-
|$stop|-|+|-
|$addButton|-|-|-
|$sendMessage|+|-|+
|$channelID|+|+|-
|$eval|+|-|-
|$message|+|-|+
|$text|+|-|-
|$message|+|-|-
|$prefix|-|-|-
## In Developing🔨
- Database
- More functions from BDFD
- More custom functions
<!-- ## In the Future🚀 -->
