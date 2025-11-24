"""
http_client.py

HTTP client wrapper that handles sessions, headers and optional login.
"""

from typing import Dict, Optional

import requests
from requests import Session, Response


class HttpClient:
    """
    Simple HTTP client built on top of requests.Session.
    Supports optional login flow if needed.
    """

    def __init__(self, user_agent: str = "Mozilla/5.0 (compatible; WebDataScraper/1.0)"):
        self.session: Session = requests.Session()
        self.session.headers.update({"User-Agent": user_agent})

    def get(self, url: str, timeout: int = 10) -> Response:
        response = self.session.get(url, timeout=timeout)
        response.raise_for_status()
        return response

    def post(
        self,
        url: str,
        data: Optional[Dict] = None,
        json: Optional[Dict] = None,
        timeout: int = 10,
    ) -> Response:
        response = self.session.post(url, data=data, json=json, timeout=timeout)
        response.raise_for_status()
        return response

    def login_simple_form(
        self,
        login_url: str,
        username_field: str,
        password_field: str,
        username: str,
        password: str,
        extra_payload: Optional[Dict] = None,
        timeout: int = 10,
    ) -> None:
        """
        Perform a simple HTML form login (no CSRF token).
        """
        payload: Dict[str, str] = {
            username_field: username,
            password_field: password,
        }
        if extra_payload:
            payload.update(extra_payload)

        response = self.post(login_url, data=payload, timeout=timeout)
        if response.status_code != 200:
            raise RuntimeError(f"Login failed with status code {response.status_code}")

    # Here you could add a more advanced login with CSRF token, JWT, etc.
