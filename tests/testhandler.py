import unittest
from MZscript.functions_handler import FunctionsHandler

class TestHandler(unittest.IsolatedAsyncioTestCase):
    async def test_chunks_and_ifs(self):
        funcs = FunctionsHandler()
        check_ifs = funcs.check_ifs
        get_chunks = funcs.get_chunks

        result = await get_chunks("$if[1==1] $console[Okay] $else $console[Good] $endif")
        self.assertEqual(result, ["$if[1==1]", " ", "$console[Okay]", " ", "$elif[True]", " ", "$console[Good]", " ", "$endif"])
        self.assertEqual(await check_ifs(result), None)
        with self.assertRaises(SyntaxError):
            result = await get_chunks("$if[1==1] $console[Okay] $else $console[Good]")
            self.assertEqual(result, ["$if[1==1]", " ", "$console[Okay]", " ", "$elif[True]", " ", "$console[Good]"])
            await check_ifs(result)

        with self.assertRaises(SyntaxError):
            result = await get_chunks("$console[Okay] $console[Good] $endif")
            self.assertEqual(result, ["$console[Okay]", " ", "$console[Good]", " ", "$endif"])
            await check_ifs(result)

        with self.assertRaises(SyntaxError):
            result = await get_chunks("$if[1!=1] $console[Okay] $console[Good] $else")
            self.assertEqual(result, ["$if[1!=1]", " ", "$console[Okay]", " ", "$console[Good]", " ", "$elif[True]"])
            await check_ifs(result)

        with self.assertRaises(SyntaxError):
            result = await get_chunks("$endif $console[Okay] $console[Good] $endif")
            self.assertEqual(result, ["$endif", " ", "$console[Okay]", " ", "$console[Good]", " ", "$endif"])
            await check_ifs(result)

        with self.assertRaises(SyntaxError):
            result = await get_chunks("$console[Okay] $else $console[Good] $endif")
            self.assertEqual(result, ["$console[Okay]", " ", "$elif[True]", " ", "$console[Good]", " ", "$endif"])
            await check_ifs(result)

        with self.assertRaises(SyntaxError):
            result = await get_chunks("$console[Okay] $else $console[Good] $if[1==1]")
            self.assertEqual(result, ["$console[Okay]", " ", "$elif[True]", " ", "$console[Good]", " ", "$if[1==1]"])
            await check_ifs(result)

        result = await get_chunks("$if[1==1] $console[Okay] $if[1!=1] $console[All] $endif $else $console[Good] $endif")
        self.assertEqual(result, ["$if[1==1]", " ", "$console[Okay]", " ", "$if[1!=1]", " ", "$console[All]", " ", "$endif", " ", "$elif[True]", " ", "$console[Good]", " ", "$endif"])
        self.assertEqual(await check_ifs(result), None)

        result = await get_chunks("$if[1==1] $console[Okay] $endif")
        self.assertEqual(result, ["$if[1==1]", " ", "$console[Okay]", " ", "$endif"])
        self.assertEqual(await check_ifs(result), None)

        result = await get_chunks("$console[Okay]")
        self.assertEqual(result, ["$console[Okay]"])
        self.assertEqual(await check_ifs(result), None)

if __name__ == "__main__":
    unittest.main()