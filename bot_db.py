import asyncio
import asyncpg
import datetime


class Db(object):
    """docstring forDb."""

    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.conn = None

    def create(self):
        return self.loop.run_until_complete(self._create()) # ASYNC call method _create

    async def _create(self):  # to connect and create tqble in the database
        self.conn = await asyncpg.connect('postgresql://postgres:root@localhost/postgres')
        await self.conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id integer,
                previous text,
                result text
            )
        ''')
        # age text,
        # sex text,
        # height text,
        # weight text,
        # activity text

    def update(self,id,previous,result):
        return self.loop.create_task(self._update(id,previous,result))

    async def _update(self,id,previous,result):
        await self.conn.execute('''
        UPDATE users
        SET previous = $1, result = $2
        WHERE id = $3
        ''',previous,result,id
        )

    def check(self,id):
        return self.loop.create_task(self._check(id))

    async def _check(self,id):
        row = await self.conn.fetchrow(
                'SELECT * FROM users WHERE id = $1', id
                )

        if row!=None:
            return row
        return False

    def insert(self,id,previous,result):
        return self.loop.create_task(self._insert(id,previous,result))

    async def _insert(self,id,previous,result):

        await self.conn.execute('''
            INSERT INTO users(id,previous, result) VALUES($1, $2, $3)
        ''', id,previous,result)
