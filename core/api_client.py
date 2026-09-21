import logging
import time
import uuid

import requests

from core.config import API_PREFIX

logger = logging.getLogger(__name__)


class APIClient:
    """Generic HTTP client responsible for API communication and diagnostics."""

    def __init__(self, base_url: str, user_id: str, timeout: int = 10):
        self.base_url = f"{base_url.rstrip("/")}/{API_PREFIX.lstrip('/')}"
        self.timeout = timeout
        self.session = requests.Session()

        self.session.headers.update(
            {
                "accept": "*/*",
                "x-user-id": user_id,
                "Content-Type": "application/json",
            }
        )

    def request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Execute an HTTP request and log request/response diagnostics."""

        correlation_id = str(uuid.uuid4())
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        start_time = time.perf_counter()

        logger.info(
            "[%s] %s %s",
            correlation_id,
            method.upper(),
            url,
        )

        if "json" in kwargs:
            logger.info(
                "[%s] Request body: %s",
                correlation_id,
                kwargs["json"],
            )

        try:
            response = self.session.request(
                method=method,
                url=url,
                timeout=self.timeout,
                **kwargs,
            )

            elapsed_ms = (time.perf_counter() - start_time) * 1000

            logger.info(
                "[%s] Response: %s | %.2f ms",
                correlation_id,
                response.status_code,
                elapsed_ms,
            )

            logger.info(
                "[%s] Response body: %s",
                correlation_id,
                response.text,
            )

            return response

        except requests.RequestException:
            elapsed_ms = (time.perf_counter() - start_time) * 1000

            logger.exception(
                "[%s] Request failed | %.2f ms",
                correlation_id,
                elapsed_ms,
            )

            raise