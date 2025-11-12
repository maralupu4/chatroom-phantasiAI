"""
This file will be responsible for connecting the client part and testing WebSocket connections. 
It will also be responsible for rendering the chatroom page.
"""

from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import random

# Initializing the route and renderer for the chatroom page
templates = Jinja2Templates(directory='app/templates')
router = APIRouter()

# Endpoint descriptions
"""
The first one will be responsible for rendering the main page
The second one will be responsible for rendering the room page (our group chat)
"""

# Endpoint 1: Main page
@router.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})  # renders the home page

# Endpoint 2: Room page (for joining chatroom)
@router.post("/join_chat", response_class=HTMLResponse)
async def join_chat(request: Request, username: str = Form(...), room_id: int = Form(...)):
    # Simple user_id generation
    user_id = random.randint(100, 100000)  # random user_id
    return templates.TemplateResponse("index.html", 
                                      {"request": request,
                                       "room_id": room_id, # ID of the room the user enters
                                       "username": username, # Username of the user
                                       "user_id": user_id}  # generated user_id
                                      )