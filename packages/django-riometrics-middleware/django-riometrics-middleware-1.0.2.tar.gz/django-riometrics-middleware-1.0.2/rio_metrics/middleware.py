import os
import time

from rio_metrics.collector import HTTPMetricsCollector, IOMetricsProtocol

IO_METRICS_HOST = os.environ.get('IO_METRICS_HOST', 'localhost')
IO_METRICS_UDP_PORT = int(os.environ.get('IO_METRICS_UDP_PORT', '8092'))
IO_METRICS_HTTP_PORT = int(os.environ.get('IO_METRICS_HTTP_PORT', '8093'))
IO_METRICS_PROTOCOL = os.environ.get('IO_METRICS_PROTOCOL', 'udp')


class HTTPMetricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        port = IO_METRICS_UDP_PORT
        if IO_METRICS_PROTOCOL == IOMetricsProtocol.HTTP.value:
            port = IO_METRICS_HTTP_PORT
        self.collector = HTTPMetricsCollector(IO_METRICS_PROTOCOL, IO_METRICS_HOST, port)

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        self.collector.collect(duration=time.time() - start_time,
                               method=request.method, path=request.path,
                               code=response.status_code)
        return response
