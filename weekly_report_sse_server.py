from fastmcp import FastMCP
from datetime import datetime
import os
import logging
import sys
import traceback
import asyncio
import json
from pydantic_settings import BaseSettings
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import threading
import uvicorn

# Configure logging with more detail
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    host: str = "127.0.0.1"
    port: int = 8002  # Different port from the main server
    debug: bool = True

# Get the current project directory
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
REPORTS_DIR = os.path.join(PROJECT_DIR, "reports")

# Log environment variables
logger.info("Initializing FastMCP server...")
settings = Settings()
logger.debug("Environment variables:")
logger.debug(f"FASTMCP_HOST: {settings.host}")
logger.debug(f"FASTMCP_PORT: {settings.port}")

# Ensure reports directory exists
os.makedirs(REPORTS_DIR, exist_ok=True)

# Create a FastAPI app for SSE
app = FastAPI()

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Store connected clients
connected_clients = set()

# Event to notify clients
report_event = asyncio.Event()
latest_report = {"filename": "", "content": ""}

@app.get("/sse")
async def sse_endpoint(request: Request):
    """
    SSE endpoint that clients can connect to for real-time updates
    """
    async def event_generator():
        # Add client to connected clients
        client_id = id(request)
        connected_clients.add(client_id)
        logger.info(f"Client {client_id} connected. Total clients: {len(connected_clients)}")
        
        try:
            # Send initial message
            yield f"data: {json.dumps({'event': 'connected', 'message': 'Connected to Weekly Report SSE'})}\n\n"
            
            # If there's a latest report, send it immediately
            if latest_report["filename"]:
                yield f"data: {json.dumps({'event': 'report', 'filename': latest_report['filename'], 'content': latest_report['content']})}\n\n"
            
            # Wait for new reports
            while True:
                # Wait for the event to be set
                await report_event.wait()
                
                # Send the report data
                yield f"data: {json.dumps({'event': 'report', 'filename': latest_report['filename'], 'content': latest_report['content']})}\n\n"
                
                # Reset the event
                report_event.clear()
        except asyncio.CancelledError:
            # Client disconnected
            logger.info(f"Client {client_id} disconnected")
        finally:
            # Remove client from connected clients
            if client_id in connected_clients:
                connected_clients.remove(client_id)
                logger.info(f"Client {client_id} removed. Total clients: {len(connected_clients)}")
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )

try:
    logger.info("Initializing FastMCP server...")
    settings = Settings()
    mcp = FastMCP(
        "weeklyReportSSEMCPServer",
        base_path="",
        host=settings.host,
        port=settings.port
    )
    logger.info("FastMCP server initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize FastMCP server: {str(e)}")
    logger.error(f"Traceback: {traceback.format_exc()}")
    sys.exit(1)

@mcp.tool(name="write_weekly_report_sse", description="Write a weekly report and notify connected clients via SSE")
async def write_weekly_report_sse(content: str) -> dict:
    """
    Write a weekly report to a text file in the reports directory and notify connected clients.
    
    Args:
        content: The content of the weekly report
        
    Returns:
        A dictionary containing the status of the operation and the filename
    """
    try:
        if not content:
            return {
                "success": False,
                "error": "Report content is required"
            }
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"weekly_report_{timestamp}.txt"
        filepath = os.path.join(REPORTS_DIR, filename)
        
        # Write report to file
        with open(filepath, 'w') as f:
            f.write(content)
        
        logger.info(f"Successfully saved report to {filename}")
        
        # Update latest report
        global latest_report
        latest_report = {"filename": filename, "content": content}
        
        # Notify connected clients
        report_event.set()
        logger.info(f"Notified {len(connected_clients)} connected clients about new report")
        
        return {
            "success": True,
            "message": "Weekly report saved successfully and clients notified",
            "filename": filename,
            "filepath": filepath,
            "clients_notified": len(connected_clients)
        }
    except Exception as e:
        logger.error(f"Error saving report: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return {
            "success": False,
            "error": f"Failed to save weekly report: {str(e)}"
        }

@mcp.tool(name="get_connected_clients", description="Get the number of connected SSE clients")
def get_connected_clients() -> dict:
    """
    Get the number of clients currently connected to the SSE endpoint.
    
    Returns:
        A dictionary containing the number of connected clients
    """
    return {
        "success": True,
        "connected_clients": len(connected_clients)
    }

if __name__ == "__main__":
    try:
        # Start FastAPI in a separate thread
        def start_fastapi():
            uvicorn.run(
                app, 
                host=settings.host, 
                port=settings.port,
                log_level="info" if settings.debug else "error"
            )

        # Create and start FastAPI thread
        fastapi_thread = threading.Thread(target=start_fastapi, daemon=True)
        fastapi_thread.start()

        # Start the FastMCP server
        logger.info("Starting MCP server with SSE support...")
        logger.info(f"FastAPI SSE endpoint available at http://{settings.host}:{settings.port}/sse")
        mcp.run()
    except Exception as e:
        logger.error(f"Error starting server: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        sys.exit(1)
