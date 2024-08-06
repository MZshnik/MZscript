# Welcome, contributors!
This text has describing what you need to know if you want contribute to this repository.
> And if you want write something in locale, very usufull! But in the end
## Projest hierarhi and files
So, project hierarhi looks like this:  
`project dir`  
__.MZscript__  
`general dirs:`  
__.MZscript/docs__  
/docs-files  
__.MZscript/src__  
`main dir of library code`  
__./src/MZscript__  
/library-files like main.py  
`general files:`  
.project-files like README.md and other

__All source files need to be in snake_case, all dirs in camelCase or PascalCase__  
Dirs names are general and can mark big topics or things like "functions"  
Files names should not to confront with other librarys, files in project and other modules/classes.
## Commits and they description
All commits need to simple-short describe all thigs what you do: from creating files, to add docs to funcs.  
Do not exaggerate what you did and indicate only what you did, the rest can be written as comments in the code.
## Creating new things
First all, mean what you do. We dont need unmaded concepts or just string with content like "Hmm maybe here need to add N thing" without describe. If you know what you do - go next

### Creating new function
Name of functions what looks like $function (important -->) builds by this template:
```py
    async def func_functionname(self, ctx, args: str):
        return "" # returning empty string by default
```
__All funcs return `str` type: result of executing or empty string__, interpreter can replace None type to str, but not recommended
This methode writs in lowercase only in Functions file class.  
After adding function, __ONLY after adding, register it__ in `__init__` methode of FunctionsHandler class from [functions_handler](/src/MZscript/functions_handler.py?FunctionsHandler). Add function to `self.all_funcs` after all and if your function no arg or can be no arg - add it to same lists(`self.no_arg_funcs` and `self.can_be_no_arg`).

From template you can see `args: str` argument in simple function, `str` type for arguments is always provided. `ctx` argument can be `disnake.Message`(by default) or other context-exists types. So, please, dont set type `disnake.Message` if your command can work without it - set `ctx = None`, or if it is interaction function - set `ctx: disnake.AppCmdInter` (` = None` if not required). Delet `args` param if your function in `no_arg_funcs` or set `args: str = None` if it can be no args.

For creating $function you can use some methods to save time and easily job:
|`self.`Methode|Description|
|--|--|
|`await self.is_have_functions`|Execute provided `args` argument how code|
|`await self.get_args`|Gets a list of args spllited by ; correctly. Usually uses after `is_have_functions`|
And some params for use:

|`self.`Param|Description|
|--|--|
|`self.handler`|Handler class of functions|
|`self.handler.client`|Main MZClient class|
|`self.bot`|Bot(client) object|
> More params maybe descrubed or added later  
You also can read in-code-docs with examples of use cases
#### Creating new files
1. Create new file in [functions](/src/MZscript/Functions/) directory or create new folder in this dir and create file with this [rules](/docs/CONTRIBUTING.md#projest-hierarhi-and-files)  
2. Insert this setup code to new file
```py
import disnake

from ...functions_handler import FunctionsHandler


class Functions(FunctionsHandler):
    def __init__(self, handler):
        super().__init__()
        self.handler = handler
        self.bot = handler.client.bot

    async def func_newfunc(self, ctx: disnake.Message, args: str):
        ... # some code of function

def setup(handler):
    return Functions(handler)
```
3. Register new folder in [`__init__.py`](/src/MZscript/Functions/__init__.py) like other modules or in `__init__.py` file of folder if you dont create new folder, only file  
Next steps writed in this [header](https://github.com/MZshnik/MZscript/blob/main/docs/CONTRIBUTING.md#creating-new-function)
### What about events
Now, events taked from basic disnake lib. Its just `on_ready`, `on_message` and other. MZClient only wrap it with beautiful MZscript code

This topic is not ended, but you can help end up it!
### Modify library
In this context we talking about library how low-level functionality and code: interpreter, parser, database and etc.  
If you dont know how library works, please, dont change anything: best way is say anyone your idea or create pull request with changes - its a very frail layer.  
However, this code has amout of doc stings, comments and instruments what interdement developer (maybe) know so you actually can understand this massive work and help us imvprove some things or add new!
