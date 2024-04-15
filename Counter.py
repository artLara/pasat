from threading import Timer

class Counter:
    def __init__(self):
        self.__seconds = 3
        self.status = None

    def __call__(self):
        self.status = True
        self.timer_thread = Timer(self.__seconds, self.timeout)
        self.timer_thread.start()

    def timeout(self):
        print("time over")
        self.status = False 

    def cancel(self):
        try:
            self.timer_thread.cancel()
        except AttributeError:
            raise RuntimeError("'UserTimer' object not started.")