import threading

class mThreading:
    def thread(func):
        def wrapper(*args):
            threading.Thread(target=func, args=args).start()
        return wrapper
