"""
    request 失败回收中间件
"""
import json
from palp import settings
from palp.conn import redis_conn
from palp.middleware.middleware_request_base import RequestMiddleware


class RequestRecycleMiddleware(RequestMiddleware):
    def request_failed(self, spider, request) -> None:
        """
        回收失败的请求

        :param spider:
        :param request:
        :return:
        """
        req = request.to_dict()
        if req['callback']:
            req['callback'] = req['callback'].__name__
        cookie = req['']

        redis_conn.sadd(settings.REDIS_KEY_QUEUE_BAD_REQUEST, json.dumps(request.to_dict(), ensure_ascii=False))
