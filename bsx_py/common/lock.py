import threading


class ReadWriteLock:
    def __init__(self, write_promotion=False):
        self._read_ready = threading.Condition(threading.RLock())
        self._write_ready = threading.Condition(threading.RLock())
        self._readers = 0
        self._writers = 0
        self._promote = write_promotion
        self._reader_list = []
        self._writer_list = []

    def acquire_read(self):
        self._read_ready.acquire()
        reader = threading.get_ident()
        try:
            while self._writers > 0 and reader not in self._writer_list:
                self._read_ready.wait()
            self._readers += 1
        finally:
            self._reader_list.append(threading.get_ident())
            self._read_ready.release()

    def release_read(self):
        self._read_ready.acquire()
        try:
            self._readers -= 1
            if not self._readers:
                self._read_ready.notify_all()
        finally:
            self._reader_list.remove(threading.get_ident())
            self._read_ready.release()

    def acquire_write_no_wait(self) -> bool:
        acquired = self._write_ready.acquire(blocking=False)
        if not acquired:
            return False
        self._read_ready.acquire()
        self._writers += 1
        self._writer_list.append(threading.get_ident())
        while self._readers > 0:
            if self._promote and threading.get_ident() in self._reader_list and set(self._reader_list).issubset(
                    set(self._writer_list)):
                break
            else:
                self._read_ready.wait()

        return True

    def release_write(self):
        self._writers -= 1
        self._writer_list.remove(threading.get_ident())
        self._read_ready.notify_all()
        self._read_ready.release()
        self._write_ready.notify_all()
        self._write_ready.release()
