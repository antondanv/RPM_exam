import time

class MetricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.total_requests = 0
        self.status_2xx = 0
        self.status_4xx = 0
        self.status_5xx = 0
        self.requests_count_since_last_log = 0
        
    def __call__(self, request):
        response = self.get_response(request)
        
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
        print("=== METRICS ===")
        print(f"Total requests: {self.total_requests}")
        print(f"2xx: {self.status_2xx}, 4xx: {self.status_4xx}, 5xx: {self.status_5xx}")
        print("===============")