# https://www.encode.io/databases/database_queries/

import asyncio
import os
import subprocess

import sqlalchemy
from dotenv import load_dotenv

from databases import Database

load_dotenv()


async def main():
    metadata = sqlalchemy.MetaData()

    notes = sqlalchemy.Table(
        "notes",
        metadata,
        sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column("text", sqlalchemy.String(length=100)),
        sqlalchemy.Column("completed", sqlalchemy.Boolean),
    )

    database = Database(
        "postgresql+asyncpg://{USER}:{PASSWORD}@localhost:5432/{DB}".format(
            **{k: os.environ[f"POSTGRES_{k}"] for k in ("USER", "DB", "PASSWORD")}
        ),
    )


    engine = sqlalchemy.create_engine(
        f"{database.url}".replace("+asyncpg","")
    )
    metadata.create_all(engine)

    # Establish the connection pool
    await database.connect()

    # Execute
    query = notes.insert()
    values = {"text": "example1", "completed": True}
    await database.execute(query=query, values=values)

    # Execute many
    query = notes.insert()
    values = [
        {"text": "example2", "completed": False},
        {"text": "example3", "completed": True},
    ]
    await database.execute_many(query=query, values=values)

    # Fetch multiple rows
    query = notes.select()
    rows = await database.fetch_all(query=query)

    # Fetch single row
    query = notes.select()
    row = await database.fetch_one(query=query)

    # Fetch single value, defaults to `column=0`.
    query = notes.select()
    value = await database.fetch_val(query=query)

    # Fetch multiple rows without loading them all into memory at once
    query = notes.select()
    async for row in database.iterate(query=query):
        ...

    # Close all connection in the connection pool
    await database.disconnect()




if __name__ == "__main__":
    # subprocess.run(["docker-compose", "up"])
    asyncio.run(main())
    subprocess.run(["docker-compose", "down"])
