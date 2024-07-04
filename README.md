# MZscript
## Improved BDFD interpreter in Python
### [Documentation](/docs/DOCS.md)
### [Docs site](https://mzscript.vercel.app)
> [Repository](https://github.com/flash4ki/mzscriptdocs)
### [Discord](https://discord.gg/gfix-bot-community-mz-796504104565211187)
> for contact with @MZshnik ([mzshnik](https://discord.com/channels/@me/700061502089986139)/MZecker)
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
## Content
<details><summary><b>List of all functions</b></summary>
<table>
<thead>
<tr>
<th>Function</th>
<th align="center">Full support</th>
<th align="center">No args</th>
<th align="center">Can be no/with args</th>
</tr>
</thead>
<tbody>
<tr>
<td>$if</td>
<td align="right">+</td>
<td align="center">-</td>
<td align="left">-</td>
</tr>
<tr>
<td>$elif</td>
<td align="right">+</td>
<td align="center">-</td>
<td align="left">-</td>
</tr>
<tr>
<td>$else</td>
<td align="right">+</td>
<td align="center">+</td>
<td align="left">-</td>
</tr>
<tr>
<td>$stop</td>
<td align="right">+</td>
<td align="center">+</td>
<td align="left">-</td>
</tr>
<tr>
<td>$endif</td>
<td align="right">+</td>
<td align="center">+</td>
<td align="left">-</td>
</tr>
<tr>
<td>$eval</td>
<td align="right">-</td>
<td align="center">-</td>
<td align="left">-</td>
</tr>
<tr>
<td>$pyeval</td>
<td align="right">-</td>
<td align="center">-</td>
<td align="left">-</td>
</tr>
<tr>
<td>$guildInfo</td>
<td align="right">+</td>
<td align="center">-</td>
<td align="left">-</td>
</tr>
<tr>
<td>$channelInfo</td>
<td align="right">+</td>
<td align="center">-</td>
<td align="left">-</td>
</tr>
<tr>
<td>$roleInfo</td>
<td align="right">+</td>
<td align="center">-</td>
<td align="left">-</td>
</tr>
<tr>
<td>$userInfo</td>
<td align="right">+</td>
<td align="center">-</td>
<td align="left">-</td>
</tr>
<tr>
<td>$hasRole</td>
<td align="right">+</td>
<td align="center">-</td>
<td align="left">-</td>
</tr>
<tr>
<td>$isMemberExists</td>
<td align="right">+</td>
<td align="center">-</td>
<td align="left">-</td>
</tr>
<tr>
<td>$isRoleExists</td>
<td align="right">+</td>
<td align="center">-</td>
<td align="left">-</td>
</tr>
<tr>
<td>$isUserExists</td>
<td align="right">+</td>
<td align="center">-</td>
<td align="left">-</td>
</tr>
<tr>
<td>$isGuildExists</td>
<td align="right">+</td>
<td align="center">-</td>
<td align="left">-</td>
</tr>
<tr>
<td>$isNumber</td>
<td align="right">+</td>
<td align="center">-</td>
<td align="left">-</td>
</tr>
<tr>
<td>$sendMessage</td>
<td align="right">+</td>
<td align="center">-</td>
<td align="left">-</td>
</tr>
<tr>
<td>$addReaction</td>
<td align="right">+</td>
<td align="center">-</td>
<td align="left">-</td>
</tr>
<tr>
<td>$message</td>
<td align="right">+</td>
<td align="center">-</td>
<td align="left">-</td>
</tr>
<tr>
<td>$text</td>
<td align="right">+</td>
<td align="center">-</td>
<td align="left">-</td>
</tr>
<tr>
<td>$replaceText</td>
<td align="right">+</td>
<td align="center">-</td>
<td align="left">-</td>
</tr>
<tr>
<td>$ban</td>
<td align="right">+</td>
<td align="center">-</td>
<td align="left">-</td>
</tr>
<tr>
<td>$unban</td>
<td align="right">+</td>
<td align="center">-</td>
<td align="left">-</td>
</tr>
<tr>
<td>$kick</td>
<td align="right">+</td>
<td align="center">-</td>
<td align="left">-</td>
</tr>
<tr>
<td>$lowerCase</td>
<td align="right">+</td>
<td align="center">-</td>
<td align="left">-</td>
</tr>
<tr>
<td>$upperCase</td>
<td align="right">+</td>
<td align="center">-</td>
<td align="left">-</td>
</tr>
<tr>
<td>$titleCase</td>
<td align="right">+</td>
<td align="center">-</td>
<td align="left">-</td>
</tr>
<tr>
<td>$customID</td>
<td align="right">+</td>
<td align="center">+</td>
<td align="left">-</td>
</tr>
<tr>
<td>$value</td>
<td align="right">+</td>
<td align="center">-</td>
<td align="left">-</td>
</tr>
<tr>
<td>$options</td>
<td align="right">-</td>
<td align="center">-</td>
<td align="left">-</td>
</tr>
<tr>
<td>$defer</td>
<td align="right">+</td>
<td align="center">+</td>
<td align="left">-</td>
</tr>
<tr>
<td>$var</td>
<td align="right">+</td>
<td align="center">-</td>
<td align="left">-</td>
</tr>
<tr>
<td>$getVar</td>
<td align="right">+</td>
<td align="center">-</td>
<td align="left">-</td>
</tr>
<tr>
<td>$setVar</td>
<td align="right">+</td>
<td align="center">-</td>
<td align="left">-</td>
</tr>
<tr>
<td>$delVar</td>
<td align="right">+</td>
<td align="center">-</td>
<td align="left">-</td>
</tr>
<tr>
<td>$getMemberVar</td>
<td align="right">+</td>
<td align="center">-</td>
<td align="left">-</td>
</tr>
<tr>
<td>$setMemberVar</td>
<td align="right">+</td>
<td align="center">-</td>
<td align="left">-</td>
</tr>
<tr>
<td>$delMemberVar</td>
<td align="right">+</td>
<td align="center">-</td>
<td align="left">-</td>
</tr>
<tr>
<td>$gelGuildVar</td>
<td align="right">+</td>
<td align="center">-</td>
<td align="left">-</td>
</tr>
<tr>
<td>$setGuildVar</td>
<td align="right">+</td>
<td align="center">-</td>
<td align="left">-</td>
</tr>
<tr>
<td>$delGuildVar</td>
<td align="right">+</td>
<td align="center">-</td>
<td align="left">-</td>
</tr>
<tr>
<td>$getUserVar</td>
<td align="right">+</td>
<td align="center">-</td>
<td align="left">-</td>
</tr>
<tr>
<td>$setUserVar</td>
<td align="right">+</td>
<td align="center">-</td>
<td align="left">-</td>
</tr>
<tr>
<td>$delUserVar</td>
<td align="right">+</td>
<td align="center">-</td>
<td align="left">-</td>
</tr>
<tr>
<td>$calculate</td>
<td align="right">+</td>
<td align="center">-</td>
<td align="left">-</td>
</tr>
<tr>
<td>$loop</td>
<td align="right">+</td>
<td align="center">-</td>
<td align="left">-</td>
</tr>
<tr>
<td>$updateCommands</td>
<td align="right">+</td>
<td align="center">-</td>
<td align="left">+</td>
</tr>
<tr>
<td>$docs</td>
<td align="right">+</td>
<td align="center">-</td>
<td align="left">-</td>
</tr>
<tr>
<td>$console</td>
<td align="right">+</td>
<td align="center">-</td>
<td align="left">-</td>
</tr>
</tbody>
</table>
<p>Full support means is function 100% works/tested</p>
</details>

#### List of functions tags:
| Function | Tags |
| -------- | ---- |
|$sendMessage | #addButton, #addMenu, #addOption, #addField, #addReaction |
#### List of events:
| Name | Description |
| -------- | ---- |
|message | Activated when anyone send message |
|button | Activated when anyone press button from bot |
|interaction | Activated when anyone use interaction from bot (button/menu/slashe) |
## In Developing🔨
- More functions from BDFD
- More custom functions
- Documentation
- Сontributing
## In the Future🚀
- Most usefull $eval/$pyeval
- Support of mods

#### Repository and first lines of code by [MZshnik](https://github.com/MZshnik)
