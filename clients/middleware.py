import logging
import os

from django.conf import settings


logger = logging.getLogger('clients_metrics')
logger.setLevel(logging.INFO)

if not logger.handlers:
    log_path = os.path.join(settings.BASE_DIR, 'clients_metrics.log')
    file_handler = logging.FileHandler(log_path, encoding='utf-8')
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.propagate = False


class ClientMetricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.total_requests = 0
        self.status_2xx = 0
        self.status_4xx = 0
        self.status_5xx = 0
        self.requests_count_since_last_log = 0

    def __call__(self, request):
        response = self.get_response(request)

        if not request.path.startswith('/clients/'):
            return response

        self.total_requests += 1
        self.requests_count_since_last_log += 1

        status_code = response.status_code
        if 200 <= status_code < 300:
            self.status_2xx += 1
        elif 400 <= status_code < 500:
            self.status_4xx += 1
        elif 500 <= status_code < 600:
            self.status_5xx += 1

        if self.requests_count_since_last_log >= 5:
            self._log_metrics()
            self.requests_count_since_last_log = 0

        return response

    def _log_metrics(self):
        logger.info(
            'Clients requests: %d | 2xx: %d, 4xx: %d, 5xx: %d',
            self.total_requests,
            self.status_2xx,
            self.status_4xx,
            self.status_5xx,
        )
