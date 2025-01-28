"""
Asyncio server for handling multiple clients
"""

import logging
import asyncio
from aiohttp import web

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def health_check_endpoint(request):
    """Health check endpoint
    Args:
        request (_type_): _description_
    Returns:
        web.Response: _description_
    """
    logger.info("Health check endpoint called")
    return web.json_response({"message": "Server is running"})


async def server():
    """
    Starts the aiohttp server
    """
    app = web.Application()
    app.add_routes([web.get("/", health_check_endpoint)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8000)
    logger.info("Server is starting on http://localhost:8000")
    await site.start()

    # Wait indefinitely for shutdown signals
    try:
        await asyncio.Event().wait()
    except asyncio.CancelledError:
        logger.info("Server is shutting down")
        await runner.cleanup()


if __name__ == "__main__":
    logger.info("Starting application")
    try:
        asyncio.run(server())
        logger.info("Press Ctrl+C to stop the application")
    except KeyboardInterrupt:
        logger.info("Application stopped manually")
