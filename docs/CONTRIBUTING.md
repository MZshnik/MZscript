# Welcome, contributors!
This text has describing what you need to know if you want contribute to this repository.
> And if you want write something in locale, very usufull! But in the end
## Projest hierarhi and files
So, projest hierarhi looks like this:  
`projest dir`  
.MZscript  
`general dirs`  
/docs  
./docs-files
/src
`main dir of library code`  
//MZscript  
.//library-files like main.py  
.project-files like README and other

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
        return "" # returnong empty string by default
```
__All funcs return `str` type: result of executing or empty string__, interpreter can replace None type to str, but not recommended
This methode writs in lowercase only in FunctionsCore class from [functions_collector](/src/MZscript/functions_collector.py?FunctionsCore) file.  
After adding function, __ONLY after adding, register it__ in `__init__` methode of FunctionsHandler class from [functions_handler](/src/MZscript/functions_handler.py?FunctionsHandler). Add function to `self.all_funcs` after all and if your function no arg or can be no arg - add it to same lists(`self.no_arg_funcs` and `self.can_be_no_arg`).

From template you can see `args: str` argument in simple function, `str` type for arguments is always provided. `ctx` argument can be `disnake.message.Message`(by default) or other context-exists types. So, pls, dont set type `disnake.message.Message` if your command can work without it or in interactions - set `ctx = None` in first case and just `str` in second. Delet `args` param if your function in `no_arg_funcs`

For creating $function you can use some methods to save time and easily job:
|`self.`Methode|Description|
|--|--|
|`await self.is_have_functions`|Execute provided `args` argument, example, from `func_functionname`|
|`await self.get_args`|Gets a list of args splited by ; correctly. Usually uses after `is_have_functions`|
And some params for use:
|`self.`Param|Description|
|`self.client`|Main MZClient class what sets in `__init__` methode|
> More params maybe descrubed or added later  
You also can read in-code-docs with examples of use cases
### What about events
This topic will be created later
### Modify library
This topic will be created later