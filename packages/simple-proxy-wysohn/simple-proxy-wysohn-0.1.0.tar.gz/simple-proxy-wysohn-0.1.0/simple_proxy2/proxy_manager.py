import random
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from threading import Lock
from typing import List, Callable

import requests
from requests import Session

from simple_proxy2.data.proxy_info import ProxyInfo
from simple_proxy2.pool.proxy_pool import ProxyPool
from simple_proxy2.tools.random_user_agent import get_random as random_agent
from simple_proxy2.tools.simple_timer import SimpleTimer


class ProxyManager:
    def __init__(self,
                 test_url: str,
                 proxy_info_dict: dict[str, List[str]],
                 num_executors=32,
                 executor_queue_size=1000,
                 verbose=False):
        self._test_url = test_url
        self._proxy_info_dict = proxy_info_dict
        self._verbose = verbose

        self._pool = self._init_pool(proxy_info_dict)

        self._executor_running = False
        self._executor_workers = num_executors
        self._executor_queue = Queue(executor_queue_size)
        self._executor = ThreadPoolExecutor(max_workers=self._executor_workers)

        self._metrics_lock = Lock()
        self._success = 0
        self._trials = 0

    def _init_pool(self, info_dict: dict[str, List[str]]) -> ProxyPool:
        info_list = []
        for protocol, addresses in info_dict.items():
            for address in addresses:
                info_list.append(ProxyInfo(protocol, address))

        random.shuffle(info_list)
        return ProxyPool(self.success_rate, info_list)

    def _on_success(self):
        with self._metrics_lock:
            self._trials += 1
            self._success += 1

    def _on_fail(self):
        with self._metrics_lock:
            self._trials += 1

    def success_rate(self):
        with self._metrics_lock:
            if self._trials < 1:
                return 0.0
            else:
                return self._success / self._trials

    def proxy_session(self,
                      fn: Callable[[Session], None],
                      exception_handle: Callable[[ProxyInfo, Exception], None] = lambda info, ex: print(info, ex)) -> None:
        def task():
            success = False

            while not success:
                with self._pool.poll() as proxy:
                    session = requests.Session()

                    session.proxies.update(proxy.info().as_requests_dict())
                    session.headers.update({'User-Agent': random_agent()})

                    timer = SimpleTimer()
                    try:
                        with timer:
                            fn(session)

                        success = True
                    except Exception as ex:
                        exception_handle(proxy.info(), ex)
                    finally:
                        proxy.update_response_time(timer.time_elapsed())

                        if success:
                            self._on_success()
                        else:
                            self._on_fail()

                        if self._verbose:
                            print("success rate:", self.success_rate())

        self._executor_queue.put(task)

    def __enter__(self):
        self._pool.start()

        def fn():
            while self._executor_running:
                task = self._executor_queue.get()
                task()

        self._executor_running = True
        for _ in range(self._executor_workers):
            self._executor.submit(fn)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._pool.end()

        self._executor_running = False
        self._executor.shutdown(True)
