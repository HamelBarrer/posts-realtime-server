import json
from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import parse_raw_as

from ...services import posts_service
from ...schemas import posts_schema
from ...websocket import websocket_manager

from . import websocket_post

router = APIRouter(
    prefix='/api/v1/posts'
)


@router.get('/{post_id}', response_model=posts_schema.Post)
async def get_post(post_id: int):
    data = await posts_service.read_post(post_id)
    if data is None:
        raise HTTPException(status_code=404, detail='Post not found')

    return data


@router.get('/', response_model=list[posts_schema.Post])
async def get_posts():
    data = await posts_service.read_posts()
    if len(data) == 0:
        raise HTTPException(status_code=204, detail='Not posts')

    return data


@router.post('/', response_model=posts_schema.Post)
async def create_post(post: posts_schema.PostCreate):
    data = await posts_service.insert_post(post)

    return data


manager = websocket_manager.ConnectionManager()


@router.websocket('/ws')
async def websocker_post(ws: WebSocket):
    await manager.connect(ws)
    try:
        while True:
            data = await ws.receive_json()

            action = data.get('action')

            if action == 'create':
                title = data.get('title')
                description = data.get('description')
                user_id = data.get('user_id')

                post = posts_schema.PostCreate(
                    title=title,
                    description=description,
                    user_id=user_id
                )

                post = await websocket_post.create_post(post)

                for client in manager.active_connections:
                    await manager.send_data(post.json(), client)

            if action == 'read':
                posts = await websocket_post.get_posts()
                post = json.dumps(
                    [posts_schema.Post.parse_obj(post.dict()).dict()
                     for post in posts]
                )
                await manager.send_data(post, ws)
    except WebSocketDisconnect:
        manager.disconnect(ws)
        await manager.broadcast('Disconet')
