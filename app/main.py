from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.router_page import router as router_page
from app.api.router_socket import router as router_socket

# Initializing the FastAPI application
app = FastAPI()

# Connect the folder with static files
app.mount('/static', StaticFiles(directory='app/static'), 'static')

# Register routes
app.include_router(router_socket)
app.include_router(router_page)
