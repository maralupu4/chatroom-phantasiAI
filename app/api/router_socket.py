"""
This file will be responsible for managing WebSocket connections and sending messages between users.
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict

# Initialize the router
router = APIRouter(prefix="/ws/chat")

# Creating a connection manager
class ConnectionManager:
    def __init__(self):
        # Store active connections as {room_id: {user_id: WebSocket}}
        self.active_connections: Dict[int, Dict[int, WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room_id: int, user_id: int):
        """
        Establishes a connection with the user.
        websocket.accept() — confirms the connection.
        """
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = {}
        self.active_connections[room_id][user_id] = websocket

    def disconnect(self, room_id: int, user_id: int):
        """
        Closes the connection and removes it from the list of active ones connections.
        If there are no more users in the room, deletes the room.
        """
        if room_id in self.active_connections and user_id in self.active_connections[room_id]:
            del self.active_connections[room_id][user_id]
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]

    async def broadcast(self, message: str, room_id: int, sender_id: int):
        """
        Broadcasts a message to all users in the room.
        """
        if room_id in self.active_connections:
            for user_id, connection in self.active_connections[room_id].items():
                message_with_class = {
                    "text": message,
                    "is_self": user_id == sender_id
                }
                await connection.send_json(message_with_class)

# Initializing the connection manager
manager = ConnectionManager()

# Creating a WebSocket endpoint
"""
will manage user connections and message transmission in the chatroom.
"""
@router.websocket("/{room_id}/{user_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: int, user_id: int, username: str):  # route
    await manager.connect(websocket, room_id, user_id)  # connects the user to the room
    await manager.broadcast(f"{username} (ID: {user_id}) has joined the chat.", room_id, user_id)  # broadcasts the message to all users in the room
    # Receiving and sending messages in the chatroom
    try: 
        while True: 
            data = await websocket.receive_text() 
            await manager.broadcast(f"{username} (ID: {user_id}): {data}", room_id, user_id) 
    except WebSocketDisconnect: 
        manager.disconnect(room_id, user_id)  # disconnects the user from the room
        await manager.broadcast(f"{username} (ID: {user_id}) has left the chat.", room_id, user_id)
