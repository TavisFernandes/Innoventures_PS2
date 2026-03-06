"""
Render production entry point.
Wraps the api_server FastAPI app with production-ready CORS
so deployed frontends can reach the API.
Does NOT modify any original source files.
"""
import os
import sys

# Ensure Backend dir is on the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from starlette.datastructures import MutableHeaders
from starlette.types import ASGIApp, Message, Receive, Scope, Send

# ---------------------------------------------------------------------------
# Thin ASGI middleware that injects permissive CORS headers.
# It runs *before* the original CORSMiddleware in api_server so that
# non-localhost origins (e.g. a Vercel-deployed frontend) are accepted.
# ---------------------------------------------------------------------------

class ProductionCORS:
    """
    Lightweight CORS override that allows any origin listed in the
    CORS_ORIGINS env-var (comma-separated) or '*' by default.
    """

    def __init__(self, app: ASGIApp):
        self.app = app
        raw = os.getenv("CORS_ORIGINS", "*")
        self.allow_all = raw.strip() == "*"
        self.allowed = {o.strip() for o in raw.split(",") if o.strip()}

    def _origin_ok(self, origin: str) -> bool:
        if self.allow_all:
            return True
        return origin in self.allowed

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        # Extract request origin
        req_headers = dict(scope.get("headers", []))
        origin = req_headers.get(b"origin", b"").decode()

        if not origin or not self._origin_ok(origin):
            # No origin header or not allowed → pass through unchanged
            await self.app(scope, receive, send)
            return

        # Handle preflight (OPTIONS) immediately
        method = scope.get("method", "")
        if method == "OPTIONS":
            preflight_headers = [
                (b"access-control-allow-origin", origin.encode()),
                (b"access-control-allow-methods", b"GET,POST,PUT,DELETE,OPTIONS,PATCH"),
                (b"access-control-allow-headers", b"*"),
                (b"access-control-allow-credentials", b"true"),
                (b"access-control-max-age", b"600"),
                (b"content-length", b"0"),
            ]
            await send({"type": "http.response.start", "status": 200, "headers": preflight_headers})
            await send({"type": "http.response.body", "body": b""})
            return

        # For normal requests, inject CORS headers into the response
        async def send_with_cors(message: Message):
            if message["type"] == "http.response.start":
                headers = MutableHeaders(raw=list(message.get("headers", [])))
                headers["access-control-allow-origin"] = origin
                headers["access-control-allow-credentials"] = "true"
                message["headers"] = headers.raw
            await send(message)

        await self.app(scope, receive, send_with_cors)


# ---------------------------------------------------------------------------
# Import the real app and wrap it
# ---------------------------------------------------------------------------
from api_server import app as _app          # noqa: E402  (import after path fix)

_app.add_middleware(ProductionCORS)

# Expose as `app` so uvicorn can find it:  uvicorn render_app:app
app = _app
