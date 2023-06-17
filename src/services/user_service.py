from typing import List
from prisma import Prisma

from ..schemas import user_schema
from ..utils import hash


async def read_user_by_account(account: str) -> user_schema.User | None:
    prisma = Prisma()
    await prisma.connect()

    data = await prisma.user.find_first(
        where={
            'OR': [
                {
                    'email': account
                },
                {
                    'username': account
                }
            ]
        }
    )

    await prisma.disconnect()

    return data


async def read_user(user_id: int) -> user_schema.User | None:
    prisma = Prisma()
    await prisma.connect()

    data = await prisma.user.find_unique(
        where={
            'userId': user_id
        }
    )

    await prisma.disconnect()

    return data


async def read_users() -> List[user_schema.User]:
    prisma = Prisma()
    await prisma.connect()

    data = await prisma.user.find_many()

    await prisma.disconnect()

    return data


async def insert_user(user: user_schema.UserCreate) -> user_schema.User:
    prisma = Prisma()
    await prisma.connect()

    password = hash.creation_hash(user.password)

    data = await prisma.user.create(
        data={
            'email': user.email,
            'username': user.username,
            'password': password
        }
    )

    await prisma.disconnect()

    return data
