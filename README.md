# MZscript
## Improved BDFD interpreter in Python
#### Supporting Python 3.10 and newer
#### pip install git+https://github.com/MZshnik/MZscript

## First step
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
