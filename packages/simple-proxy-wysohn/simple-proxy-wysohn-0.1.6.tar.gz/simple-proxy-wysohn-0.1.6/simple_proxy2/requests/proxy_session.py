from typing import Optional, Callable

import requests
from requests import Session, Response

from simple_proxy2.data.proxy import Proxy

from simple_proxy2.tools.simple_timer import SimpleTimer


class Predicate:
    def __call__(self, response: Response) -> bool:
        pass

    def __repr__(self):
        pass


class PredicateResponse200(Predicate):
    def __call__(self, response: Response) -> bool:
        return response.status_code == 200

    def __repr__(self):
        return "Check for status code 200"


class ProxySession(Session):
    def __init__(self,
                 proxy: Proxy,
                 predicate: Optional[Predicate] = PredicateResponse200(),
                 timeout=2):

        super().__init__()
        self._proxy = proxy
        self._predicate = predicate
        self._timeout = timeout

        self._content_length = -1

    def content_length(self) -> int:
        return self._content_length

    def request(self, method, url,
                params=None, data=None, headers=None, cookies=None, files=None,
                auth=None, timeout=None, allow_redirects=True, proxies=None,
                hooks=None, stream=True, verify=None, cert=None, json=None):

        with self._proxy as current_proxy:
            proxy_dict = current_proxy.info().as_requests_dict()

            timer = SimpleTimer()

            try:
                with timer:
                    response = requests.session().request(method, url, params, data, f_header, cookies, files,
                                                          auth,
                                                          self._timeout if timeout is None else timeout,
                                                          allow_redirects,
                                                          proxy_dict,
                                                          hooks, stream, verify, cert, json)

                    # process stream early here so it doesn't fail later
                    self._content_length = len(response.content)

                    if self._predicate and not self._predicate(response):
                        raise Exception("Predicate failure:", self._predicate)

                    return response
            finally:
                self._proxy.update_response_time(timer.time_elapsed())


