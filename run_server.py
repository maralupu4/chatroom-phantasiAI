#!/usr/bin/env python3
"""
Run script for the chatroom application.
This script starts the server on all network interfaces (0.0.0.0) 
so it can be accessed from other computers on the network.
"""

import uvicorn
import sys
import socket

def get_local_ip():
    """Get the local IP address of this machine"""
    try:
        # Connect to a public IP without sending any data
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

if __name__ == "__main__":
    port = 8000
    local_ip = get_local_ip()
    print(f"Server running on http://{local_ip}:{port}")
    
    # Run the server on all interfaces (0.0.0.0) so it's accessible from other computers
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",  # Listen on all network interfaces
        port=port,
        reload=True  # Auto-reload on code changes
    )

