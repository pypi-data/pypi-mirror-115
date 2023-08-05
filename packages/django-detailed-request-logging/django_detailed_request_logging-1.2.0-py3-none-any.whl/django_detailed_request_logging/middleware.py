import json
import logging
from typing import Optional, Tuple

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from rest_framework.permissions import SAFE_METHODS

request_logger = logging.getLogger("django.request")


NO_LOGGING_MARKER = "_NO_LOGGING"


def no_logging(obj):
    """Disable logging on a view

    This decorator works for both class- and function-based views.
    """
    setattr(obj, NO_LOGGING_MARKER, True)
    return obj


def get_ip_address(request: HttpRequest) -> Tuple[Optional[str], Optional[str]]:
    """Get client and proxy IP address.

    :param request: request from which IP address should be extracted
    :return: a tuple of client_ip and proxy_ip. IP addresses are comma separated
        for multiple proxies.
    """
    x_forwarded_for: Optional[str] = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip_list = x_forwarded_for.split(",", maxsplit=1)
        return (ip_list[0], ip_list[1] if len(ip_list) > 1 else None)
    return request.META.get("REMOTE_ADDR"), None


def get_app_name(request: HttpRequest) -> Optional[str]:
    return request.resolver_match.app_name if request.resolver_match else None


def get_method(request: HttpRequest) -> str:
    return request.method or "NONE"


class LoggingMiddleware:
    def __init__(self, get_response=None):
        self.get_response = get_response
        custom_settings = getattr(settings, "LOGGING_REQUEST_MIDDLEWARE", {})
        self.max_body_length = custom_settings.get("max_body_length", 10_000)
        self.apps = tuple(custom_settings.get("apps", ()))
        self.sensitive_headers = frozenset(
            custom_settings.get(
                "sensitive_headers",
                (
                    "HTTP_AUTHORIZATION",
                    "HTTP_COOKIE",
                    "HTTP_PROXY_AUTHORIZATION",
                    "HTTP_X_CSRFTOKEN",
                ),
            )
        )
        self.skip_methods = frozenset(
            m.lower() for m in custom_settings.get("skip_methods", ())
        )
        self.request_body_copy = b""

    def __call__(self, request: HttpRequest):
        self.request_body_copy = request.body
        response = self.get_response(request)
        self.process_request(request, response)
        return response

    def trim_body(self, body: bytes) -> bytes:
        return body[: self.max_body_length]

    @staticmethod
    def get_log_level(status_code: int, method: str) -> int:
        """Get logging level based on response status code and HTTP method type

        4xx WARNING
        5xx ERROR
        Other codes: INFO (modifying methods), DEBUG (non-modifying methods)
        """
        if 400 <= status_code < 500:
            return logging.WARNING
        if 500 <= status_code < 600:
            return logging.ERROR
        if method not in SAFE_METHODS:
            return logging.INFO
        return logging.DEBUG

    def process_request(self, request: HttpRequest, response: HttpResponse):
        if not self._should_skip_log(request):
            self._log_request(request, response)

    def _should_skip_log(self, request: HttpRequest):
        has_skip_field = lambda obj: getattr(obj, NO_LOGGING_MARKER, False) is True
        method = get_method(request).lower()
        if method in self.skip_methods:
            return True
        if request.resolver_match is None:  # HTTP 404
            return False
        if get_app_name(request) not in self.apps:
            return True

        view = request.resolver_match.func
        skip = False
        if hasattr(view, "cls"):
            # djangorestframework
            if has_skip_field(view.cls):  # type: ignore
                skip = True
            elif hasattr(view, "actions"):
                action = view.actions.get(method)  # type: ignore
                if action is not None:
                    skip = has_skip_field(getattr(view.cls, action, None))  # type: ignore
            else:
                skip = has_skip_field(getattr(view.cls, method, None))  # type: ignore
        elif hasattr(view, "view_class"):
            # django class-based views
            skip = has_skip_field(view.view_class) or has_skip_field(  # type: ignore
                getattr(view.view_class, method, None)  # type: ignore
            )
        else:
            # function-based views
            skip = has_skip_field(view)
        return skip

    def _log_request(self, request: HttpRequest, response: HttpResponse):
        method = get_method(request)
        headers = {
            k: "*{masked}*" if k in self.sensitive_headers else v
            for k, v in request.META.items()
            if k.startswith("HTTP_")
        }
        content_type = request.META.get("CONTENT_TYPE", "")
        data = {}
        if content_type == "application/json":
            try:
                data = json.loads(self.request_body_copy)
            except json.decoder.JSONDecodeError:
                data = self.request_body_copy
        body = self.trim_body(self.request_body_copy)
        ip_addr, proxy_ip_addr = get_ip_address(request)
        msg = {
            "message": " ".join(
                [
                    method,
                    request.get_full_path(),
                    str(response.status_code),
                    response.reason_phrase,
                ]
            ),
            "method": request.method,
            "path": request.get_full_path(),
            "status_code": response.status_code,
            "user": request.user.get_username(),
            "content_type": content_type,
            "json": data,
            "headers": headers,
            "body": body,
            "truncated": len(body) < len(self.request_body_copy),
            "app": get_app_name(request),
            "ip_addr": ip_addr,
            "proxy_ip_addr": proxy_ip_addr,
        }
        log_level = self.get_log_level(response.status_code, method)
        request_logger.log(log_level, msg)
