"""
Ryhavean Userbot - Uptime Robot Handler
Keeps the bot alive 24/7 on Render free tier by responding to HTTP pings
"""

import os
import asyncio
import logging
from datetime import datetime
from aiohttp import web

logger = logging.getLogger("uptimerobot")

class UptimeRobotHandler:
    """Handles HTTP requests from Uptime Robot"""
    
    def __init__(self, port=8000):
        self.port = port
        self.start_time = datetime.now()
        self.request_count = 0
    
    async def health_handler(self, request):
        """Handler for /health endpoint"""
        self.request_count += 1
        uptime = datetime.now() - self.start_time
        
        response = {
            "status": "ok",
            "bot": "Ryhavean Userbot",
            "version": "1.0.0",
            "uptime_seconds": int(uptime.total_seconds()),
            "requests": self.request_count,
            "timestamp": datetime.now().isoformat()
        }
        
        return web.json_response(response, status=200)
    
    async def ping_handler(self, request):
        """Handler for /ping endpoint (simple ping)"""
        return web.Response(text="pong", status=200)
    
    async def status_handler(self, request):
        """Handler for /status endpoint"""
        uptime = datetime.now() - self.start_time
        
        status_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Ryhavean Userbot Status</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    margin: 0;
                    padding: 20px;
                    min-height: 100vh;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }}
                .container {{
                    background: white;
                    border-radius: 10px;
                    padding: 30px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                    max-width: 500px;
                    width: 100%;
                }}
                h1 {{
                    color: #667eea;
                    margin-top: 0;
                    text-align: center;
                }}
                .status {{
                    background: #4CAF50;
                    color: white;
                    padding: 10px;
                    border-radius: 5px;
                    text-align: center;
                    font-weight: bold;
                    margin: 20px 0;
                }}
                .info {{
                    margin: 15px 0;
                    padding: 10px;
                    background: #f5f5f5;
                    border-radius: 5px;
                }}
                .label {{
                    font-weight: bold;
                    color: #667eea;
                }}
                .value {{
                    color: #333;
                }}
                .footer {{
                    text-align: center;
                    color: #999;
                    margin-top: 20px;
                    font-size: 12px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🤖 Ryhavean Userbot</h1>
                <div class="status">✓ Active & Running</div>
                <div class="info">
                    <span class="label">Status:</span>
                    <span class="value">✅ Online</span>
                </div>
                <div class="info">
                    <span class="label">Version:</span>
                    <span class="value">1.0.0</span>
                </div>
                <div class="info">
                    <span class="label">Uptime:</span>
                    <span class="value">{int(uptime.total_seconds())} seconds ({uptime.days} days)</span>
                </div>
                <div class="info">
                    <span class="label">Requests:</span>
                    <span class="value">{self.request_count}</span>
                </div>
                <div class="info">
                    <span class="label">Last Update:</span>
                    <span class="value">{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</span>
                </div>
                <div class="footer">
                    <p>Ryhavean Userbot v1.0.0 | Powered by Pyrogram</p>
                    <p>
                        <a href="https://t.me/ryhaveanupdates" style="color: #667eea; text-decoration: none;">📢 Updates</a> |
                        <a href="https://t.me/RyhaveanTeam" style="color: #667eea; text-decoration: none;">👥 Team</a>
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return web.Response(text=status_html, content_type='text/html', status=200)
    
    async def start_server(self):
        """Start the HTTP server"""
        app = web.Application()
        app.router.add_get('/health', self.health_handler)
        app.router.add_get('/ping', self.ping_handler)
        app.router.add_get('/status', self.status_handler)
        app.router.add_get('/', self.status_handler)
        
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, '0.0.0.0', self.port)
        await site.start()
        
        logger.info(f"Uptime Robot HTTP server started on port {self.port}")
        logger.info(f"Access status at: http://localhost:{self.port}/status")
        
        return runner
    
    async def keep_alive(self):
        """Keep the server running"""
        runner = await self.start_server()
        try:
            await asyncio.sleep(float('inf'))
        except KeyboardInterrupt:
            await runner.cleanup()


async def start_uptime_monitor():
    """Start the uptime monitoring"""
    port = int(os.getenv('PORT', 8000))
    handler = UptimeRobotHandler(port)
    await handler.keep_alive()


if __name__ == "__main__":
    asyncio.run(start_uptime_monitor())
