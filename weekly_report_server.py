from fastmcp import FastMCP
from datetime import datetime
import os
import logging
import json
import sys
import traceback
from pydantic_settings import BaseSettings

# Configure logging with more detail
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    host: str = "127.0.0.1"
    port: int =  8001
    debug: bool = True

# Get the current project directory
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
REPORTS_DIR = os.path.join(PROJECT_DIR, "reports")

# Ensure reports directory exists
os.makedirs(REPORTS_DIR, exist_ok=True)

try:
    logger.info("Initializing FastMCP server...")
    settings = Settings()
    mcp = FastMCP(
        "weeklyReportMCPServer",
        base_path="",
        host=settings.host,
        port=settings.port
    )
    logger.info("FastMCP server initialized successfully")
    logger.debug("Environment variables:")
    logger.debug(f"FASTMCP_HOST: {settings.host}")
    logger.debug(f"FASTMCP_PORT: {settings.port}")
except Exception as e:
    logger.error(f"Failed to initialize FastMCP server: {str(e)}")
    logger.error(f"Traceback: {traceback.format_exc()}")
    sys.exit(1)

@mcp.tool(name="write_weekly_report", description="Write a weekly report to a text file in the reports directory")
def write_weekly_report(content: str) -> dict:
    """
    Write a weekly report to a text file in the reports directory.
    
    Args:
        content: The content of the weekly report
        
    Returns:
        A dictionary containing the status of the operation and the filename
    """
    try:
        if not content:
            return json.dumps({
                "success": False,
                "error": "Report content is required"
            })
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"weekly_report_{timestamp}.txt"
        filepath = os.path.join(REPORTS_DIR, filename)
        
        # Write report to file
        with open(filepath, 'w') as f:
            f.write(content)
        
        logger.info(f"Successfully saved report to {filename}")
        return {
            "success": True,
            "message": "Weekly report saved successfully",
            "filename": filename,
            "filepath": filepath
        }
    except Exception as e:
        logger.error(f"Error saving report: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return {
            "success": False,
            "error": f"Failed to save weekly report: {str(e)}"
        }

if __name__ == "__main__":
    try:
        logger.info("Starting MCP server...")
        logger.info(f"Server will run on {settings.host}:{settings.port}")
        mcp.run()
    except Exception as e:
        logger.error(f"Error starting MCP server: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        sys.exit(1)
