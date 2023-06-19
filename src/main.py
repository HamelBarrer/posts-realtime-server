from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from .controllers import user_controller, auth_controller
from .controllers.posts import posts_controller

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_controller.router)
app.include_router(user_controller.router)
app.include_router(posts_controller.router)
