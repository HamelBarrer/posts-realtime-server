from typing import List
from prisma import Prisma

from ..schemas import posts_schema


async def read_post(post_id: int) -> posts_schema.Post | None:
    prisma = Prisma()
    await prisma.connect()

    data = await prisma.posts.find_unique(
        where={
            'post_id': post_id
        },
        include={
            'user': True
        }
    )

    await prisma.disconnect()

    return data


async def read_posts() -> List[posts_schema.Post] | None:
    prisma = Prisma()
    await prisma.connect()

    data = await prisma.posts.find_many(
        include={
            'user': True
        }
    )

    await prisma.disconnect()

    return data


async def insert_post(post: posts_schema.PostCreate) -> posts_schema.Post:
    prisma = Prisma()
    await prisma.connect()

    data = await prisma.posts.create(
        data={
            'title': post.title,
            'description': post.description,
            'user_id': post.user_id
        },
        include={
            'user': True
        }
    )

    await prisma.disconnect()

    return data
