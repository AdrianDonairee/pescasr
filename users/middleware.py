import logging
import json

logger = logging.getLogger(__name__)

class UserRegisterLoggingMiddleware:
    """
    Middleware para loguear request/response en /api/users/register/
    (uso temporal para debugging).
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        if path.startswith("/api/users/register/"):
            try:
                body_bytes = request.body
                body_text = body_bytes.decode("utf-8") if body_bytes else ""
                try:
                    body_parsed = json.loads(body_text) if body_text else {}
                except Exception:
                    body_parsed = body_text
                logger.debug(">>> REGISTER REQUEST PATH: %s", path)
                logger.debug(">>> HEADERS: %s", dict(request.headers))
                logger.debug(">>> BODY: %s", body_parsed)
            except Exception:
                logger.exception("Error leyendo body de request para /api/users/register/")
        response = self.get_response(request)
        if path.startswith("/api/users/register/"):
            try:
                content_preview = (response.content.decode("utf-8") if hasattr(response, "content") else str(response))[:1000]
                logger.debug("<<< REGISTER RESPONSE STATUS: %s", response.status_code)
                logger.debug("<<< REGISTER RESPONSE BODY (preview): %s", content_preview)
            except Exception:
                logger.exception("Error leyendo response para /api/users/register/")
        return response