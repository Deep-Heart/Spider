from concurrent.futures import ThreadPoolExecutor


class ThreadPool(object):
    def __init__(self):
        super().__init__()
        self.thread_pool = ThreadPoolExecutor()

    def submit(self, fun, *args, **kwargs):
        self.thread_pool.submit(fun, *args, **kwargs)


th_pool = ThreadPool()
