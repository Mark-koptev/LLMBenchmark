from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import router
from core.middleware import logging_middleware
from .lifespan import lifespan


def init_routers(app_: FastAPI) -> None:
    app_.include_router(router)



def create_app() -> FastAPI:
    app_ = FastAPI(
        title="IEMK Management",
        lifespan=lifespan,
    )

    app_.middleware("http")(logging_middleware)

    app_.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    init_routers(app_=app_)
    return app_


app = create_app()
