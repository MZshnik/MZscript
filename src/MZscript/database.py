import sqlite3


class Database:
    """
    ## Main sqlite3 database in library.
    #### Uses singl connection and synced requests because bots is I/O latency.
    You can add aiosqlite to Database class, if you want, and share with other users.
    ### Methods:
    #### Getters: get value from Database(next - DB), return result if data is exists, else - False
    - `await get_global_var` gets var from Database(next - DB) where user_id and guild_id tables has 0 value by var_name
    - `await get_value_from_member` gets var from DB where user_id and guild_id tables has 0 value by var_name
    - `await get_value_from_guild` gets value from DB where user_id has value 0 by providing guild_id and var_name
    - `await get_value_from_user` gets var from DB where guild_id has value 0 by providing user_id and var_name
    #### Setters: set value in DB, if the data does not exist - it is created
    - `await set_global_var` copy from get_global_var but sets provided value by var_name
    - `await set_value_of_member` copy from get_value_from_member but sets provided value by var_name
    - `await set_value_of_guild` copy from get_value_of_guild but sets provided value by var_name
    - `await set_value_of_user` copy from get_value_of_user but sets provided value by var_name
    """
    def __init__(self):
        self.connection = sqlite3.connect("database.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users(
            guild_id INT,
            user_id INT,
            var_name VARCHAR,
            var_value VARCHAR
            )""")

    async def get_global_var(self, var_name: str):
        result = self.cursor.execute("SELECT var_value FROM users WHERE user_id = ? AND var_name = ? AND guild_id = ?", (0, var_name, 0)).fetchone()
        if result:
            return result[0]
        else:
            return False

    async def get_value_from_member(self, guild_id: str, user_id: int, var_name: str):
        result = self.cursor.execute("SELECT var_value FROM users WHERE guild_id = ? AND user_id = ? AND var_name = ?", (guild_id, user_id, var_name)).fetchone()
        if result:
            return result[0]
        else:
            return False

    async def get_value_from_guild(self, guild_id: int, var_name: str):
        result = self.cursor.execute("SELECT var_value FROM users WHERE guild_id = ? AND var_name = ? AND user_id = ?", (guild_id, var_name, 0)).fetchone()
        if result:
            return result[0]
        else:
            return False

    async def get_value_from_user(self, user_id: int, var_name: str):
        result = self.cursor.execute("SELECT var_value FROM users WHERE user_id = ? AND var_name = ? AND guild_id = ?", (user_id, var_name, 0)).fetchone()
        if result:
            return result[0]
        else:
            return False

    async def set_global_var(self, var_name: str, var_value: str):
        if await self.get_global_var(var_name):
            self.cursor.execute("UPDATE users SET var_value = ? WHERE var_name = ?", (var_value, var_name))
        else:
            self.cursor.execute("INSERT INTO users(guild_id, user_id, var_name, var_value) VALUES(?, ?, ?, ?)", (0, 0, var_name, var_value))
        self.connection.commit()

    async def set_value_of_member(self, guild_id: str, user_id: str, var_name: str, var_value: str):
        if await self.get_value_from_member(guild_id, user_id, var_name):
            self.cursor.execute("UPDATE users SET var_value = ? WHERE var_name = ? AND guild_id = ? AND user_id = ?", (var_value, var_name, guild_id, user_id))
        else:
            self.cursor.execute("INSERT INTO users(guild_id, user_id, var_name, var_value) VALUES(?, ?, ?, ?)", (guild_id, user_id, var_name, var_value))
        self.connection.commit()

    async def set_value_of_guild(self, guild_id: str, var_name: str, var_value: str):
        if await self.get_value_from_guild(guild_id, var_name):
            self.cursor.execute("UPDATE users SET var_value = ? WHERE var_name = ? AND guild_id = ? AND user_id = ?", (var_value, var_name, guild_id, 0))
        else:
            self.cursor.execute("INSERT INTO users(guild_id, user_id, var_name, var_value) VALUES(?, ?, ?, ?)", (guild_id, 0, var_name, var_value))
        self.connection.commit()

    async def set_value_of_user(self, user_id: str, var_name: str, var_value: str):
        if await self.get_value_from_user(user_id, var_name):
            self.cursor.execute("UPDATE users SET var_value = ? WHERE var_name = ? AND guild_id = ? AND user_id = ?", (var_value, var_name, 0, user_id))
        else:
            self.cursor.execute("INSERT INTO users(guild_id, user_id, var_name, var_value) VALUES(?, ?, ?, ?)", (0, user_id, var_name, var_value))
        self.connection.commit()