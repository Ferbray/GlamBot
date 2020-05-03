import asyncio
import asyncpg
import termcolor


class Database:
    def __init__(
            self,
            user: str = None,
            password: str = None,
            host: str = "127.0.0.1",
            database: str = None,
    ):
        self.connection = asyncio.get_event_loop().run_until_complete(
            asyncpg.connect(user=user, password=password, host=host, database=database)
        )

    async def fetch(
            self, sentence: str, first_row: bool = True, is_dict: bool = False
    ):
        rows = await self.connection.fetch(sentence)
        return (await self.represent_as_dict(rows) if is_dict else rows)[
               :1 if first_row else None
               ]

    async def execute(self, sentence: str):
        return await self.connection.execute(sentence)


    async def set_type_codec(
            self, target: str, encoder=None, decoder=None, schema=None
    ):
        await self.connection.set_type_codec(
            target, encoder=encoder, decoder=decoder, schema=schema
        )

    async def close(self):
        await self.connection.close()

    async def represent_as_dict(self, rows):
        return [dict(row) for row in rows]
